import json
import string
from functools import lru_cache

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from tensorflow import keras

from .forms import PostForm
from .models import Profile
from .moderation import moderation_action


MODEL_PATH = settings.BASE_DIR / "models" / "hate_speech_classifier.h5"
VOCABULARY_PATH = settings.BASE_DIR / "models" / "vocabulary.json"


@lru_cache(maxsize=1)
def load_inference_assets():
    """Load the trained model and vocabulary once per application process."""
    model = keras.models.load_model(MODEL_PATH)
    with VOCABULARY_PATH.open(encoding="utf-8") as vocabulary_file:
        vocabulary = json.load(vocabulary_file)
    return model, vocabulary


def encode_text(text, vocabulary):
    cleaned_text = text.translate(str.maketrans("", "", string.punctuation))
    token_ids = [vocabulary["<START>"]]
    token_ids.extend(
        vocabulary.get(word.lower(), vocabulary["<UNK>"])
        for word in cleaned_text.split()
    )
    return keras.preprocessing.sequence.pad_sequences(
        [token_ids],
        value=vocabulary["<PAD>"],
        padding="post",
        maxlen=250,
    )


def predict_hate_probability(text):
    model, vocabulary = load_inference_assets()
    encoded_text = encode_text(text, vocabulary)
    return float(model.predict(encoded_text, verbose=0)[0][0])


def route_post(post):
    """Apply the moderation decision and return its destination route."""
    action = moderation_action(predict_hate_probability(post.body))
    if action == "reject":
        return "Mymedia:warning"
    if action == "review":
        post.approved = False
        post.save()
        return "Mymedia:suspe"
    post.save()
    return "Mymedia:dashboard"


@login_required
def dashboard(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        return redirect(route_post(post))
    return render(request, "Mymedia/dashboard.html", {"form": form})


@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "Mymedia/profile_list.html", {"profiles": profiles})


@login_required
def warning(request):
    return render(request, "Mymedia/warning.html")


@login_required
def suspe(request):
    return render(request, "Mymedia/suspe.html")


@login_required
def profile(request, pk):
    if not hasattr(request.user, "profile"):
        Profile.objects.create(user=request.user)

    selected_profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_profile = request.user.profile
        action = request.POST.get("follow")
        if action == "follow":
            current_profile.follows.add(selected_profile)
        elif action == "unfollow":
            current_profile.follows.remove(selected_profile)
        current_profile.save()

    return render(
        request,
        "Mymedia/profile.html",
        {"profile": selected_profile},
    )


@login_required
def Myprofile(request, pk):
    selected_profile = Profile.objects.get(pk=pk)
    form = PostForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        action = request.POST.get("follow")
        current_profile = request.user.profile
        if action == "follow":
            current_profile.follows.add(selected_profile)
            current_profile.save()
        elif action == "unfollow":
            current_profile.follows.remove(selected_profile)
            current_profile.save()
        elif form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            return redirect(route_post(post))

    return render(
        request,
        "Mymedia/Myprofile.html",
        {"profile": selected_profile, "form": form},
    )
