#!/usr/bin/env python
"""
Quick test script to verify settings work correctly
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, '/workspaces/Compete/Compete')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Compete.settings')

try:
    from Compete import settings
    
    print("=" * 60)
    print("SETTINGS TEST - ALL CHECKS")
    print("=" * 60)
    
    # Test basic settings
    print(f"✓ Settings loaded successfully")
    print(f"✓ DEBUG = {settings.DEBUG}")
    print(f"✓ ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
    print(f"✓ SECRET_KEY = {settings.SECRET_KEY[:20]}...")
    print(f"✓ CSRF_TRUSTED_ORIGINS = {settings.CSRF_TRUSTED_ORIGINS[:2]}")
    
    # Test Django setup
    import django
    django.setup()
    print(f"✓ Django setup successful")
    
    # Test database connection
    from django.db import connection
    print(f"✓ Database: {settings.DATABASES['default']['ENGINE'].split('.')[-1]}")
    
    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    
except Exception as e:
    print("=" * 60)
    print("ERROR OCCURRED:")
    print("=" * 60)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    print("=" * 60)
    sys.exit(1)
