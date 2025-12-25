from cli.models import NewCLIChallenge

challenges = [
    # LINUX CLI - EASY
    {'title': 'List Directory Contents', 'description': 'Welcome to CLI challenges! Let\'s start with the basics.\n\nYour task: List all files in the current directory, including hidden files.\n\nWhat command would you use to accomplish this?\n\nThe flag is the command itself (without any path arguments).\nExample format: flag{command_with_options}', 'difficulty': 'Easy', 'category': 'Linux CLI', 'flag': 'flag{ls -a}'},
    {'title': 'Print Working Directory', 'description': 'Understanding where you are in the filesystem is crucial.\n\nYour task: What command displays your current working directory path?\n\nThe flag is the command name.\nFormat: flag{command}', 'difficulty': 'Easy', 'category': 'Linux CLI', 'flag': 'flag{pwd}'},
    {'title': 'Create a Directory', 'description': 'File system navigation requires creating directories.\n\nYour task: What command creates a new directory named "projects"?\n\nThe flag is the complete command.\nFormat: flag{command directory_name}', 'difficulty': 'Easy', 'category': 'Linux CLI', 'flag': 'flag{mkdir projects}'},
    {'title': 'View File Contents', 'description': 'You need to read the contents of a file named "readme.txt".\n\nYour task: What command displays the entire contents of a file?\n\nThe flag is the command with the filename.\nFormat: flag{command filename}', 'difficulty': 'Easy', 'category': 'Linux CLI', 'flag': 'flag{cat readme.txt}'},
    {'title': 'Copy Files', 'description': 'File operations are essential in any command line environment.\n\nYour task: Copy a file named "data.txt" to "backup.txt".\n\nThe flag is the complete command.\nFormat: flag{command source destination}', 'difficulty': 'Easy', 'category': 'Linux CLI', 'flag': 'flag{cp data.txt backup.txt}'},
    
    # LINUX CLI - MEDIUM
    {'title': 'Find Files by Name', 'description': 'You need to locate all files with a specific name pattern.\n\nYour task: Find all files named "config.txt" in the /home directory and its subdirectories.\n\nThe flag is the complete command.\nFormat: flag{command path options}', 'difficulty': 'Medium', 'category': 'Linux CLI', 'flag': 'flag{find /home -name config.txt}'},
    {'title': 'Search Text in Files', 'description': 'A log file contains thousands of lines. You need to find entries containing "ERROR".\n\nYour task: Search for the word "ERROR" in a file named "system.log" and display line numbers.\n\nThe flag is the complete command.\nFormat: flag{command options pattern filename}', 'difficulty': 'Medium', 'category': 'Linux CLI', 'flag': 'flag{grep -n ERROR system.log}'},
    {'title': 'Change File Permissions', 'description': 'Security requires proper file permissions.\n\nYour task: Make a script named "deploy.sh" executable for the owner only.\n\nThe flag is the complete command using octal notation.\nFormat: flag{command permissions filename}', 'difficulty': 'Medium', 'category': 'Linux CLI', 'flag': 'flag{chmod 700 deploy.sh}'},
    {'title': 'Process Management', 'description': 'You need to find and stop a misbehaving process.\n\nYour task: Display all running processes with their PIDs, filtering for processes containing "apache".\n\nThe flag is the piped command.\nFormat: flag{command1 | command2 pattern}', 'difficulty': 'Medium', 'category': 'Linux CLI', 'flag': 'flag{ps aux | grep apache}'},
    {'title': 'Disk Usage Analysis', 'description': 'System administrators need to monitor disk space.\n\nYour task: Show disk usage of all directories in /var, sorted by size in human-readable format.\n\nThe flag is the complete command with options.\nFormat: flag{command options path | sort_command}', 'difficulty': 'Medium', 'category': 'Linux CLI', 'flag': 'flag{du -h /var | sort -h}'},
    
    # LINUX CLI - HARD
    {'title': 'Advanced Text Processing', 'description': 'You have a CSV file with user data. Extract the 3rd column (email addresses) from users.csv, sort them alphabetically, remove duplicates, and count the total unique emails.\n\nYour task: Create a pipeline command that accomplishes all of this.\n\nThe flag is the complete piped command.\nFormat: flag{command1 | command2 | command3 | command4}', 'difficulty': 'Hard', 'category': 'Linux CLI', 'flag': 'flag{cut -d, -f3 users.csv | sort | uniq | wc -l}'},
    {'title': 'Find and Replace in Multiple Files', 'description': 'A security vulnerability requires updating API keys across multiple configuration files.\n\nYour task: Find all .conf files in /etc and replace "old_key_123" with "new_key_456" in-place.\n\nThe flag is the complete command using find and sed.\nFormat: flag{find command with exec}', 'difficulty': 'Hard', 'category': 'Linux CLI', 'flag': 'flag{find /etc -name *.conf -exec sed -i s/old_key_123/new_key_456/g {} \\;}'},
    {'title': 'Network Troubleshooting', 'description': 'System is experiencing network issues. You need to trace the route to google.com and limit the output to 15 hops without DNS resolution for faster results.\n\nYour task: Create the traceroute command with appropriate options.\n\nThe flag is the complete command.\nFormat: flag{command options hostname}', 'difficulty': 'Hard', 'category': 'Linux CLI', 'flag': 'flag{traceroute -n -m 15 google.com}'},
    {'title': 'Cron Job Scheduling', 'description': 'Automate a backup script to run every day at 2:30 AM.\n\nYour task: Write the cron expression for this schedule, followed by the command "/usr/local/bin/backup.sh".\n\nThe flag is the complete cron line.\nFormat: flag{min hour day month weekday command}', 'difficulty': 'Hard', 'category': 'Linux CLI', 'flag': 'flag{30 2 * * * /usr/local/bin/backup.sh}'},
    {'title': 'Log Analysis Mastery', 'description': 'Analyze access.log to find the top 5 IP addresses making the most requests.\n\nThe log format has IP addresses as the first field. Extract IPs, count occurrences, sort by frequency, and show top 5.\n\nYour task: Create the complete pipeline command.\n\nFormat: flag{awk_or_cut | sort | uniq | sort | head}', 'difficulty': 'Hard', 'category': 'Linux CLI', 'flag': 'flag{awk \'{print $1}\' access.log | sort | uniq -c | sort -rn | head -5}'},
    
    # WINDOWS CLI - EASY
    {'title': 'List Files in Windows', 'description': 'Welcome to Windows Command Prompt challenges!\n\nYour task: List all files in the current directory including hidden files and system files.\n\nThe flag is the complete command with options.\nFormat: flag{command /options}', 'difficulty': 'Easy', 'category': 'Windows CLI', 'flag': 'flag{dir /a}'},
    {'title': 'Display Current Directory', 'description': 'Know where you are in the Windows file system.\n\nYour task: What command displays the current directory path in Windows?\n\nThe flag is the command.\nFormat: flag{command}', 'difficulty': 'Easy', 'category': 'Windows CLI', 'flag': 'flag{cd}'},
    {'title': 'Create a Folder', 'description': 'File organization starts with creating directories.\n\nYour task: Create a new directory named "Documents" in Windows.\n\nThe flag is the complete command.\nFormat: flag{command foldername}', 'difficulty': 'Easy', 'category': 'Windows CLI', 'flag': 'flag{mkdir Documents}'},
    {'title': 'Display File Content', 'description': 'View the contents of a text file in Windows.\n\nYour task: Display the contents of "notes.txt".\n\nThe flag is the complete command.\nFormat: flag{command filename}', 'difficulty': 'Easy', 'category': 'Windows CLI', 'flag': 'flag{type notes.txt}'},
    {'title': 'Copy Files in Windows', 'description': 'File operations are fundamental in Windows CMD.\n\nYour task: Copy "report.doc" to "report_backup.doc".\n\nThe flag is the complete command.\nFormat: flag{command source destination}', 'difficulty': 'Easy', 'category': 'Windows CLI', 'flag': 'flag{copy report.doc report_backup.doc}'},
]

created = 0
for c in challenges[:20]:
    if not NewCLIChallenge.objects.filter(title=c['title']).exists():
        NewCLIChallenge.objects.create(**c)
        created += 1
        print(f"Created: {c['title']}")
    else:
        print(f"Skipped: {c['title']}")

print(f"\nCreated {created} challenges (batch 1/3)")
