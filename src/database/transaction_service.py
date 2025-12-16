"""Transaction service for database operations"""

from typing import List, Dict, Optional
from datetime import datetime
from supabase import Client
from ..utils.config import Config


class TransactionService:
    """Service for managing transactions in Supabase"""
    
    def __init__(self):
        """Initialize transaction service"""
        self.supabase: Optional[Client] = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Supabase connection"""
        if Config.is_configured():
            from supabase import create_client
            # Use service role key for backend operations to bypass RLS
            service_key = Config.SUPABASE_SERVICE_KEY if hasattr(Config, 'SUPABASE_SERVICE_KEY') and Config.SUPABASE_SERVICE_KEY else Config.SUPABASE_KEY
            self.supabase = create_client(Config.SUPABASE_URL, service_key)
    
    async def get_user_transactions(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent transactions for a user"""
        if not self.supabase:
            return []
        
        try:
            response = self.supabase.table('transactions')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('transaction_date', desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    async def get_monthly_summary(self, user_id: str, year: int, month: int) -> Dict:
        """Get monthly income and expense summary"""
        if not self.supabase:
            return {'income': 0, 'expenses': 0, 'savings': 0, 'savings_rate': 0}
        
        try:
            # Calculate next month for date range
            if month == 12:
                next_month = 1
                next_year = year + 1
            else:
                next_month = month + 1
                next_year = year
            
            # Get all transactions for the month
            response = self.supabase.table('transactions')\
                .select('amount, transaction_type, transaction_date')\
                .eq('user_id', user_id)\
                .gte('transaction_date', f'{year}-{month:02d}-01')\
                .lt('transaction_date', f'{next_year}-{next_month:02d}-01')\
                .execute()
            
            transactions = response.data if response.data else []
            
            print(f"📊 Found {len(transactions)} transactions for {year}-{month:02d}")
            
            income = sum(t['amount'] for t in transactions if t['transaction_type'] == 'income')
            expenses = sum(t['amount'] for t in transactions if t['transaction_type'] == 'expense')
            
            # If no data for current month, get all-time data
            if income == 0 and expenses == 0:
                print(f"⚠️ No transactions in {year}-{month:02d}, fetching all-time data...")
                all_response = self.supabase.table('transactions')\
                    .select('amount, transaction_type')\
                    .eq('user_id', user_id)\
                    .execute()
                
                all_transactions = all_response.data if all_response.data else []
                income = sum(t['amount'] for t in all_transactions if t['transaction_type'] == 'income')
                expenses = sum(t['amount'] for t in all_transactions if t['transaction_type'] == 'expense')
                print(f"📊 All-time: Income=${income}, Expenses=${expenses}")
            
            return {
                'income': income,
                'expenses': expenses,
                'savings': income - expenses,
                'savings_rate': (income - expenses) / income * 100 if income > 0 else 0
            }
        except Exception as e:
            print(f"Error fetching monthly summary: {e}")
            return {'income': 0, 'expenses': 0, 'savings': 0, 'savings_rate': 0}
    
    async def get_total_balance(self, user_id: str) -> float:
        """Calculate total balance from all transactions"""
        if not self.supabase:
            return 0.0
        
        try:
            response = self.supabase.table('transactions')\
                .select('amount, transaction_type')\
                .eq('user_id', user_id)\
                .execute()
            
            transactions = response.data if response.data else []
            
            balance = 0
            for t in transactions:
                if t['transaction_type'] == 'income':
                    balance += t['amount']
                else:
                    balance -= t['amount']
            
            return balance
        except Exception as e:
            print(f"Error calculating balance: {e}")
            return 0.0
    
    async def check_duplicate(self, user_id: str, amount: float, 
                            description: str, date: datetime) -> bool:
        """Check if a transaction already exists (to avoid duplicates)"""
        if not self.supabase:
            return False
        
        try:
            # Check for transaction with same user, amount, description, and date
            response = self.supabase.table('transactions')\
                .select('id')\
                .eq('user_id', user_id)\
                .eq('amount', amount)\
                .eq('description', description)\
                .eq('transaction_date', date.isoformat())\
                .execute()
            
            return len(response.data) > 0
        except Exception as e:
            print(f"Error checking duplicate: {e}")
            return False
    
    async def add_transaction(self, user_id: str, amount: float, 
                            transaction_type: str, category: str, 
                            description: str, date: datetime) -> bool:
        """Add a new transaction (with duplicate detection)"""
        if not self.supabase:
            print("❌ Error: Supabase not configured")
            return False
        
        try:
            # Check for duplicates first
            is_duplicate = await self.check_duplicate(user_id, amount, description, date)
            if is_duplicate:
                print(f"⚠️ Duplicate skipped: {description[:30]}...")
                return False
            
            data = {
                'user_id': user_id,
                'amount': amount,
                'transaction_type': transaction_type,
                'category': category,
                'description': description,
                'transaction_date': date.isoformat()
            }
            
            print(f"📤 Inserting transaction: {description[:30]}... for user {user_id[:8]}...")
            response = self.supabase.table('transactions').insert(data).execute()
            print(f"✅ Transaction inserted successfully!")
            return True
        except Exception as e:
            print(f"❌ Error adding transaction: {e}")
            import traceback
            traceback.print_exc()
            return False
