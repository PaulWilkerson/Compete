from django.core.management.base import BaseCommand
from cyber.models import NewCyberChallenge


class Command(BaseCommand):
    help = 'Populates the database with Cybersecurity challenges for all difficulty levels'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Cybersecurity challenge creation...'))
        self.stdout.write(f'Current challenges in database: {NewCyberChallenge.objects.count()}')

        challenges_data = [
            # ========================
            # RED TEAM - EASY (7 challenges)
            # ========================
            {
                'title': 'Basic Reconnaissance',
                'description': '''Learn the first phase of ethical hacking.

Your task: What is the process of gathering information about a target called?

This is the first step before any attack.

The flag is the term.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Red Team',
                'flag': 'flag{reconnaissance}'
            },
            {
                'title': 'Port Scanning Basics',
                'description': '''Discover open ports on a target system.

Your task: What tool is commonly used for network discovery and port scanning?

It's often called the "Network Mapper".

The flag is the tool name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Red Team',
                'flag': 'flag{nmap}'
            },
            {
                'title': 'SQL Injection Intro',
                'description': '''Exploit database vulnerabilities.

Your task: What SQL clause always evaluates to true?

Often used in login bypass: ' OR '1'='1

The flag is the clause.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Red Team',
                'flag': 'flag{1=1}'
            },
            {
                'title': 'Default Credentials',
                'description': '''Many systems ship with default passwords.

Your task: What is the most common default username?

Found in routers, cameras, and many IoT devices.

The flag is the username.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Red Team',
                'flag': 'flag{admin}'
            },
            {
                'title': 'Directory Enumeration',
                'description': '''Find hidden directories on web servers.

Your task: What tool is used to brute-force directories and files?

Common choices: dirb, dirbuster, or...?

The flag is the Python-based tool.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Red Team',
                'flag': 'flag{gobuster}'
            },
            {
                'title': 'Social Engineering',
                'description': '''Manipulate people to divulge information.

Your task: What type of email attack impersonates a trusted entity?

Sounds like "fishing" for information.

The flag is the attack type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Red Team',
                'flag': 'flag{phishing}'
            },
            {
                'title': 'Password Cracking',
                'description': '''Break weak password hashes.

Your task: What tool is famous for password cracking?

Named after a medieval ripping tool.

The flag is the tool name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Red Team',
                'flag': 'flag{john}'
            },

            # ========================
            # RED TEAM - MEDIUM (7 challenges)
            # ========================
            {
                'title': 'Reverse Shell',
                'description': '''Establish remote command execution.

Your task: What netcat flag puts it in listening mode?

nc -? 4444

The flag is the single character option.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Red Team',
                'flag': 'flag{l}'
            },
            {
                'title': 'Privilege Escalation',
                'description': '''Gain higher privileges on a compromised system.

Your task: On Linux, what command runs programs with superuser privileges?

The flag is the command.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Red Team',
                'flag': 'flag{sudo}'
            },
            {
                'title': 'XSS Attack',
                'description': '''Cross-Site Scripting vulnerability exploitation.

Your task: What HTML tag is commonly used to inject malicious JavaScript?

<tag>alert('XSS')</tag>

The flag is the tag name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Red Team',
                'flag': 'flag{script}'
            },
            {
                'title': 'Metasploit Framework',
                'description': '''Use the popular penetration testing framework.

Your task: What Metasploit component delivers the malicious code?

It's paired with an exploit.

The flag is the term.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Red Team',
                'flag': 'flag{payload}'
            },
            {
                'title': 'Hash Cracking',
                'description': '''Identify hash types before cracking.

Your task: What is the length of an MD5 hash in hexadecimal characters?

The flag is the number.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Red Team',
                'flag': 'flag{32}'
            },
            {
                'title': 'Web Application Fuzzing',
                'description': '''Test for vulnerabilities by sending unexpected inputs.

Your task: What Python tool is used for web fuzzing?

Created by Edge-Security, it stands for "Web Fuzzer".

The flag is the tool name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Red Team',
                'flag': 'flag{wfuzz}'
            },
            {
                'title': 'Lateral Movement',
                'description': '''Move through a network after initial compromise.

Your task: What Windows tool can be used for remote command execution?

Named after the mind-control technique.

The flag is the tool name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Red Team',
                'flag': 'flag{psexec}'
            },

            # ========================
            # RED TEAM - HARD (6 challenges)
            # ========================
            {
                'title': 'Buffer Overflow Exploitation',
                'description': '''Exploit memory corruption vulnerabilities.

Your task: What register typically holds the return address in x86 architecture?

The flag is the register name (3 letters).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Red Team',
                'flag': 'flag{EIP}'
            },
            {
                'title': 'Active Directory Attack',
                'description': '''Exploit Windows domain authentication.

Your task: What attack passes authentication without cracking passwords?

Involves replaying captured hashes.

The flag is the attack type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Red Team',
                'flag': 'flag{pass-the-hash}'
            },
            {
                'title': 'Pivoting Techniques',
                'description': '''Use compromised host to attack internal network.

Your task: What tool creates encrypted tunnels for pivoting?

SSH, meterpreter, or this popular proxy tool.

The flag is the tool that rhymes with "blocks".
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Red Team',
                'flag': 'flag{socks}'
            },
            {
                'title': 'Kerberos Attack',
                'description': '''Exploit Windows authentication protocol.

Your task: What attack requests service tickets for offline cracking?

Named after roasting a bird.

The flag is the attack name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Red Team',
                'flag': 'flag{Kerberoasting}'
            },
            {
                'title': 'DLL Injection',
                'description': '''Inject malicious code into running processes.

Your task: What Windows API function is commonly used for DLL injection?

Creates a remote thread in another process.

The flag is the function name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Red Team',
                'flag': 'flag{CreateRemoteThread}'
            },
            {
                'title': 'Evasion Techniques',
                'description': '''Bypass antivirus and detection systems.

Your task: What technique modifies malware to avoid signature detection?

The flag is the technique name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Red Team',
                'flag': 'flag{obfuscation}'
            },

            # ========================
            # BLUE TEAM - EASY (7 challenges)
            # ========================
            {
                'title': 'Firewall Basics',
                'description': '''Network security first line of defense.

Your task: What device filters network traffic based on rules?

The flag is the device type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Blue Team',
                'flag': 'flag{firewall}'
            },
            {
                'title': 'Antivirus Detection',
                'description': '''Identify malware signatures.

Your task: What method detects known malware by matching patterns?

The flag is the detection method.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Blue Team',
                'flag': 'flag{signature-based}'
            },
            {
                'title': 'Log Analysis',
                'description': '''Review system logs for security events.

Your task: On Linux, what directory typically contains system logs?

The flag is the absolute path.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Blue Team',
                'flag': 'flag{/var/log}'
            },
            {
                'title': 'Password Policy',
                'description': '''Enforce strong authentication practices.

Your task: What is the minimum recommended password length?

The flag is the number of characters.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Blue Team',
                'flag': 'flag{12}'
            },
            {
                'title': 'Patch Management',
                'description': '''Keep systems up to date.

Your task: What is the process of applying security updates called?

The flag is the term.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Blue Team',
                'flag': 'flag{patching}'
            },
            {
                'title': 'Network Segmentation',
                'description': '''Isolate critical systems.

Your task: What network device divides networks into segments?

The flag is the device type (Layer 3).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Blue Team',
                'flag': 'flag{router}'
            },
            {
                'title': 'Backup Strategy',
                'description': '''Ensure data recovery capability.

Your task: What backup rule suggests 3 copies, 2 media types, 1 offsite?

The flag is the rule name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Blue Team',
                'flag': 'flag{3-2-1}'
            },

            # ========================
            # BLUE TEAM - MEDIUM (7 challenges)
            # ========================
            {
                'title': 'Intrusion Detection',
                'description': '''Monitor network for suspicious activity.

Your task: What does IDS stand for?

The flag is the full term.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Blue Team',
                'flag': 'flag{Intrusion Detection System}'
            },
            {
                'title': 'SIEM Implementation',
                'description': '''Centralize security event management.

Your task: What does SIEM stand for?

The flag is the acronym expansion.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Blue Team',
                'flag': 'flag{Security Information and Event Management}'
            },
            {
                'title': 'Incident Response',
                'description': '''Handle security incidents effectively.

Your task: What is the first phase of incident response?

Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned

The flag is the first phase.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Blue Team',
                'flag': 'flag{Preparation}'
            },
            {
                'title': 'Network Traffic Analysis',
                'description': '''Capture and analyze packets.

Your task: What popular tool captures network traffic?

Named after a shark.

The flag is the tool name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Blue Team',
                'flag': 'flag{Wireshark}'
            },
            {
                'title': 'File Integrity Monitoring',
                'description': '''Detect unauthorized changes to files.

Your task: What cryptographic function creates a unique file fingerprint?

The flag is the function type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Blue Team',
                'flag': 'flag{hash}'
            },
            {
                'title': 'Access Control Lists',
                'description': '''Define who can access what resources.

Your task: What security model uses "least privilege" principle?

The flag is the principle name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Blue Team',
                'flag': 'flag{least privilege}'
            },
            {
                'title': 'Vulnerability Scanning',
                'description': '''Identify security weaknesses proactively.

Your task: What popular commercial vulnerability scanner is widely used?

Developed by Tenable.

The flag is the tool name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Blue Team',
                'flag': 'flag{Nessus}'
            },

            # ========================
            # BLUE TEAM - HARD (6 challenges)
            # ========================
            {
                'title': 'Threat Hunting',
                'description': '''Proactively search for hidden threats.

Your task: What framework categorizes adversary tactics and techniques?

Maintained by MITRE.

The flag is the framework name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Blue Team',
                'flag': 'flag{ATT&CK}'
            },
            {
                'title': 'Memory Forensics',
                'description': '''Analyze RAM for malicious artifacts.

Your task: What framework is used for memory dump analysis?

Created by Volatility Foundation.

The flag is the tool name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Blue Team',
                'flag': 'flag{Volatility}'
            },
            {
                'title': 'Malware Sandboxing',
                'description': '''Analyze suspicious files in isolated environments.

Your task: What online service analyzes files and URLs for malware?

Owned by Google, aggregates multiple AV engines.

The flag is the service name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Blue Team',
                'flag': 'flag{VirusTotal}'
            },
            {
                'title': 'Zero Trust Architecture',
                'description': '''Never trust, always verify security model.

Your task: What is the core principle of Zero Trust?

The flag is the principle.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Blue Team',
                'flag': 'flag{never trust, always verify}'
            },
            {
                'title': 'EDR Implementation',
                'description': '''Endpoint Detection and Response systems.

Your task: What does EDR stand for?

The flag is the full term.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Blue Team',
                'flag': 'flag{Endpoint Detection and Response}'
            },
            {
                'title': 'Chain of Custody',
                'description': '''Maintain evidence integrity for legal proceedings.

Your task: What process documents evidence handling?

Critical for forensic investigations.

The flag is the process name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Blue Team',
                'flag': 'flag{chain of custody}'
            },

            # ========================
            # MISCELLANEOUS - EASY (7 challenges)
            # ========================
            {
                'title': 'CIA Triad',
                'description': '''Fundamental security principles.

Your task: What does CIA stand for in cybersecurity?

The three pillars of information security.

The flag is the acronym expansion.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{Confidentiality, Integrity, Availability}'
            },
            {
                'title': 'Encryption Basics',
                'description': '''Protect data confidentiality.

Your task: What process converts plaintext to ciphertext?

The flag is the process name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{encryption}'
            },
            {
                'title': 'HTTP vs HTTPS',
                'description': '''Secure web communications.

Your task: What does the 'S' in HTTPS stand for?

The flag is the word.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{Secure}'
            },
            {
                'title': 'Two-Factor Authentication',
                'description': '''Add extra security layer to authentication.

Your task: What does 2FA stand for?

The flag is the full term.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{Two-Factor Authentication}'
            },
            {
                'title': 'VPN Purpose',
                'description': '''Secure remote connections.

Your task: What does VPN stand for?

The flag is the full term.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{Virtual Private Network}'
            },
            {
                'title': 'MAC Address',
                'description': '''Hardware addressing in networks.

Your task: How many hexadecimal digits are in a MAC address?

Example: 00:1A:2B:3C:4D:5E

The flag is the count.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{12}'
            },
            {
                'title': 'Public Key Infrastructure',
                'description': '''Certificate-based authentication.

Your task: What does PKI stand for?

The flag is the full term.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{Public Key Infrastructure}'
            },

            # ========================
            # MISCELLANEOUS - MEDIUM (7 challenges)
            # ========================
            {
                'title': 'OSI Model',
                'description': '''Network communication layers.

Your task: How many layers are in the OSI model?

The flag is the number.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{7}'
            },
            {
                'title': 'Cryptographic Hash',
                'description': '''One-way functions for data integrity.

Your task: What is the output size of SHA-256 in bits?

The flag is the number.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{256}'
            },
            {
                'title': 'Digital Signature',
                'description': '''Verify authenticity and integrity.

Your task: What key type is used to create a digital signature?

Public or Private?

The flag is the key type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{Private}'
            },
            {
                'title': 'DNS Security',
                'description': '''Secure domain name resolution.

Your task: What attack redirects DNS queries to malicious servers?

The flag is the attack type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{DNS poisoning}'
            },
            {
                'title': 'SSL/TLS Handshake',
                'description': '''Establish secure connections.

Your task: What protocol replaced SSL for secure communications?

The flag is the protocol abbreviation.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{TLS}'
            },
            {
                'title': 'Port Numbers',
                'description': '''Common service ports.

Your task: What is the default port for HTTPS?

The flag is the port number.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{443}'
            },
            {
                'title': 'Symmetric vs Asymmetric',
                'description': '''Encryption algorithm types.

Your task: Which encryption uses the same key for encryption and decryption?

The flag is the type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{Symmetric}'
            },

            # ========================
            # MISCELLANEOUS - HARD (6 challenges)
            # ========================
            {
                'title': 'Perfect Forward Secrecy',
                'description': '''Protect past communications from future compromises.

Your task: What does PFS stand for?

The flag is the full term.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{Perfect Forward Secrecy}'
            },
            {
                'title': 'Blockchain Security',
                'description': '''Distributed ledger technology.

Your task: What consensus mechanism does Bitcoin use?

The flag is the mechanism name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{Proof of Work}'
            },
            {
                'title': 'Quantum Cryptography',
                'description': '''Post-quantum security concerns.

Your task: What algorithm is considered quantum-resistant?

Named after a mathematical structure.

The flag is the algorithm family.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{Lattice-based}'
            },
            {
                'title': 'Side-Channel Attacks',
                'description': '''Exploit implementation weaknesses.

Your task: What attack analyzes power consumption?

The flag is the attack type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{Power Analysis}'
            },
            {
                'title': 'Secure Boot',
                'description': '''Verify firmware integrity at startup.

Your task: What standard enables secure boot on modern PCs?

The flag is the standard abbreviation.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{UEFI}'
            },
            {
                'title': 'Homomorphic Encryption',
                'description': '''Compute on encrypted data.

Your task: What type of encryption allows operations without decryption?

The flag is the encryption type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{Homomorphic}'
            },
        ]

        created_count = 0
        skipped_count = 0

        for challenge in challenges_data:
            existing = NewCyberChallenge.objects.filter(title=challenge['title']).first()
            if existing:
                self.stdout.write(self.style.WARNING(f"⏭️  Skipped: {challenge['title']} (already exists)"))
                skipped_count += 1
            else:
                NewCyberChallenge.objects.create(**challenge)
                self.stdout.write(self.style.SUCCESS(f"✅ Created: {challenge['title']} ({challenge['difficulty']} - {challenge['category']})"))
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Summary:"))
        self.stdout.write(self.style.SUCCESS(f"  Created: {created_count} challenges"))
        self.stdout.write(self.style.WARNING(f"  Skipped: {skipped_count} challenges"))
        self.stdout.write(self.style.SUCCESS(f"  Total in database: {NewCyberChallenge.objects.count()} challenges"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))

        # Display breakdown by category and difficulty
        self.stdout.write(self.style.SUCCESS("\nBreakdown by Category and Difficulty:"))
        for category in ['Red Team', 'Blue Team', 'Miscellaneous']:
            self.stdout.write(f"\n{category}:")
            for difficulty in ['Easy', 'Medium', 'Hard']:
                count = NewCyberChallenge.objects.filter(
                    category=category,
                    difficulty=difficulty
                ).count()
                self.stdout.write(f"  {difficulty}: {count} challenges")
