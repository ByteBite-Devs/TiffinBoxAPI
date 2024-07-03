from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('signup',views.signup),
    path('send-otp', views.verify_phone_number),
    path('profile/<str:id>', views.profile),
]