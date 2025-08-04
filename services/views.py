from django.shortcuts import render, get_object_or_404
from .models import Service, Product

def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    products = service.products.all()
    return render(request, 'services/service_detail.html', {
        'service': service,
        'products': products
    })

def product_detail(request, service_slug, slug):
    product = get_object_or_404(Product, slug=slug, service__slug=service_slug)
    return render(request, 'services/product_detail.html', {
        'product': product
    })
