from django.urls import path

from . import views

app_name = "reminders"

urlpatterns = [
    path("", views.index, name="index"),
]
