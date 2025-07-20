from printing.models import ServiceCategory, Service
from slugify import slugify

def generate_unique_slug(instance, field_value, slug_field_name='slug'):
    slug = slugify(field_value)
    ModelClass = instance.__class__
    unique_slug = slug
    num = 1
    while ModelClass.objects.filter(**{slug_field_name: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug

for obj in ServiceCategory.objects.all():
    obj.slug = generate_unique_slug(obj, obj.name)
    obj.save()
# print("✅ Đã fix slug ServiceCategory.")

for obj in Service.objects.all():
    obj.slug = generate_unique_slug(obj, obj.name)
    obj.save()
# print("✅ Đã fix slug Service.")
