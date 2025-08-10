from .models import Service

def popular_services(request):
    return {
        'popular_services': Service.objects.filter(phobien=True)
    }
