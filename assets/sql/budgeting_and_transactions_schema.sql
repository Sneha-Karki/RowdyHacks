-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (Supabase Auth handles this automatically)

-- Budgets table
CREATE TABLE budgets (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    period VARCHAR(20) DEFAULT 'monthly',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transactions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    budget_id UUID REFERENCES budgets(id) ON DELETE CASCADE,
    description TEXT,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    transaction_date DATE NOT NULL,
    type VARCHAR(20) CHECK (type IN ('income', 'expense')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- CSV Imports table (track uploaded files)
CREATE TABLE csv_imports (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    filename VARCHAR(255),
    row_count INTEGER,
    imported_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_budgets_user_id ON budgets(user_id);
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_budget_id ON transactions(budget_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);

-- Enable Row Level Security (RLS)
ALTER TABLE budgets ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE csv_imports ENABLE ROW LEVEL SECURITY;

-- RLS Policies: Users can only see their own data
CREATE POLICY "Users can view own budgets" ON budgets
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own budgets" ON budgets
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own budgets" ON budgets
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own budgets" ON budgets
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own transactions" ON transactions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own transactions" ON transactions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own transactions" ON transactions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own transactions" ON transactions
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own imports" ON csv_imports
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own imports" ON csv_imports
    FOR INSERT WITH CHECK (auth.uid() = user_id);
