from django.urls import path
from . import views
from . import authentication as auth
from . import tiffins as tiffin
from . import user as user

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('signup',auth.signup),
    path('login-phone', auth.loginWithPhone),
    path('login-google', auth.loginWithGoogle),

    path('profile/<str:id>', user.profile),
    path('address/all/<str:id>', user.addresses),
    path('address/add', user.add_address),
    path('address/setDefault/<str:id>', user.set_default_address),

    path('business_signup', auth.business_signup),
    path('tiffins', tiffin.tiffins),
    path('tiffins/<str:id>', tiffin.tiffin),
    path('add_tiffin', tiffin.add_tiffin)
]