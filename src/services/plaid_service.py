"""Plaid service for bank integration"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from ..utils.config import Config


class PlaidService:
    """Service for Plaid bank integration"""
    
    def __init__(self):
        """Initialize Plaid service"""
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Plaid client"""
        try:
            import plaid
            from plaid.api import plaid_api
            
            if Config.PLAID_CLIENT_ID and Config.PLAID_SECRET:
                configuration = plaid.Configuration(
                    host=self._get_plaid_host(),
                    api_key={
                        'clientId': Config.PLAID_CLIENT_ID,
                        'secret': Config.PLAID_SECRET,
                    }
                )
                api_client = plaid.ApiClient(configuration)
                self.client = plaid_api.PlaidApi(api_client)
                print("✅ Plaid connected successfully!")
            else:
                print("⚠️ Plaid credentials not configured")
        except ImportError:
            print("⚠️ plaid-python not installed. Run: pip install plaid-python")
        except Exception as e:
            print(f"⚠️ Plaid initialization error: {e}")
    
    def _get_plaid_host(self):
        """Get Plaid API host based on environment"""
        import plaid
        
        env = Config.PLAID_ENV.lower()
        if env == 'sandbox':
            return plaid.Environment.Sandbox
        elif env == 'development':
            return plaid.Environment.Development
        else:
            return plaid.Environment.Production
    
    async def create_link_token(self, user_id: str) -> Optional[str]:
        """Create a Link token for Plaid Link UI"""
        if not self.client:
            print("❌ Plaid client not initialized")
            return None
        
        try:
            import plaid
            from plaid.model.link_token_create_request import LinkTokenCreateRequest
            from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
            from plaid.model.products import Products
            from plaid.model.country_code import CountryCode
            
            request = LinkTokenCreateRequest(
                user=LinkTokenCreateRequestUser(client_user_id=user_id),
                client_name="Budget Buddy",
                products=[Products("transactions")],
                country_codes=[CountryCode("US")],
                language="en"
            )
            
            response = self.client.link_token_create(request)
            print(f"✅ Link token created successfully")
            return response['link_token']
        except Exception as e:
            print(f"❌ Error creating link token: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def exchange_public_token(self, public_token: str) -> Optional[str]:
        """Exchange public token for access token"""
        if not self.client:
            return None
        
        try:
            from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
            
            request = ItemPublicTokenExchangeRequest(public_token=public_token)
            response = self.client.item_public_token_exchange(request)
            return response['access_token']
        except Exception as e:
            print(f"Error exchanging token: {e}")
            return None
    
    async def get_transactions(self, access_token: str, start_date: datetime, 
                              end_date: datetime) -> List[Dict]:
        """Fetch transactions from Plaid"""
        if not self.client:
            return []
        
        try:
            from plaid.model.transactions_get_request import TransactionsGetRequest
            
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date.date(),
                end_date=end_date.date()
            )
            
            response = self.client.transactions_get(request)
            transactions = response['transactions']
            
            # Transform to our format
            return [self._transform_transaction(txn) for txn in transactions]
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    def _transform_transaction(self, plaid_txn: Dict) -> Dict:
        """Transform Plaid transaction to our format"""
        # Plaid: positive amount = money out (expense)
        # Our format: income vs expense type
        amount = abs(plaid_txn['amount'])
        transaction_type = 'expense' if plaid_txn['amount'] > 0 else 'income'
        
        # Get category
        categories = plaid_txn.get('category', [])
        category = categories[0] if categories else 'Other'
        
        return {
            'description': plaid_txn['name'],
            'amount': amount,
            'transaction_type': transaction_type,
            'category': category,
            'transaction_date': plaid_txn['date'],
            'external_id': plaid_txn['transaction_id'],
            'pending': plaid_txn.get('pending', False)
        }
    
    async def sync_transactions(self, access_token: str, user_id: str, 
                               transaction_service) -> int:
        """Sync transactions from Plaid to database"""
        if not self.client:
            return 0
        
        try:
            # Get last 30 days of transactions
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            plaid_transactions = await self.get_transactions(
                access_token, start_date, end_date
            )
            
            # Import to database
            count = 0
            for txn in plaid_transactions:
                # Skip pending transactions
                if txn.get('pending'):
                    continue
                
                # Add to database
                success = await transaction_service.add_transaction(
                    user_id=user_id,
                    amount=txn['amount'],
                    transaction_type=txn['transaction_type'],
                    category=txn['category'],
                    description=txn['description'],
                    date=datetime.fromisoformat(txn['transaction_date'])
                )
                
                if success:
                    count += 1
            
            print(f"✅ Synced {count} transactions from Plaid")
            return count
        except Exception as e:
            print(f"Error syncing transactions: {e}")
            return 0
