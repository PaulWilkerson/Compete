# Email Functionality Test Guide for Compete CTF

## Overview
This guide will help you test the email functionality on the Compete CTF site.

## Email Configuration Status

✅ **Email Backend Configured**: Console Backend (emails will print to terminal)
✅ **Default From Email**: noreply@compete-ctf.com
✅ **Email Templates**: All templates exist and are properly configured

### Configuration Details (in settings.py):
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'noreply@compete-ctf.com'
```

## Available Email Features

1. **Password Reset Email** - Primary email functionality
   - URL: http://localhost:8000/password_reset/
   - Template: website/templates/account/password_reset_email.html
   - Subject Template: website/templates/account/password_reset_subject.txt

## Manual Test Procedure

### Test 1: Start the Development Server

```bash
cd /workspaces/Compete/Compete
python3 manage.py runserver
```

The server should start on http://localhost:8000

### Test 2: Test Password Reset Email

1. **Navigate to the password reset page:**
   - URL: http://localhost:8000/password_reset/
   
2. **Check if you have a user account:**
   ```bash
   cd /workspaces/Compete/Compete
   python3 manage.py shell
   ```
   
   In the shell:
   ```python
   from django.contrib.auth.models import User
   users = User.objects.all()
   for user in users:
       print(f"Username: {user.username}, Email: {user.email}")
   exit()
   ```

3. **If no users exist, create one:**
   ```bash
   python3 manage.py createsuperuser
   ```
   Or use the signup page: http://localhost:8000/signup/

4. **Test the password reset flow:**
   - Go to: http://localhost:8000/password_reset/
   - Enter the email address of an existing user
   - Click "Send Reset Link"
   - **Check the terminal where you ran `runserver`**
   - You should see the email content printed in the console

5. **Expected Output in Terminal:**
   You should see something like:
   ```
   Content-Type: text/plain; charset="utf-8"
   MIME-Version: 1.0
   Content-Transfer-Encoding: 7bit
   Subject: Password Reset Request - Compete CTF
   From: noreply@compete-ctf.com
   To: user@example.com
   Date: ...
   Message-ID: ...
   
   [Email content with reset link]
   ```

## Automated Test Script

You can also run the automated test script:

```bash
cd /workspaces/Compete
python3 test_email.py
```

This script will:
- Check email configuration
- Verify email templates exist
- Send test emails
- Test password reset functionality

## Expected Results

### ✅ Success Indicators:
1. Email configuration is properly set in settings.py
2. Email templates exist and are accessible
3. Password reset form loads without errors
4. When submitting password reset, email content appears in the terminal console
5. Reset link in email is properly formatted

### ❌ Failure Indicators:
1. Server errors when accessing password reset page
2. No email output in terminal after submitting form
3. Template not found errors
4. ImportError or configuration errors

## Troubleshooting

### Issue: No email output in terminal
**Solution**: Make sure you're watching the terminal where `python3 manage.py runserver` is running, not a different terminal.

### Issue: User has no email
**Solution**: Update the user's email:
```python
python3 manage.py shell
from django.contrib.auth.models import User
user = User.objects.get(username='your_username')
user.email = 'test@example.com'
user.save()
exit()
```

### Issue: Template not found
**Solution**: Check that the templates exist in:
- `/workspaces/Compete/Compete/website/templates/account/password_reset_email.html`
- `/workspaces/Compete/Compete/website/templates/account/password_reset_subject.txt`

## Production Email Configuration

For production, you would need to change the email backend to use a real SMTP server:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@compete-ctf.com'
```

## Summary

The email functionality is now properly configured for development testing:
- ✅ Email backend set to console (prints to terminal)
- ✅ Password reset templates exist and are configured
- ✅ URL routing is properly set up
- ✅ Ready for testing

To test, simply:
1. Run the development server
2. Go to /password_reset/
3. Enter a user's email
4. Check the terminal for email output
