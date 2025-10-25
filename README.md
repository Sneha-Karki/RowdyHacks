# 💰 Budget Buddy - Personal Finance Manager

A modern budgeting application built with Python and Flet, featuring user authentication, CSV import, and AI-powered financial insights.

## 🚀 Tech Stack

- **Frontend/UI**: Flet (Python + Flutter) - Cross-platform web & mobile
- **Database & Auth**: Supabase (PostgreSQL + Auth)
- **AI Analysis**: Claude API / Local Llama
- **Bank Integration**: Plaid (optional)
- **Deployment**: Render (free tier)

## 📦 Features

- ✅ User Authentication (Sign up, Login, Password Reset)
- ✅ Manual Transaction Entry
- ✅ CSV Import for Bank Statements
- ✅ Budget Categories & Tracking
- ✅ AI-Powered Spending Insights
- ✅ Visual Charts & Reports
- ✅ Responsive Web & Mobile UI

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.11+ installed
- Git installed
- VS Code (recommended)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon/public key
- `CLAUDE_API_KEY`: Anthropic Claude API key (optional)
- `PLAID_CLIENT_ID`: Plaid client ID (optional)
- `PLAID_SECRET`: Plaid secret (optional)

### 4. Run the Application
```bash
python main.py
```

For web deployment:
```bash
flet run main.py --web --port 8080
```

## 📁 Project Structure

```
budget-buddy/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── auth/              # Authentication logic
│   │   ├── __init__.py
│   │   └── auth_service.py
│   ├── database/          # Database operations
│   │   ├── __init__.py
│   │   └── db_service.py
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   ├── budget_service.py
│   │   ├── csv_parser.py
│   │   └── ai_insights.py
│   ├── ui/                # Flet UI components
│   │   ├── __init__.py
│   │   ├── pages/
│   │   │   ├── __init__.py
│   │   │   ├── login.py
│   │   │   ├── signup.py
│   │   │   ├── dashboard.py
│   │   │   ├── transactions.py
│   │   │   └── insights.py
│   │   └── components/
│   │       ├── __init__.py
│   │       ├── navbar.py
│   │       └── charts.py
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── config.py
└── assets/                # Images, icons, etc.
```

## 🎯 Development Roadmap

### Phase 1: Core Setup (Day 1)
- [x] Project structure
- [ ] Basic authentication UI
- [ ] Supabase integration
- [ ] Landing page

### Phase 2: Features (Day 2)
- [ ] Transaction management
- [ ] CSV import functionality
- [ ] Budget categories
- [ ] Basic charts

### Phase 3: Polish & Deploy
- [ ] AI insights integration
- [ ] Plaid integration (optional)
- [ ] Deploy to Render
- [ ] Mobile testing

## 📚 Resources

- [Flet Documentation](https://flet.dev/docs/)
- [Supabase Docs](https://supabase.com/docs)
- [Claude API](https://docs.anthropic.com/)
- [Plaid Quickstart](https://plaid.com/docs/quickstart/)

## 🤝 Contributing

This is a hackathon project! Feel free to fork and improve.

## 📝 License

MIT License - feel free to use for your own projects!
