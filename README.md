# Big $hot 🐍

A personal finance manager with Randy, your friendly budget-tracking snake companion! Built for RowdyHacks.

## Features

- 🐍 Randy: Your virtual pet that reacts to your financial health
-  Transaction tracking and categorization
-  Bank account integration via Plaid
-  Monthly summaries and insights
-  Modern UI with Flet framework
-  FastAPI backend with Supabase database


### SneakPeak
#### Dashboard
<img width="2553" height="1331" alt="image" src="https://github.com/user-attachments/assets/2a82c541-ab4c-4409-b62d-037978b6c35c" />

FUNCTIONAL --> Import CSV, Plaid Integration, Connect to bank, Manual Transaction Handling.

#### Randy Page
![image](https://github.com/user-attachments/assets/1b0ab624-5d7c-4ec0-835b-ba5dc04f6df2)


#### Budget Page
![Screenshot_2025-10-26_at_11 26 44_AM](https://github.com/user-attachments/assets/801b06a9-cc13-475c-8b57-fa4ea0d4e8ca)
![Screenshot_2025-10-26_at_11 28 32_AM](https://github.com/user-attachments/assets/61fd80c2-b24d-40cc-bf35-2cb672fd5eb8)
![Screenshot_2025-10-26_at_11 25 45_AM](https://github.com/user-attachments/assets/081cbcec-973e-41ac-acad-62db7b679ec4)

#### Brand Leaderboard
<img width="2558" height="1333" alt="image" src="https://github.com/user-attachments/assets/2b623894-fbfb-45a1-9d07-ac3386c63a73" />

#### Plaid Integration
![Screenshot_2025-10-26_at_11 23 25_AM](https://github.com/user-attachments/assets/5e1ddcaa-c056-448e-a625-10bb26a6572e)

### Prerequisites

- Python 3.11 or higher
- Virtual environment (recommended)
- Supabase account
- Plaid developer account
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
- AI Insights: Claude/OpenAI API (Not Yet Implemented)

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

- Fernanda Garza Gonzalez
- Sneha 
- Perfect
- Emily
