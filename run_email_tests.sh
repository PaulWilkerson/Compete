#!/bin/bash

# Test Email Functionality for Compete CTF

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║        COMPETE CTF EMAIL FUNCTIONALITY TEST             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

cd /workspaces/Compete/Compete

echo "============================================================"
echo "Test 1: Checking Email Configuration"
echo "============================================================"
grep -A 3 "Email Configuration" Compete/settings.py
echo ""

echo "============================================================"
echo "Test 2: Checking Email Templates"
echo "============================================================"

templates=("website/templates/account/password_reset_email.html" "website/templates/account/password_reset_subject.txt" "website/templates/account/password_reset.html")

for template in "${templates[@]}"; do
    if [ -f "$template" ]; then
        echo "✓ $template: Found"
    else
        echo "✗ $template: Missing"
    fi
done
echo ""

echo "============================================================"
echo "Test 3: Running Python Email Test"
echo "============================================================"
python3 /workspaces/Compete/test_email.py
