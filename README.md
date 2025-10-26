# Big $hot 🐍

A personal finance manager with Randy, your friendly budget-tracking snake companion! Built for RowdyHacks.

## Features

- 🐍 Randy: Your virtual pet that reacts to your financial health
- 📊 Transaction tracking and categorization
- 🏦 Bank account integration via Plaid
- 📈 Monthly summaries and insights
- 📱 Modern UI with Flet framework
- 🚀 FastAPI backend with Supabase database

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Virtual environment (recommended)
- Supabase account
- (Optional) Plaid developer account
- (Optional) Claude or OpenAI API key for AI insights

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Sneha-Karki/RowdyHacks.git
cd RowdyHacks
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Configuration

1. Supabase setup (Required):
   - Create a project at https://supabase.com
   - Add your project URL and anon key to `.env`

2. Plaid setup (Optional):
   - Get API credentials from https://plaid.com/docs/api/
   - Add Plaid credentials to `.env`

3. AI setup (Optional):
   - Get API key from Anthropic (Claude) or OpenAI
   - Add to `.env`

### Running the Application

1. Start the FastAPI backend:
```bash
python api.py
```

2. In another terminal, start the Flet frontend:
```bash
python main.py
```

The application will open in your default web browser.

## Architecture

- Frontend: Flet (Python UI framework)
- Backend: FastAPI with async support
- Database: Supabase (PostgreSQL)
- Bank Integration: Plaid API
- AI Insights: Claude/OpenAI API

## Project Structure

```
RowdyHacks/
├── api.py              # FastAPI backend
├── main.py            # Flet frontend
├── requirements.txt   # Python dependencies
├── src/
│   ├── auth/         # Authentication services
│   ├── database/     # Database operations
│   ├── services/     # API clients and services
│   ├── ui/          # Frontend components
│   └── utils/       # Shared utilities
└── assets/         # Static assets
```

## Contributing

1. Create a feature branch:
```bash
git checkout -b feature-name
```

2. Make your changes and commit:
```bash
git commit -m "Description of changes"
```

3. Push to your branch:
```bash
git push origin feature-name
```

4. Create a Pull Request on GitHub

## Team

- Fernanda Garza
- Sneha Kharki
- Emily Steinmetz
- Perfect Sylvester
