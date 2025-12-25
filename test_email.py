#!/usr/bin/env python3
"""
Script to test email functionality in the Compete CTF application
"""
import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, '/workspaces/Compete/Compete')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Compete.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

def test_email_configuration():
    """Test basic email configuration"""
    print("=" * 60)
    print("Testing Email Configuration")
    print("=" * 60)
    
    from django.conf import settings
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")
    print()

def test_basic_email():
    """Test sending a basic email"""
    print("=" * 60)
    print("Test 1: Basic Email Send")
    print("=" * 60)
    
    try:
        send_mail(
            subject='Test Email from Compete CTF',
            message='This is a test email to verify email functionality.',
            from_email='noreply@compete-ctf.com',
            recipient_list=['test@example.com'],
            fail_silently=False,
        )
        print("✓ Basic email sent successfully!")
        print()
        return True
    except Exception as e:
        print(f"✗ Failed to send basic email: {e}")
        print()
        return False

def test_password_reset_email():
    """Test password reset email functionality"""
    print("=" * 60)
    print("Test 2: Password Reset Email")
    print("=" * 60)
    
    # Check if users exist
    users = User.objects.all()
    print(f"Total users in database: {users.count()}")
    
    if users.count() == 0:
        print("No users found. Creating test user...")
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        print(f"✓ Created test user: {user.username} ({user.email})")
    else:
        user = users.first()
        print(f"Using existing user: {user.username} (Email: {user.email})")
    
    print()
    
    # Test password reset email
    if not user.email:
        print("✗ User has no email address set. Cannot test password reset.")
        print()
        return False
    
    try:
        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Render email template
        email_context = {
            'email': user.email,
            'domain': 'localhost:8000',
            'site_name': 'Compete CTF',
            'uid': uid,
            'user': user,
            'token': token,
            'protocol': 'http',
        }
        
        email_body = render_to_string('account/password_reset_email.html', email_context)
        
        # Send email
        send_mail(
            subject='Password Reset Request - Compete CTF',
            message=email_body,
            from_email='noreply@compete-ctf.com',
            recipient_list=[user.email],
            fail_silently=False,
            html_message=email_body,
        )
        
        print(f"✓ Password reset email sent successfully to {user.email}!")
        print()
        return True
    except Exception as e:
        print(f"✗ Failed to send password reset email: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False

def check_email_templates():
    """Check if email templates exist"""
    print("=" * 60)
    print("Test 3: Email Template Check")
    print("=" * 60)
    
    templates = [
        'account/password_reset_email.html',
        'account/password_reset_subject.txt',
    ]
    
    all_exist = True
    for template in templates:
        template_path = f'/workspaces/Compete/Compete/website/templates/{template}'
        exists = os.path.exists(template_path)
        status = "✓" if exists else "✗"
        print(f"{status} {template}: {'Found' if exists else 'Missing'}")
        if not exists:
            all_exist = False
    
    print()
    return all_exist

def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "COMPETE CTF EMAIL FUNCTIONALITY TEST" + " " * 11 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Run tests
    test_email_configuration()
    templates_ok = check_email_templates()
    basic_ok = test_basic_email()
    reset_ok = test_password_reset_email()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Email Templates: {'✓ PASS' if templates_ok else '✗ FAIL'}")
    print(f"Basic Email: {'✓ PASS' if basic_ok else '✗ FAIL'}")
    print(f"Password Reset: {'✓ PASS' if reset_ok else '✗ FAIL'}")
    print()
    
    if templates_ok and basic_ok and reset_ok:
        print("✓ ALL TESTS PASSED - Email functionality is working!")
    else:
        print("✗ SOME TESTS FAILED - Please review the errors above")
    
    print("=" * 60)
    print()
    print("NOTE: Emails are being sent to console (check terminal output)")
    print("      To see actual emails, look for 'Content-Type: text/plain'")
    print("=" * 60)
    print()

if __name__ == '__main__':
    main()
