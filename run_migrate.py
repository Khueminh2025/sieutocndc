import os
import django
from django.core.management import call_command

# ✅ Chỉ định settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sieutoc_printing.settings')

# ✅ Setup Django thủ công
django.setup()

# ✅ Gọi migrate
call_command('migrate')
