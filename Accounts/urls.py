from django.urls import path
from Accounts import views

urlpatterns = [
    path('register/', views.Register, name='register'), 
    path('profile/', views.Profile, name='profile'),
    path('logout/', views.Logout, name='logout'),
    path('delete/', views.Delete, name='delete'),
    path('send-verification-code/', views.send_verification_code, name='send-verification-code'), 
    path('verify-code/',views.verify_code,name = "verify-code")
    
]