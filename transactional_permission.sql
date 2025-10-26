-- Check if table exists and structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'transactions'
ORDER BY ordinal_position;

-- Check RLS policies
SELECT * FROM pg_policies WHERE tablename = 'transactions';

-- Try manual insert to test permissions
INSERT INTO transactions (user_id, amount, transaction_type, category, description, transaction_date)
VALUES ('2bb0cf57-8075-425c-a361-881247857a51', 100.00, 'income', 'Test', 'Manual test', NOW());
