# Compete CTF Platform

A competitive Capture The Flag (CTF) web application where users solve challenges across multiple categories including CLI, Cyber Security, and Programming to earn points and compete on global leaderboards.

## 🎯 Features

- **Multiple Challenge Categories**: CLI, Cyber Security, and Programming
- **Hosted competitions**: Users create their own CTFs and challenges, instead of only playing the official tracks
- **Entry fees and commission**: Hosts set an entry fee and keep the payout. Compete keeps a commission (default 15%) on every paid entry
- **User Authentication**: Secure signup, login, and password reset
- **Progress Tracking**: Track solved challenges and earned points
- **Leaderboards**: Compete with other players globally
- **Challenge Management**: Admin interface for adding/managing challenges
- **Responsive Design**: Built with Semantic UI for a modern interface

## 🚀 Quick Start

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Paul-W-0/Compete.git
   cd Compete
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment (optional for development):**
   ```bash
   cp Compete/.env.example Compete/.env
   # Edit .env if needed, defaults work for development
   ```

4. **Run migrations:**
   ```bash
   cd Compete
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample challenges (optional):**
   ```bash
   python manage.py populate_cli_challenges
   python manage.py populate_cyber_challenges
   python manage.py populate_programming_challenges
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## 📦 Production Deployment

For production deployment, see the comprehensive [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

**Key production requirements:**
- PostgreSQL database
- SMTP email server
- SSL/TLS certificate
- Web server (Nginx/Apache)
- Python 3.12+

## 🔐 Security

This application follows Django security best practices:
- ✅ Environment variable management
- ✅ CSRF protection
- ✅ Secure password hashing
- ✅ HTTPS enforcement (production)
- ✅ Security headers configured
- ✅ SQL injection protection via ORM

For the complete security assessment, see [PRODUCTION_READINESS_REPORT_UPDATED.md](PRODUCTION_READINESS_REPORT_UPDATED.md).

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete production deployment instructions
- **[PRODUCTION_READINESS_REPORT_UPDATED.md](PRODUCTION_READINESS_REPORT_UPDATED.md)** - Security assessment and status
- **[PRODUCTION_FIXES_SUMMARY.md](PRODUCTION_FIXES_SUMMARY.md)** - Summary of production fixes
- **[.env.example](Compete/.env.example)** - Environment variable template

## 🛠️ Technology Stack

- **Framework**: Django 5.1.4
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Semantic UI, jQuery
- **Authentication**: Django built-in auth system
- **Email**: Django email framework
- **Server**: Gunicorn (production)

## 📋 Project Structure

```
Compete/
├── Compete/              # Main Django project
│   ├── settings.py      # Configuration (with environment variables)
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── cli/                 # CLI challenges app
├── cyber/               # Cyber security challenges app
├── programming/         # Programming challenges app
├── marketplace/         # User-hosted CTFs, entry fees, commissions
├── website/             # Main website app (auth, profiles)
├── templates/           # HTML templates
├── staticfiles/         # Collected static files (production)
├── logs/                # Application logs
├── requirements.txt     # Python dependencies
└── .env.example        # Environment variable template
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Core Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional for development)
USE_POSTGRESQL=False

# Email (optional for development)
USE_SMTP_EMAIL=False

# Hosted competitions
# Percent of each paid entry kept by Compete. Integer from 0 to 50. Default 15.
PLATFORM_COMMISSION_PERCENT=15
MAX_ENTRY_FEE=500.00
# Leave blank in development. Paid entries then use a test-payment button when DEBUG=True.
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

## Hosted competitions

Official CLI, cyber, and programming challenges stay as they are. A separate aggregator lives at `/ctfs/`.

1. A signed-in user hosts a competition, writes challenges (title, description, points, flag), and sets an entry fee. Free events are allowed.
2. The competition stays a draft until it has at least one challenge and the host opens it.
3. Other users pay the entry fee to see challenge text and submit flags. Hosts already have access and do not pay themselves.
4. On each paid entry the fee is split at the current `PLATFORM_COMMISSION_PERCENT` and stored on the entry, so a later rate change does not rewrite history.
5. The host's share shows up under **Earnings**. They can request a payout. Staff review those requests at **Competitions → Commissions**, which is also where Compete's commission total lives.
6. Card payments use Stripe Checkout. Set `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET`, and point Stripe at `https://your-domain/ctfs/stripe/webhook/`. With `DEBUG=True` and no Stripe key, a "Record test payment" button simulates the same ledger split. That button is off when `DEBUG=False`.

For production configuration, see [.env.example](Compete/.env.example).

## 🧪 Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

### Accessing Django Shell
```bash
python manage.py shell
```

## 📊 Production Status

**Status**: ✅ Production Ready  
**Security Score**: 10/10  
**Last Updated**: December 25, 2025

All critical security issues have been resolved. The application is ready for production deployment.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT license.

## 👤 Author

**PaulWilkerson**
- GitHub: [@PaulWilkerson](https://github.com/PaulWilkerson)

## 🙏 Acknowledgments

- Django framework and community
- Semantic UI for the interface
- All CTF challenge contributors

---

For questions or support, please open an issue on GitHub.
