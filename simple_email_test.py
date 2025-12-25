import os
import sys

# Setup Django
sys.path.insert(0, '/workspaces/Compete/Compete')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Compete.settings'

import django
django.setup()

from django.core.mail import send_mail
from django.contrib.auth.models import User

print("✓ Django setup successful")
print(f"✓ Found {User.objects.count()} users in database")

# Test basic email
try:
    result = send_mail(
        'Test Email',
        'This is a test email from Compete CTF',
        'noreply@compete-ctf.com',
        ['test@example.com'],
    )
    print(f"✓ Email sent successfully! Result: {result}")
except Exception as e:
    print(f"✗ Email failed: {e}")
