from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lien-he/', views.lien_he, name='lien_he'),
]
