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
        
        Expected columns: Date, Description, Amount, Category (optional)
        
        Returns:
            List of transaction dictionaries
        """
        try:
            df = pd.read_csv(file_path)
            
            # Try to standardize column names
            column_mapping = {
                'date': ['date', 'transaction date', 'posted date', 'Date'],
                'description': ['description', 'merchant', 'payee', 'Description'],
                'amount': ['amount', 'debit', 'credit', 'Amount'],
                'category': ['category', 'type', 'Category']
            }
            
            # Find matching columns
            standardized = {}
            for standard_name, possible_names in column_mapping.items():
                for col in df.columns:
                    if col.lower() in [n.lower() for n in possible_names]:
                        standardized[standard_name] = col
                        break
            
            if 'date' not in standardized or 'amount' not in standardized:
                raise ValueError("CSV must contain Date and Amount columns")
            
            # Parse transactions
            transactions = []
            for _, row in df.iterrows():
                transaction = {
                    'date': str(row[standardized['date']]),
                    'description': str(row[standardized.get('description', '')]) if 'description' in standardized else 'Unknown',
                    'amount': float(row[standardized['amount']]),
                    'category': str(row[standardized.get('category', '')]) if 'category' in standardized else 'Uncategorized'
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
