from django.urls import path
from . import views
from . import authentication as auth
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('signup',auth.signup),
    path('login-phone', auth.loginWithPhone),
    path('login-google', auth.loginWithGoogle),
    path('profile/<str:id>', views.profile),
]