from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    path('service/<slug:slug>/order/', views.order_create, name='order_create'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('order-tracking/<int:order_id>/', views.order_tracking, name='order_tracking'),
    path('order-tracking/', views.order_tracking_entry, name='order_tracking_entry'),
]
