from django import forms
from .models import *


class PostForm(forms.ModelForm):
    body = forms.CharField(required=False,
    widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "What do you think ?...",
                "class": "textarea is-info is-medium",
                "id": "ptext",
                "onmouseover": "check()"
            }
        ),
        label="",
    )

    img = forms.ImageField(required=False,label = "", widget=forms.widgets.FileInput(attrs={"id" : "up"}))

    class Meta:
        model = Post
        exclude = ("user","approved" )
        


