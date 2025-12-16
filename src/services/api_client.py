"""API Client for communicating with FastAPI backend"""

import os
import requests
from typing import Dict, List, Optional, BinaryIO
from datetime import datetime


class APIClient:
    """Client for Budget Buddy FastAPI backend"""
    
    def __init__(self, base_url: str = None):
        """Initialize API client

        By default the client will read the API base URL from the environment
        variable API_BASE_URL. If that isn't set, it falls back to
        http://localhost:8000 for local development.
        """
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        self.session = requests.Session()
    
    def health_check(self) -> bool:
        """Check if API is running"""
        try:
            response = self.session.get(f"{self.base_url}/")
            return response.status_code == 200
        except:
            return False
    
    async def upload_csv(self, file_path: str, user_id: str) -> Dict:
        """
        Upload CSV file to API for processing
        
        Args:
            file_path: Path to CSV file
            user_id: User ID for transactions
            
        Returns:
            Dict with import results
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.split('/')[-1], f, 'text/csv')}
                params = {'user_id': user_id}
                
                response = self.session.post(
                    f"{self.base_url}/api/csv/upload",
                    files=files,
                    params=params,
                    timeout=60
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "success": False,
                        "error": f"API returned {response.status_code}: {response.text}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_plaid_link_token(self, user_id: str) -> Optional[str]:
        """
        Create Plaid Link token
        
        Args:
            user_id: User ID
            
        Returns:
            Link token or None if failed
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/plaid/create-link-token",
                params={'user_id': user_id},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('link_token')
            else:
                print(f"❌ Plaid API error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Plaid API exception: {e}")
            return None
    
    async def exchange_plaid_token(self, public_token: str) -> Optional[str]:
        """
        Exchange Plaid public token for access token
        
        Args:
            public_token: Public token from Plaid Link
            
        Returns:
            Access token or None if failed
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/plaid/exchange-token",
                json={'public_token': public_token},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('access_token')
            else:
                return None
        except Exception as e:
            print(f"❌ Token exchange error: {e}")
            return None
    
    async def get_transactions(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Get user transactions from API
        
        Args:
            user_id: User ID
            limit: Number of transactions to fetch
            
        Returns:
            List of transactions
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/transactions",
                params={'user_id': user_id, 'limit': limit},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('transactions', [])
            else:
                return []
        except Exception as e:
            print(f"❌ Get transactions error: {e}")
            return []
    
    async def get_summary(self, user_id: str) -> Dict:
        """
        Get balance and monthly summary from API
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with balance and summary
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/summary",
                params={'user_id': user_id},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'balance': data.get('balance', 0),
                    'summary': data.get('summary', {})
                }
            else:
                return {
                    'balance': 0,
                    'summary': {'income': 0, 'expenses': 0, 'savings': 0, 'savings_rate': 0}
                }
        except Exception as e:
            print(f"❌ Get summary error: {e}")
            return {
                'balance': 0,
                'summary': {'income': 0, 'expenses': 0, 'savings': 0, 'savings_rate': 0}
            }

    async def get_ai_insights(self, user_id):
        url = f"{self.base_url}/api/ai-insights?user_id={user_id}"
        return await self._get(url)

    async def _get(self, url: str) -> Dict:
        """Internal helper to perform GET requests and return parsed JSON."""
        try:
            # AI calls can take longer; increase timeout to accommodate model latency
            response = self.session.get(url, timeout=60)
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": f"API returned {response.status_code}: {response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
