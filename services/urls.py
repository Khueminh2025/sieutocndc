from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<slug:slug>/', views.service_detail, name='service_detail'),
    path('<slug:service_slug>/<slug:slug>/', views.product_detail, name='product_detail'),
]