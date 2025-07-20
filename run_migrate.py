import os
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model

# ✅ Chỉ định settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sieutoc_printing.settings')

# ✅ Setup Django thủ công
django.setup()

# ✅ Gọi migrate
call_command('migrate')

# Chạy loaddata nếu dữ liệu chưa có
# from printing.models import ServiceCategory
# if not ServiceCategory.objects.exists():
#     call_command("loaddata", "fixtures_sieutoc_printing_clean.json")
#     print("✅ Đã load dữ liệu JSON lên Render.")


# User = get_user_model()

# if not User.objects.filter(username="admin").exists():
#     User.objects.create_superuser("sieutoc", "sieutocndc@example.com", "St134b@!")
#     print("✅ Superuser 'sieutoc' created with password ''")
# else:
#     print("✅ Superuser already exists")

# from slugify import slugify
# from printing.models import ServiceCategory, Service

# def generate_unique_slug(model, base_slug):
#     slug = base_slug
#     counter = 1
#     while model.objects.filter(slug=slug).exists():
#         slug = f"{base_slug}-{counter}"
#         counter += 1
#     return slug

# # Fix slug cho ServiceCategory
# for obj in ServiceCategory.objects.all():
#     base_slug = slugify(obj.name)
#     obj.slug = generate_unique_slug(ServiceCategory, base_slug)
#     obj.save()
# print("✅ ServiceCategory slugs fixed.")

# # Fix slug cho Service
# for obj in Service.objects.all():
#     base_slug = slugify(obj.name)
#     obj.slug = generate_unique_slug(Service, base_slug)
#     obj.save()
# print("✅ Service slugs fixed.")