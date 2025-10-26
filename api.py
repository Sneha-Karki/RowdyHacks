"""FastAPI backend for Budget Buddy"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from typing import List, Dict
import pandas as pd
from datetime import datetime
import io

# Import your existing services
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.database.transaction_service import TransactionService
from src.services.plaid_service import PlaidService
from src.utils.config import Config

app = FastAPI(title="Budget Buddy API", version="1.0.0")

# CORS middleware (allows Flet to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
transaction_service = TransactionService()
plaid_service = PlaidService()


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "app": "Budget Buddy API",
        "supabase_configured": Config.is_configured()
    }


@app.get("/plaid-link")
async def serve_plaid_link():
    """Serve Plaid Link HTML page"""
    html_path = os.path.join(os.getcwd(), 'assets', 'plaid_link.html')
    return FileResponse(html_path, media_type="text/html")


@app.post("/api/csv/upload")
async def upload_csv(file: UploadFile = File(...), user_id: str = "demo"):
    """
    Upload and process CSV file
    
    Expected CSV columns: user_id, date, description, amount, type, category
    """
    try:
        # Read file content
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        print(f"📊 Received CSV with {len(df)} rows")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Validate required columns
        required_cols = ['date', 'description', 'amount', 'type', 'category']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise HTTPException(400, f"Missing columns: {missing}")
        
        # Process transactions
        imported = 0
        skipped = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                amount = float(row['amount'])
                txn_type = str(row['type']).lower().strip()
                
                # ALWAYS use the logged-in user's ID (ignore CSV user_id)
                # This ties all transactions to whoever uploads the file
                
                # Parse date
                try:
                    date = datetime.strptime(str(row['date']), '%Y-%m-%d')
                except:
                    date = datetime.now()
                
                # Add transaction
                success = await transaction_service.add_transaction(
                    user_id=user_id,  # Use the logged-in user ID
                    amount=abs(amount),
                    transaction_type=txn_type,
                    category=str(row['category']),
                    description=str(row['description']),
                    date=date
                )
                
                if success:
                    imported += 1
                else:
                    skipped += 1
                    
            except Exception as e:
                skipped += 1
                errors.append(f"Row {index + 2}: {str(e)}")
        
        return {
            "success": True,
            "imported": imported,
            "skipped": skipped,
            "total": len(df),
            "errors": errors[:5]  # Return first 5 errors
        }
        
    except Exception as e:
        print(f"❌ CSV Upload Error: {e}")
        raise HTTPException(500, f"Failed to process CSV: {str(e)}")


@app.post("/api/plaid/create-link-token")
async def create_plaid_link_token(user_id: str = "demo"):
    """Create Plaid Link token for bank connection"""
    try:
        link_token = await plaid_service.create_link_token(user_id)
        
        if link_token:
            return {
                "success": True,
                "link_token": link_token
            }
        else:
            raise HTTPException(500, "Failed to create Plaid link token")
            
    except Exception as e:
        print(f"❌ Plaid Error: {e}")
        raise HTTPException(500, str(e))


@app.post("/api/plaid/exchange-token")
async def exchange_plaid_token(public_token: str):
    """Exchange Plaid public token for access token"""
    try:
        access_token = await plaid_service.exchange_public_token(public_token)
        
        if access_token:
            return {
                "success": True,
                "access_token": access_token
            }
        else:
            raise HTTPException(500, "Failed to exchange token")
            
    except Exception as e:
        print(f"❌ Plaid Token Exchange Error: {e}")
        raise HTTPException(500, str(e))


@app.get("/api/transactions")
async def get_transactions(user_id: str = "demo", limit: int = 10):
    """Get user transactions"""
    try:
        transactions = await transaction_service.get_user_transactions(user_id, limit)
        return {
            "success": True,
            "transactions": transactions
        }
    except Exception as e:
        print(f"❌ Get Transactions Error: {e}")
        raise HTTPException(500, str(e))


@app.get("/api/summary")
async def get_summary(user_id: str = "demo"):
    """Get monthly summary"""
    try:
        now = datetime.now()
        summary = await transaction_service.get_monthly_summary(user_id, now.year, now.month)
        balance = await transaction_service.get_total_balance(user_id)
        
        return {
            "success": True,
            "balance": balance,
            "summary": summary
        }
    except Exception as e:
        print(f"❌ Get Summary Error: {e}")
        raise HTTPException(500, str(e))


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Budget Buddy API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
