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
            self.supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    
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
            # Get all transactions for the month
            response = self.supabase.table('transactions')\
                .select('amount, transaction_type')\
                .eq('user_id', user_id)\
                .gte('transaction_date', f'{year}-{month:02d}-01')\
                .lt('transaction_date', f'{year}-{month+1 if month < 12 else 1:02d}-01')\
                .execute()
            
            transactions = response.data if response.data else []
            
            income = sum(t['amount'] for t in transactions if t['transaction_type'] == 'income')
            expenses = sum(t['amount'] for t in transactions if t['transaction_type'] == 'expense')
            
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
    
    async def add_transaction(self, user_id: str, amount: float, 
                            transaction_type: str, category: str, 
                            description: str, date: datetime) -> bool:
        """Add a new transaction"""
        if not self.supabase:
            print("❌ Error: Supabase not configured")
            return False
        
        try:
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
