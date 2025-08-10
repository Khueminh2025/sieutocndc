from django.shortcuts import render
from services.models import Service, Product

def home(request):
    services = Service.objects.all()
    products = Product.objects.filter(phobien=True)[:12]  # lấy 8 sp phổ biến
    return render(request, "core/home.html", {"services": services, "products": products})

def lien_he(request):
    return render(request, 'core/lien_he.html')