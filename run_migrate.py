# run_migrate.py
from django.core.management import call_command

if __name__ == "__main__":
    call_command('migrate')
