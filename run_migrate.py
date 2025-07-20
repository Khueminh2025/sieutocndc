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
from printing.models import ServiceCategory
if not ServiceCategory.objects.exists():
    call_command("loaddata", "fixtures_sieutoc_printing_clean.json")
    print("✅ Đã load dữ liệu JSON lên Render.")


# User = get_user_model()

# if not User.objects.filter(username="admin").exists():
#     User.objects.create_superuser("sieutoc", "sieutocndc@example.com", "St134b@!")
#     print("✅ Superuser 'sieutoc' created with password ''")
# else:
#     print("✅ Superuser already exists")