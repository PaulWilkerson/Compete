#!/usr/bin/env python
import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, '/workspaces/Compete/Compete')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Compete.settings')

import django
django.setup()

from cli.models import NewCLIChallenge

print("Starting CLI challenge creation...")
print(f"Current challenges in database: {NewCLIChallenge.objects.count()}")

challenges_data = [
    # LINUX CLI - EASY (5 challenges)
    {
        'title': 'List Directory Contents',
        'description': '''Welcome to CLI challenges! Let's start with the basics.

Your task: List all files in the current directory, including hidden files.

What command would you use to accomplish this?

The flag is the command itself (without any path arguments).
Example format: flag{command_with_options}''',
        'difficulty': 'Easy',
        'category': 'Linux CLI',
        'flag': 'flag{ls -a}'
    },
    {
        'title': 'Print Working Directory',
        'description': '''Understanding where you are in the filesystem is crucial.

Your task: What command displays your current working directory path?

The flag is the command name.
Format: flag{command}''',
        'difficulty': 'Easy',
        'category': 'Linux CLI',
        'flag': 'flag{pwd}'
    },
    {
        'title': 'Create a Directory',
        'description': '''File system navigation requires creating directories.

Your task: What command creates a new directory named "projects"?

The flag is the complete command.
Format: flag{command directory_name}''',
        'difficulty': 'Easy',
        'category': 'Linux CLI',
        'flag': 'flag{mkdir projects}'
    },
    {
        'title': 'View File Contents',
        'description': '''You need to read the contents of a file named "readme.txt".

Your task: What command displays the entire contents of a file?

The flag is the command with the filename.
Format: flag{command filename}''',
        'difficulty': 'Easy',
        'category': 'Linux CLI',
        'flag': 'flag{cat readme.txt}'
    },
    {
        'title': 'Copy Files',
        'description': '''File operations are essential in any command line environment.

Your task: Copy a file named "data.txt" to "backup.txt".

The flag is the complete command.
Format: flag{command source destination}''',
        'difficulty': 'Easy',
        'category': 'Linux CLI',
        'flag': 'flag{cp data.txt backup.txt}'
    },
    
    # LINUX CLI - MEDIUM (5 challenges)
    {
        'title': 'Find Files by Name',
        'description': '''You need to locate all files with a specific name pattern.

Your task: Find all files named "config.txt" in the /home directory and its subdirectories.

The flag is the complete command.
Format: flag{command path options}''',
        'difficulty': 'Medium',
        'category': 'Linux CLI',
        'flag': 'flag{find /home -name config.txt}'
    },
    {
        'title': 'Search Text in Files',
        'description': '''A log file contains thousands of lines. You need to find entries containing "ERROR".

Your task: Search for the word "ERROR" in a file named "system.log" and display line numbers.

The flag is the complete command.
Format: flag{command options pattern filename}''',
        'difficulty': 'Medium',
        'category': 'Linux CLI',
        'flag': 'flag{grep -n ERROR system.log}'
    },
    {
        'title': 'Change File Permissions',
        'description': '''Security requires proper file permissions.

Your task: Make a script named "deploy.sh" executable for the owner only.

The flag is the complete command using octal notation.
Format: flag{command permissions filename}''',
        'difficulty': 'Medium',
        'category': 'Linux CLI',
        'flag': 'flag{chmod 700 deploy.sh}'
    },
    {
        'title': 'Process Management',
        'description': '''You need to find and stop a misbehaving process.

Your task: Display all running processes with their PIDs, filtering for processes containing "apache".

The flag is the piped command.
Format: flag{command1 | command2 pattern}''',
        'difficulty': 'Medium',
        'category': 'Linux CLI',
        'flag': 'flag{ps aux | grep apache}'
    },
    {
        'title': 'Disk Usage Analysis',
        'description': '''System administrators need to monitor disk space.

Your task: Show disk usage of all directories in /var, sorted by size in human-readable format.

The flag is the complete command with options.
Format: flag{command options path | sort_command}''',
        'difficulty': 'Medium',
        'category': 'Linux CLI',
        'flag': 'flag{du -h /var | sort -h}'
    },
    
    # LINUX CLI - HARD (5 challenges)
    {
        'title': 'Advanced Text Processing',
        'description': '''You have a CSV file with user data. Extract the 3rd column (email addresses) from users.csv, sort them alphabetically, remove duplicates, and count the total unique emails.

Your task: Create a pipeline command that accomplishes all of this.

The flag is the complete piped command.
Format: flag{command1 | command2 | command3 | command4}''',
        'difficulty': 'Hard',
        'category': 'Linux CLI',
        'flag': 'flag{cut -d, -f3 users.csv | sort | uniq | wc -l}'
    },
    {
        'title': 'Find and Replace in Multiple Files',
        'description': '''A security vulnerability requires updating API keys across multiple configuration files.

Your task: Find all .conf files in /etc and replace "old_key_123" with "new_key_456" in-place.

The flag is the complete command using find and sed.
Format: flag{find command with exec}''',
        'difficulty': 'Hard',
        'category': 'Linux CLI',
        'flag': 'flag{find /etc -name *.conf -exec sed -i s/old_key_123/new_key_456/g {} \\;}'
    },
    {
        'title': 'Network Troubleshooting',
        'description': '''System is experiencing network issues. You need to trace the route to google.com and limit the output to 15 hops without DNS resolution for faster results.

Your task: Create the traceroute command with appropriate options.

The flag is the complete command.
Format: flag{command options hostname}''',
        'difficulty': 'Hard',
        'category': 'Linux CLI',
        'flag': 'flag{traceroute -n -m 15 google.com}'
    },
    {
        'title': 'Cron Job Scheduling',
        'description': '''Automate a backup script to run every day at 2:30 AM.

Your task: Write the cron expression for this schedule, followed by the command "/usr/local/bin/backup.sh".

The flag is the complete cron line.
Format: flag{min hour day month weekday command}''',
        'difficulty': 'Hard',
        'category': 'Linux CLI',
        'flag': 'flag{30 2 * * * /usr/local/bin/backup.sh}'
    },
    {
        'title': 'Log Analysis Mastery',
        'description': '''Analyze access.log to find the top 5 IP addresses making the most requests.

The log format has IP addresses as the first field. Extract IPs, count occurrences, sort by frequency, and show top 5.

Your task: Create the complete pipeline command.

Format: flag{awk_or_cut | sort | uniq | sort | head}''',
        'difficulty': 'Hard',
        'category': 'Linux CLI',
        'flag': '''flag{awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5}'''
    },
]

created_count = 0
skipped_count = 0

for challenge in challenges_data:
    existing = NewCLIChallenge.objects.filter(title=challenge['title']).first()
    if existing:
        print(f"⏭️  Skipped: {challenge['title']} (already exists)")
        skipped_count += 1
    else:
        NewCLIChallenge.objects.create(**challenge)
        print(f"✅ Created: {challenge['title']} ({challenge['difficulty']} - {challenge['category']})")
        created_count += 1

print(f"\n{'='*60}")
print(f"Batch 1 Summary - Linux CLI Challenges:")
print(f"  Created: {created_count}")
print(f"  Skipped: {skipped_count}")
print(f"  Total in database: {NewCLIChallenge.objects.count()}")
print(f"{'='*60}")
