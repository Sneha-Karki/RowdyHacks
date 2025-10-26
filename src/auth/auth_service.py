"""Authentication service using Supabase"""

from typing import Optional, Dict, Any
from supabase import create_client, Client
from src.utils.config import Config


class AuthService:
    """Handles user authentication with Supabase"""
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.current_user: Optional[Dict[str, Any]] = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Supabase client"""
        if Config.is_configured():
            try:
                self.supabase = create_client(
                    Config.SUPABASE_URL,
                    Config.SUPABASE_KEY
                )
                print("Supabase connected successfully!")
            except Exception as e:
                print(f"Failed to initialize Supabase: {e}")
        else:
            print("Supabase credentials not found in .env file. Running in demo mode.")
    
    async def sign_up(self, email: str, password: str) -> tuple[bool, str]:
        """
        Register a new user
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.supabase:
            return False, "Authentication service not configured"
        
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                return True, "Account created successfully! Please check your email to verify."
            return False, "Failed to create account"
            
        except Exception as e:
            return False, f"Sign up error: {str(e)}"
    
    async def sign_in(self, email: str, password: str) -> tuple[bool, str]:
        """
        Sign in an existing user
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.supabase:
            return False, "Authentication service not configured"
        
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                self.current_user = response.user
                return True, "Successfully signed in!"
            return False, "Invalid credentials"
            
        except Exception as e:
            return False, f"Sign in error: {str(e)}"
    
    async def sign_out(self) -> tuple[bool, str]:
        """Sign out the current user"""
        if not self.supabase:
            return False, "Authentication service not configured"
        
        try:
            self.supabase.auth.sign_out()
            self.current_user = None
            return True, "Signed out successfully"
        except Exception as e:
            return False, f"Sign out error: {str(e)}"
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get the currently authenticated user"""
        if not self.supabase:
            return None
        
        try:
            user = self.supabase.auth.get_user()
            return user
        except:
            return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
