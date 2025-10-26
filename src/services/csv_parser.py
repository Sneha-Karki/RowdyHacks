"""CSV parser for importing bank statements"""

import pandas as pd
from typing import List, Dict, Any
from datetime import datetime


class CSVParser:
    """Parse CSV files from various bank formats"""
    
    @staticmethod
    def parse_generic_csv(file_path: str) -> List[Dict[str, Any]]:
        """
        Parse a generic CSV file with transactions
        
        Expected columns: date, description, amount, type, category, user_id (optional)
        
        Returns:
            List of transaction dictionaries
        """
        try:
            df = pd.read_csv(file_path)
            
            # Try to standardize column names
            column_mapping = {
                'date': ['date', 'transaction date', 'posted date', 'transaction_date'],
                'description': ['description', 'merchant', 'payee', 'name'],
                'amount': ['amount', 'debit', 'credit'],
                'type': ['type', 'transaction_type', 'transaction type'],
                'category': ['category', 'Category'],
                'user_id': ['user_id', 'user', 'User ID']
            }
            
            # Find matching columns
            standardized = {}
            for standard_name, possible_names in column_mapping.items():
                for col in df.columns:
                    if col.lower() in [n.lower() for n in possible_names]:
                        standardized[standard_name] = col
                        break
            
            if 'date' not in standardized or 'amount' not in standardized:
                raise ValueError("CSV must contain 'date' and 'amount' columns")
            
            # Parse transactions
            transactions = []
            for _, row in df.iterrows():
                amount = float(row[standardized['amount']])
                
                # Determine transaction type
                if 'type' in standardized:
                    txn_type = str(row[standardized['type']]).lower()
                else:
                    # Infer from amount
                    txn_type = 'income' if amount > 0 else 'expense'
                
                transaction = {
                    'date': str(row[standardized['date']]),
                    'description': str(row[standardized.get('description', '')]) if 'description' in standardized else 'Unknown',
                    'amount': abs(amount),  # Always positive
                    'transaction_type': txn_type,
                    'category': str(row[standardized.get('category', '')]) if 'category' in standardized else 'Uncategorized',
                    'user_id': str(row[standardized.get('user_id', '')]) if 'user_id' in standardized else None
                }
                transactions.append(transaction)
            
            return transactions
            
        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {str(e)}")
    
    @staticmethod
    def get_summary(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics from transactions"""
        if not transactions:
            return {
                'total_transactions': 0,
                'total_income': 0,
                'total_expenses': 0,
                'net': 0
            }
        
        total_income = sum(t['amount'] for t in transactions if t['amount'] > 0)
        total_expenses = sum(abs(t['amount']) for t in transactions if t['amount'] < 0)
        
        return {
            'total_transactions': len(transactions),
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net': total_income - total_expenses
        }
