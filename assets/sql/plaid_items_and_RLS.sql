-- Create plaid_items table to store bank connections
CREATE TABLE IF NOT EXISTS plaid_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    access_token TEXT NOT NULL,
    item_id TEXT NOT NULL,
    institution_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_synced_at TIMESTAMP WITH TIME ZONE
);

-- Disable RLS for now (you can add policies later)
ALTER TABLE plaid_items DISABLE ROW LEVEL SECURITY;

-- Create index for faster lookups
CREATE INDEX idx_plaid_items_user_id ON plaid_items(user_id);
