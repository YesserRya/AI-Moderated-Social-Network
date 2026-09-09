from logging import warning
from django.urls import path
from .views import *

app_name = "Mymedia"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("Myprofile/<int:pk>", Myprofile, name="Myprofile"),
    path("warning", warning, name="warning"),
    path("suspe", suspe, name="suspe"),
    
]

