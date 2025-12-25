from django.core.management.base import BaseCommand
from cli.models import NewCLIChallenge


class Command(BaseCommand):
    help = 'Populates the database with CLI challenges for all difficulty levels'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting CLI challenge creation...'))
        self.stdout.write(f'Current challenges in database: {NewCLIChallenge.objects.count()}')

        challenges_data = [
            # ========================
            # LINUX CLI - EASY (5 challenges)
            # ========================
            {
                'title': 'List Directory Contents',
                'description': '''Welcome to CLI challenges! Let's start with the basics.

Your task: List all files in the current directory, including hidden files.

What command would you use to accomplish this?

The flag is the command itself (without any path arguments).
Flag format: flag{your_command_here}''',
                'difficulty': 'Easy',
                'category': 'Linux CLI',
                'flag': 'flag{ls -a}'
            },
            {
                'title': 'Print Working Directory',
                'description': '''Understanding where you are in the filesystem is crucial.

Your task: What command displays your current working directory path?

The flag is the command name.
Flag format: flag{your_answer}''',
                'difficulty': 'Easy',
                'category': 'Linux CLI',
                'flag': 'flag{pwd}'
            },
            {
                'title': 'Create a Directory',
                'description': '''File system navigation requires creating directories.

Your task: What command creates a new directory named "projects"?

The flag is the complete command.
Flag format: flag{your_command}''',
                'difficulty': 'Easy',
                'category': 'Linux CLI',
                'flag': 'flag{mkdir projects}'
            },
            {
                'title': 'View File Contents',
                'description': '''You need to read the contents of a file named "readme.txt".

Your task: What command displays the entire contents of a file?

The flag is the command with the filename.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Linux CLI',
                'flag': 'flag{cat readme.txt}'
            },
            {
                'title': 'Copy Files',
                'description': '''File operations are essential in any command line environment.

Your task: Copy a file named "data.txt" to "backup.txt".

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Linux CLI',
                'flag': 'flag{cp data.txt backup.txt}'
            },

            # ========================
            # LINUX CLI - MEDIUM (5 challenges)
            # ========================
            {
                'title': 'Find Files by Name',
                'description': '''You need to locate all files with a specific name pattern.

Your task: Find all files named "config.txt" in the /home directory and its subdirectories.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Linux CLI',
                'flag': 'flag{find /home -name config.txt}'
            },
            {
                'title': 'Search Text in Files',
                'description': '''A log file contains thousands of lines. You need to find entries containing "ERROR".

Your task: Search for the word "ERROR" in a file named "system.log" and display line numbers.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Linux CLI',
                'flag': 'flag{grep -n ERROR system.log}'
            },
            {
                'title': 'Change File Permissions',
                'description': '''Security requires proper file permissions.

Your task: Make a script named "deploy.sh" executable for the owner only.

The flag is the complete command using octal notation.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Linux CLI',
                'flag': 'flag{chmod 700 deploy.sh}'
            },
            {
                'title': 'Process Management',
                'description': '''You need to find and stop a misbehaving process.

Your task: Display all running processes with their PIDs, filtering for processes containing "apache".

The flag is the piped command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Linux CLI',
                'flag': 'flag{ps aux | grep apache}'
            },
            {
                'title': 'Disk Usage Analysis',
                'description': '''System administrators need to monitor disk space.

Your task: Show disk usage of all directories in /var, sorted by size in human-readable format.

The flag is the complete command with options.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Linux CLI',
                'flag': 'flag{du -h /var | sort -h}'
            },

            # ========================
            # LINUX CLI - HARD (5 challenges)
            # ========================
            {
                'title': 'Advanced Text Processing',
                'description': '''You have a CSV file with user data. Extract the 3rd column (email addresses) from users.csv, sort them alphabetically, remove duplicates, and count the total unique emails.

Your task: Create a pipeline command that accomplishes all of this.

The flag is the complete piped command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Linux CLI',
                'flag': 'flag{cut -d, -f3 users.csv | sort | uniq | wc -l}'
            },
            {
                'title': 'Find and Replace in Multiple Files',
                'description': '''A security vulnerability requires updating API keys across multiple configuration files.

Your task: Find all .conf files in /etc and replace "old_key_123" with "new_key_456" in-place.

The flag is the complete command using find and sed.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Linux CLI',
                'flag': 'flag{find /etc -name *.conf -exec sed -i s/old_key_123/new_key_456/g {} \\;}'
            },
            {
                'title': 'Network Troubleshooting',
                'description': '''System is experiencing network issues. You need to trace the route to google.com and limit the output to 15 hops without DNS resolution for faster results.

Your task: Create the traceroute command with appropriate options.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Linux CLI',
                'flag': 'flag{traceroute -n -m 15 google.com}'
            },
            {
                'title': 'Cron Job Scheduling',
                'description': '''Automate a backup script to run every day at 2:30 AM.

Your task: Write the cron expression for this schedule, followed by the command "/usr/local/bin/backup.sh".

The flag is the complete cron line.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Linux CLI',
                'flag': 'flag{30 2 * * * /usr/local/bin/backup.sh}'
            },
            {
                'title': 'Log Analysis Mastery',
                'description': '''Analyze access.log to find the top 5 IP addresses making the most requests.

The log format has IP addresses as the first field. Extract IPs, count occurrences, sort by frequency, and show top 5.

Your task: Create the complete pipeline command.

Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Linux CLI',
                'flag': '''flag{awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5}'''
            },

            # ========================
            # WINDOWS CLI - EASY (5 challenges)
            # ========================
            {
                'title': 'List Files in Windows',
                'description': '''Welcome to Windows Command Prompt challenges!

Your task: List all files in the current directory including hidden files and system files.

The flag is the complete command with options.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Windows CLI',
                'flag': 'flag{dir /a}'
            },
            {
                'title': 'Display Current Directory',
                'description': '''Know where you are in the Windows file system.

Your task: What command displays the current directory path in Windows?

The flag is the command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Windows CLI',
                'flag': 'flag{cd}'
            },
            {
                'title': 'Create a Folder',
                'description': '''File organization starts with creating directories.

Your task: Create a new directory named "Documents" in Windows.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Windows CLI',
                'flag': 'flag{mkdir Documents}'
            },
            {
                'title': 'Display File Content',
                'description': '''View the contents of a text file in Windows.

Your task: Display the contents of "notes.txt".

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Windows CLI',
                'flag': 'flag{type notes.txt}'
            },
            {
                'title': 'Copy Files in Windows',
                'description': '''File operations are fundamental in Windows CMD.

Your task: Copy "report.doc" to "report_backup.doc".

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Windows CLI',
                'flag': 'flag{copy report.doc report_backup.doc}'
            },

            # ========================
            # WINDOWS CLI - MEDIUM (5 challenges)
            # ========================
            {
                'title': 'Find Files by Pattern',
                'description': '''Search for files in the Windows file system.

Your task: Search for all .log files in C:\\Windows\\System32 and its subdirectories.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Windows CLI',
                'flag': 'flag{dir /s C:\\Windows\\System32\\*.log}'
            },
            {
                'title': 'Search Text in Files',
                'description': '''Find specific text within files using Windows CMD.

Your task: Search for the word "password" in "config.ini" (case-insensitive).

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Windows CLI',
                'flag': 'flag{find /i "password" config.ini}'
            },
            {
                'title': 'System Information',
                'description': '''Gather detailed system information in Windows.

Your task: Display detailed system configuration information and save it to a file named "sysinfo.txt".

The flag is the complete command with output redirection.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Windows CLI',
                'flag': 'flag{systeminfo > sysinfo.txt}'
            },
            {
                'title': 'Network Configuration',
                'description': '''View network adapter configuration in Windows.

Your task: Display all network adapter configurations in detail.

The flag is the complete command with options.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Windows CLI',
                'flag': 'flag{ipconfig /all}'
            },
            {
                'title': 'Task Management',
                'description': '''View and manage running processes in Windows.

Your task: List all running processes with their PIDs in verbose format.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Windows CLI',
                'flag': 'flag{tasklist /v}'
            },

            # ========================
            # WINDOWS CLI - HARD (5 challenges)
            # ========================
            {
                'title': 'Advanced File Operations',
                'description': '''Recursively copy all files from C:\\Source to C:\\Backup, including empty directories,
and preserve file attributes and timestamps.

Your task: Use the appropriate command with all necessary options.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Windows CLI',
                'flag': 'flag{xcopy C:\\Source C:\\Backup /E /H /K /O}'
            },
            {
                'title': 'Network Diagnostics',
                'description': '''Perform a continuous ping to 8.8.8.8, but limit it to exactly 10 packets 
and set the packet size to 1500 bytes.

Your task: Construct the ping command with appropriate options.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Windows CLI',
                'flag': 'flag{ping -n 10 -l 1500 8.8.8.8}'
            },
            {
                'title': 'Scheduled Task Creation',
                'description': '''Create a scheduled task named "BackupTask" that runs "C:\\Scripts\\backup.bat" 
every day at 3:00 AM as SYSTEM user.

Your task: Write the schtasks command to create this task.

The flag is the complete command (simplified version focusing on core parameters).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Windows CLI',
                'flag': 'flag{schtasks /create /tn BackupTask /tr C:\\Scripts\\backup.bat /sc daily /st 03:00}'
            },
            {
                'title': 'Service Management',
                'description': '''Query the status of the Windows Update service, then create a command to stop it.

Your task: Write the command to stop the wuauserv service.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Windows CLI',
                'flag': 'flag{net stop wuauserv}'
            },
            {
                'title': 'Registry Query',
                'description': '''Query the Windows Registry to find the value of "ProgramFilesDir" 
in the "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion" key.

Your task: Write the reg query command.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Windows CLI',
                'flag': 'flag{reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion" /v ProgramFilesDir}'
            },

            # ========================
            # POWERSHELL - EASY (5 challenges)
            # ========================
            {
                'title': 'Get PowerShell Version',
                'description': '''Welcome to PowerShell challenges! Let's start by checking your environment.

Your task: Display the PowerShell version information.

The flag is the command to display the PSVersion table.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Powershell',
                'flag': 'flag{$PSVersionTable.PSVersion}'
            },
            {
                'title': 'List Directory Contents',
                'description': '''PowerShell uses cmdlets for operations.

Your task: Use the PowerShell cmdlet to list all items in the current directory.

The flag is the cmdlet name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Powershell',
                'flag': 'flag{Get-ChildItem}'
            },
            {
                'title': 'Create a New File',
                'description': '''File creation in PowerShell uses specific cmdlets.

Your task: Create a new empty file named "test.txt".

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Powershell',
                'flag': 'flag{New-Item -ItemType File -Name test.txt}'
            },
            {
                'title': 'Display File Content',
                'description': '''Read file contents using PowerShell cmdlets.

Your task: Display the contents of "readme.txt".

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Powershell',
                'flag': 'flag{Get-Content readme.txt}'
            },
            {
                'title': 'Get Running Processes',
                'description': '''PowerShell excels at system management.

Your task: List all currently running processes.

The flag is the cmdlet name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Powershell',
                'flag': 'flag{Get-Process}'
            },

            # ========================
            # POWERSHELL - MEDIUM (5 challenges)
            # ========================
            {
                'title': 'Filter Processes by Name',
                'description': '''PowerShell pipelines allow powerful data manipulation.

Your task: Get all processes with names starting with "chrome" and sort them by CPU usage (descending).

The flag is the complete piped command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Powershell',
                'flag': 'flag{Get-Process chrome* | Sort-Object CPU -Descending}'
            },
            {
                'title': 'Search Files by Content',
                'description': '''PowerShell can search through file contents efficiently.

Your task: Search for files containing the text "API_KEY" in all .txt files in the current directory.

The flag is the complete command using Select-String.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Powershell',
                'flag': 'flag{Select-String -Pattern "API_KEY" -Path *.txt}'
            },
            {
                'title': 'Get Service Status',
                'description': '''System administrators need to monitor services.

Your task: Get all services that are currently running.

The flag is the complete piped command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Powershell',
                'flag': 'flag{Get-Service | Where-Object {$_.Status -eq "Running"}}'
            },
            {
                'title': 'Export to CSV',
                'description': '''PowerShell makes data export simple.

Your task: Get all processes, select only Name and CPU properties, and export to "processes.csv".

The flag is the complete piped command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Powershell',
                'flag': 'flag{Get-Process | Select-Object Name,CPU | Export-Csv processes.csv}'
            },
            {
                'title': 'Measure Object Properties',
                'description': '''Calculate statistics on collections of objects.

Your task: Get all files in the current directory and calculate the total size in MB.

The flag is the complete piped command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Powershell',
                'flag': 'flag{Get-ChildItem | Measure-Object -Property Length -Sum}'
            },

            # ========================
            # POWERSHELL - HARD (5 challenges)
            # ========================
            {
                'title': 'Advanced Filtering and Grouping',
                'description': '''Analyze event logs for security incidents.

Your task: Get the last 100 Application event log entries, filter for Error level events,
group by Source, and display count for each source.

The flag is the complete piped command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Powershell',
                'flag': 'flag{Get-EventLog -LogName Application -Newest 100 | Where-Object {$_.EntryType -eq "Error"} | Group-Object Source | Select-Object Name,Count}'
            },
            {
                'title': 'Remote Command Execution',
                'description': '''Execute commands on remote systems using PowerShell remoting.

Your task: Invoke a command to get the computer name on remote server "SERVER01".

The flag is the complete command using Invoke-Command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Powershell',
                'flag': 'flag{Invoke-Command -ComputerName SERVER01 -ScriptBlock {Get-ComputerInfo}}'
            },
            {
                'title': 'Active Directory Query',
                'description': '''Query Active Directory for user information.

Your task: Get all enabled user accounts in the "Sales" organizational unit.

The flag is the complete command using Get-ADUser.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Powershell',
                'flag': 'flag{Get-ADUser -Filter {Enabled -eq $true} -SearchBase "OU=Sales,DC=domain,DC=com"}'
            },
            {
                'title': 'Custom Object Creation',
                'description': '''Create a custom PowerShell object with properties and export it.

Your task: Create a custom object with Name="Server01", Status="Online", Uptime=30 
and export to JSON file "server.json".

The flag is the complete piped command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Powershell',
                'flag': 'flag{[PSCustomObject]@{Name="Server01";Status="Online";Uptime=30} | ConvertTo-Json | Out-File server.json}'
            },
            {
                'title': 'Recursive File Analysis',
                'description': '''Find all files larger than 100MB in C:\\Data and its subdirectories,
sort by size (descending), and display the full path and size in MB.

Your task: Create the complete piped command.

Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Powershell',
                'flag': 'flag{Get-ChildItem -Path C:\\Data -Recurse | Where-Object {$_.Length -gt 100MB} | Sort-Object Length -Descending | Select-Object FullName,@{N="SizeMB";E={$_.Length/1MB}}}'
            },

            # ========================
            # MISCELLANEOUS - EASY (5 challenges)
            # ========================
            {
                'title': 'Basic Git Command',
                'description': '''Version control is essential for developers.

Your task: What command initializes a new Git repository in the current directory?

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{git init}'
            },
            {
                'title': 'SSH Connection',
                'description': '''Connect to remote servers securely.

Your task: Connect to server "remote.example.com" as user "admin" using SSH.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{ssh admin@remote.example.com}'
            },
            {
                'title': 'Archive Creation',
                'description': '''Create compressed archives for backup or distribution.

Your task: Create a gzip-compressed tar archive named "backup.tar.gz" containing the "data" directory.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{tar -czf backup.tar.gz data}'
            },
            {
                'title': 'Download Files',
                'description': '''Download files from the internet using command line.

Your task: Download a file from "https://example.com/file.zip" using curl.

The flag is the complete command with output option.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{curl https://example.com/file.zip -o file.zip}'
            },
            {
                'title': 'Environment Variables',
                'description': '''Display environment variables in Unix-like systems.

Your task: Show the value of the HOME environment variable.

The flag is the command to echo the variable.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{echo $HOME}'
            },

            # ========================
            # MISCELLANEOUS - MEDIUM (5 challenges)
            # ========================
            {
                'title': 'SCP File Transfer',
                'description': '''Securely copy files between systems.

Your task: Copy "report.pdf" from your local machine to "/home/user/documents/" on remote server "server.example.com" as user "john".

The flag is the complete scp command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{scp report.pdf john@server.example.com:/home/user/documents/}'
            },
            {
                'title': 'Docker Container Management',
                'description': '''Run a Docker container from an image.

Your task: Run an nginx container in detached mode, mapping port 8080 on host to port 80 in container, named "webserver".

The flag is the complete docker run command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{docker run -d -p 8080:80 --name webserver nginx}'
            },
            {
                'title': 'Kubernetes Pod Inspection',
                'description': '''Inspect running pods in Kubernetes.

Your task: Get all pods in the "production" namespace with detailed output.

The flag is the complete kubectl command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{kubectl get pods -n production -o wide}'
            },
            {
                'title': 'Git Branch Management',
                'description': '''Create and switch to a new Git branch.

Your task: Create and checkout a new branch named "feature-login" in one command.

The flag is the complete git command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{git checkout -b feature-login}'
            },
            {
                'title': 'System Monitor',
                'description': '''Monitor system resources in real-time on Linux.

Your task: Display an interactive view of running processes, sorted by CPU usage, updating every 2 seconds.

The flag is the command name (the most common system monitoring tool).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{htop}'
            },

            # ========================
            # MISCELLANEOUS - HARD (5 challenges)
            # ========================
            {
                'title': 'Advanced Git Operations',
                'description': '''Rewrite Git history to combine the last 3 commits into one.

Your task: Start an interactive rebase for the last 3 commits.

The flag is the complete git command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{git rebase -i HEAD~3}'
            },
            {
                'title': 'Docker Compose Orchestration',
                'description': '''Start multi-container Docker application in detached mode and build images if they don't exist.

Your task: Write the docker-compose command with appropriate options.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{docker-compose up -d --build}'
            },
            {
                'title': 'SSL Certificate Inspection',
                'description': '''Check the SSL certificate details of a website.

Your task: Use openssl to connect to "example.com" on port 443 and display the certificate.

The flag is the complete openssl command with echo pipe for automated input.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{echo | openssl s_client -connect example.com:443}'
            },
            {
                'title': 'Advanced SSH Tunneling',
                'description': '''Create an SSH tunnel to forward local port 3306 to remote port 3306 on database.internal.com through jumphost.example.com.

Your task: Write the SSH command with local port forwarding.

The flag is the complete ssh command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{ssh -L 3306:database.internal.com:3306 user@jumphost.example.com}'
            },
            {
                'title': 'Kubernetes Deployment Scaling',
                'description': '''Scale a Kubernetes deployment named "api-server" to 5 replicas in the "production" namespace.

Your task: Write the kubectl command to scale the deployment.

The flag is the complete command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{kubectl scale deployment api-server --replicas=5 -n production}'
            },
        ]

        created_count = 0
        skipped_count = 0

        for challenge in challenges_data:
            existing = NewCLIChallenge.objects.filter(title=challenge['title']).first()
            if existing:
                self.stdout.write(self.style.WARNING(f"⏭️  Skipped: {challenge['title']} (already exists)"))
                skipped_count += 1
            else:
                NewCLIChallenge.objects.create(**challenge)
                self.stdout.write(self.style.SUCCESS(f"✅ Created: {challenge['title']} ({challenge['difficulty']} - {challenge['category']})"))
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Summary:"))
        self.stdout.write(self.style.SUCCESS(f"  Created: {created_count} challenges"))
        self.stdout.write(self.style.WARNING(f"  Skipped: {skipped_count} challenges"))
        self.stdout.write(self.style.SUCCESS(f"  Total in database: {NewCLIChallenge.objects.count()} challenges"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))

        # Display breakdown by category and difficulty
        self.stdout.write(self.style.SUCCESS("\nBreakdown by Category and Difficulty:"))
        for category in ['Linux CLI', 'Windows CLI', 'Powershell', 'Miscellaneous']:
            self.stdout.write(f"\n{category}:")
            for difficulty in ['Easy', 'Medium', 'Hard']:
                count = NewCLIChallenge.objects.filter(
                    category=category,
                    difficulty=difficulty
                ).count()
                self.stdout.write(f"  {difficulty}: {count} challenges")
