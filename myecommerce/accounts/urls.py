from django.urls import path
from . import views

urlpatterns = [
    path('activate/<email_token>/', views.activate, name='activate'),
    path('accounts/signin/', views.signin, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/cart/', views.cart, name='cart'),
    path('add_to_cart/<slug>/', views.add, name='add_to_cart'),
    path('remove_from_cart/<slug>/', views.remove, name='remove_from_cart'),
    path('remove_from_cart_item/<slug>/', views.remove_item, name='remove_from_cart_item'),
    path('accounts/logout/', views.logout, name='logout'),
]

