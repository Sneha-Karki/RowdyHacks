# 🚀 Deployment Guide - Budget Buddy

## Table of Contents
1. [Supabase Setup](#supabase-setup)
2. [Local Development](#local-development)
3. [Deploy to Render](#deploy-to-render)
4. [Optional Integrations](#optional-integrations)

---

## Supabase Setup

### Step 1: Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Create a new organization (free)
4. Create a new project:
   - Name: `budget-buddy`
   - Database Password: (save this!)
   - Region: Choose closest to you

### Step 2: Get Your Credentials
1. In your project dashboard, click "Settings" → "API"
2. Copy these values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public key** (starts with `eyJ...`)

### Step 3: Create Database Tables

Run this SQL in the SQL Editor (Database → SQL Editor):

```sql
-- Users table (handled by Supabase Auth automatically)

-- Transactions table
CREATE TABLE transactions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  description TEXT NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  category TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Budget categories table
CREATE TABLE budget_categories (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  monthly_limit DECIMAL(10, 2),
  color TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget_categories ENABLE ROW LEVEL SECURITY;

-- Policies for transactions
CREATE POLICY "Users can view own transactions"
  ON transactions FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own transactions"
  ON transactions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own transactions"
  ON transactions FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own transactions"
  ON transactions FOR DELETE
  USING (auth.uid() = user_id);

-- Policies for budget_categories
CREATE POLICY "Users can view own categories"
  ON budget_categories FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own categories"
  ON budget_categories FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own categories"
  ON budget_categories FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own categories"
  ON budget_categories FOR DELETE
  USING (auth.uid() = user_id);
```

### Step 4: Configure .env File

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and add your Supabase credentials:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

---

## Local Development

### Run the Application

```bash
# Make sure you're in the project directory
cd c:\dev

# Run in desktop mode (recommended for development)
python main.py

# Or run in web browser mode
flet run main.py --web --port 8080
```

The app will open automatically!

---

## Deploy to Render

### Option 1: Deploy Web Version (Recommended for Hackathon)

1. **Create a Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Budget Buddy"
   git remote add origin https://github.com/yourusername/budget-buddy.git
   git push -u origin main
   ```

3. **Create Web Service on Render**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name**: `budget-buddy`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `flet run main.py --web --port $PORT`
     - **Plan**: Free

4. **Add Environment Variables**
   In Render dashboard → Environment:
   ```
   SUPABASE_URL=your-url
   SUPABASE_KEY=your-key
   CLAUDE_API_KEY=your-claude-key (optional)
   ```

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your app will be live at `https://budget-buddy.onrender.com`

### Option 2: Deploy as Desktop App (Advanced)

Package with PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

Executable will be in `dist/` folder.

---

## Optional Integrations

### Claude AI Setup

1. Get API key from [console.anthropic.com](https://console.anthropic.com)
2. Add to `.env`:
   ```env
   CLAUDE_API_KEY=sk-ant-api03-...
   ```
3. Restart the app

### Plaid Bank Integration (Future Feature)

1. Sign up at [dashboard.plaid.com](https://dashboard.plaid.com)
2. Get Sandbox credentials
3. Add to `.env`:
   ```env
   PLAID_CLIENT_ID=your-client-id
   PLAID_SECRET=your-sandbox-secret
   PLAID_ENV=sandbox
   ```

---

## Testing the App

### Test User Flow
1. ✅ Sign up with email/password
2. ✅ Check email for verification (Supabase sends automatically)
3. ✅ Sign in
4. ✅ View dashboard
5. ✅ Add manual transactions
6. ✅ Import CSV file
7. ✅ View AI insights

### Sample CSV Format
Create a file `sample_transactions.csv`:
```csv
Date,Description,Amount,Category
2024-01-15,Grocery Store,-125.50,Food
2024-01-16,Salary Deposit,3200.00,Income
2024-01-17,Electric Bill,-89.00,Utilities
2024-01-18,Coffee Shop,-15.75,Food
```

---

## Troubleshooting

### Issue: "Authentication service not configured"
**Solution**: Make sure `.env` file has correct Supabase credentials

### Issue: "Module not found"
**Solution**: Install requirements:
```bash
pip install -r requirements.txt
```

### Issue: Port already in use
**Solution**: Use a different port:
```bash
flet run main.py --web --port 8081
```

### Issue: Render deployment fails
**Solution**: Check Build Logs in Render dashboard. Common fixes:
- Ensure `requirements.txt` is in root directory
- Verify Python version compatibility
- Check environment variables are set

---

## Next Steps for Hackathon

### Phase 1 (First 6 hours) ✅
- [x] Project setup
- [x] Basic UI with Flet
- [x] Supabase authentication
- [x] Dashboard layout

### Phase 2 (Next 6 hours)
- [ ] Transaction CRUD operations
- [ ] CSV import functionality
- [ ] Budget categories
- [ ] Charts and visualizations

### Phase 3 (Next 6 hours)
- [ ] AI insights integration
- [ ] Polish UI/UX
- [ ] Mobile responsive design
- [ ] Error handling

### Phase 4 (Final 6 hours)
- [ ] Deploy to Render
- [ ] Testing on multiple devices
- [ ] Documentation
- [ ] Demo video/presentation

---

## Resources

- **Flet Docs**: https://flet.dev/docs/
- **Supabase Docs**: https://supabase.com/docs
- **Claude API**: https://docs.anthropic.com/
- **Render Docs**: https://render.com/docs

---

## Support

Questions? Check the code comments or reach out to the team!

**Good luck with your hackathon! 🚀**
