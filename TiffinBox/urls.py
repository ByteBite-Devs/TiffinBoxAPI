from django.urls import path
from . import views, user, business, orders
from . import tiffins as tiffin
from . import authentication as auth
from . import reviews as reviews

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
    path('tiffin/<str:id>', tiffin.tiffin),
    path('tiffins/add_tiffin', tiffin.add_tiffin),
    path('tiffins/update_tiffin', tiffin.update_tiffin),
    path('tiffins/business/<str:id>', tiffin.business_tiffins),

    path('business/<str:id>', business.get_business),

    path('order/create', orders.create_order),
    path('order/all/<str:id>', orders.get_orders),
    path('order/<int:id>', orders.getOrder),
    path('order/update/<int:id>/<str:status>', orders.update_order),
    path('order/update/<int:id>', orders.updateDeliveryInformation),
    path('order/business/<str:id>', orders.getBusinessOrders),

    path('review/add', reviews.add_review),
    path('reviews/all/<str:id>', reviews.get_reviews),
    path('review/update', reviews.update_review),
    path('review/delete', reviews.delete_review),

]