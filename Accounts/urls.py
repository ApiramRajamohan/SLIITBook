from django.urls import path
from Accounts import views

urlpatterns = [
    path("/register", views.Register, name="Register"),
]