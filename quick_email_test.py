#!/usr/bin/env python3
"""
Quick Email Test for Compete CTF
Run this script to verify email functionality is working
"""

import os
import sys

# Setup paths
COMPETE_DIR = '/workspaces/Compete/Compete'
sys.path.insert(0, COMPETE_DIR)
os.chdir(COMPETE_DIR)

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Compete.settings')

try:
    import django
    django.setup()
    print("✓ Django initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize Django: {e}")
    sys.exit(1)

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
import os.path

def print_header(text):
    print("\n" + "="*60)
    print(text)
    print("="*60)

def test_configuration():
    """Test email configuration"""
    print_header("EMAIL CONFIGURATION")
    print(f"Backend: {settings.EMAIL_BACKEND}")
    print(f"From Email: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")
    print(f"Host: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
    
    if 'console' in settings.EMAIL_BACKEND.lower():
        print("\n✓ Console backend configured - emails will print to terminal")
        return True
    else:
        print("\n⚠ Non-console backend - emails will try to send via SMTP")
        return True

def test_templates():
    """Check if templates exist"""
    print_header("EMAIL TEMPLATES")
    
    templates_to_check = [
        'account/password_reset_email.html',
        'account/password_reset_subject.txt',
        'account/password_reset.html',
    ]
    
    all_good = True
    for template_name in templates_to_check:
        try:
            template = get_template(template_name)
            print(f"✓ {template_name}")
        except Exception as e:
            print(f"✗ {template_name} - {e}")
            all_good = False
    
    return all_good

def test_send_email():
    """Test sending a basic email"""
    print_header("BASIC EMAIL TEST")
    
    try:
        num_sent = send_mail(
            subject='Test Email - Compete CTF',
            message='This is a test email to verify the email system is working correctly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test@example.com'],
            fail_silently=False,
        )
        print(f"✓ Email sent successfully! (sent to {num_sent} recipient(s))")
        print("\nIf using console backend, check terminal output above for email content.")
        return True
    except Exception as e:
        print(f"✗ Failed to send email: {e}")
        return False

def test_users():
    """Check user database"""
    print_header("USER DATABASE CHECK")
    
    users = User.objects.all()
    count = users.count()
    
    print(f"Total users: {count}")
    
    if count > 0:
        print("\nUsers with email addresses:")
        for user in users[:5]:
            email_status = "✓" if user.email else "✗"
            print(f"  {email_status} {user.username}: {user.email or '(no email)'}")
        
        users_with_email = users.exclude(email='').exclude(email__isnull=True)
        if users_with_email.exists():
            print(f"\n✓ {users_with_email.count()} user(s) have email addresses")
            return True
        else:
            print("\n⚠ No users have email addresses set")
            print("  To test password reset, add an email to a user:")
            print("  python3 manage.py shell")
            print("  >>> from django.contrib.auth.models import User")
            print("  >>> user = User.objects.first()")
            print("  >>> user.email = 'test@example.com'")
            print("  >>> user.save()")
            return False
    else:
        print("\n⚠ No users found in database")
        print("  Create a user first:")
        print("  python3 manage.py createsuperuser")
        print("  Or visit: http://localhost:8000/signup/")
        return False

def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         COMPETE CTF - EMAIL FUNCTIONALITY TEST             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Run all tests
    config_ok = test_configuration()
    templates_ok = test_templates()
    users_ok = test_users()
    email_ok = test_send_email()
    
    # Summary
    print_header("TEST SUMMARY")
    print(f"Configuration:  {'✓ PASS' if config_ok else '✗ FAIL'}")
    print(f"Templates:      {'✓ PASS' if templates_ok else '✗ FAIL'}")
    print(f"Users:          {'✓ PASS' if users_ok else '⚠ WARNING'}")
    print(f"Email Sending:  {'✓ PASS' if email_ok else '✗ FAIL'}")
    
    print("\n" + "="*60)
    if config_ok and templates_ok and email_ok:
        print("✓ EMAIL SYSTEM IS FUNCTIONAL")
        print("\nTo test password reset:")
        print("  1. Run: python3 manage.py runserver")
        print("  2. Visit: http://localhost:8000/password_reset/")
        print("  3. Enter a user's email address")
        print("  4. Check the terminal for email output")
    else:
        print("✗ SOME ISSUES DETECTED - Review errors above")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
