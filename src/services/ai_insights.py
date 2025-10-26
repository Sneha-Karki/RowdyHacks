"""AI-powered insights using Claude or local LLM"""

from typing import List, Dict, Any, Optional
from src.utils.config import Config

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class AIInsightsService:
    """Generate financial insights using AI"""
    
    def __init__(self):
        self.client = None
        if ANTHROPIC_AVAILABLE and Config.CLAUDE_API_KEY:
            try:
                self.client = Anthropic(api_key=Config.CLAUDE_API_KEY)
            except:
                pass
    
    def analyze_spending(self, transactions: List[Dict[str, Any]]) -> str:
        """
        Analyze spending patterns and provide insights
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            AI-generated insights as a string
        """
        if not self.client:
            return self._generate_basic_insights(transactions)
        
        try:
            # Prepare transaction summary for AI
            summary = self._prepare_transaction_summary(transactions)
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"""Analyze these financial transactions and provide helpful insights:

{summary}

Please provide:
1. Key spending patterns
2. Budget recommendations
3. Areas to save money
4. Overall financial health assessment

Keep it concise and actionable."""
                }]
            )
            
            return message.content[0].text
            
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"
    
    def _prepare_transaction_summary(self, transactions: List[Dict[str, Any]]) -> str:
        """Prepare transaction data for AI analysis"""
        if not transactions:
            return "No transactions available"
        
        # Group by category
        by_category = {}
        total_income = 0
        total_expenses = 0
        
        for t in transactions:
            category = t.get('category', 'Uncategorized')
            amount = t.get('amount', 0)
            
            if amount > 0:
                total_income += amount
            else:
                total_expenses += abs(amount)
                
            if category not in by_category:
                by_category[category] = 0
            by_category[category] += abs(amount)
        
        summary = f"Total Income: ${total_income:.2f}\n"
        summary += f"Total Expenses: ${total_expenses:.2f}\n"
        summary += f"Net: ${total_income - total_expenses:.2f}\n\n"
        summary += "Spending by Category:\n"
        
        for category, amount in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            summary += f"  - {category}: ${amount:.2f}\n"
        
        return summary
    
    def _generate_basic_insights(self, transactions: List[Dict[str, Any]]) -> str:
        """Generate basic insights without AI"""
        if not transactions:
            return "No transaction data available for analysis."
        
        # Calculate basic stats
        total_income = sum(t['amount'] for t in transactions if t['amount'] > 0)
        total_expenses = sum(abs(t['amount']) for t in transactions if t['amount'] < 0)
        net = total_income - total_expenses
        
        # Group by category
        by_category = {}
        for t in transactions:
            category = t.get('category', 'Uncategorized')
            amount = abs(t.get('amount', 0))
            by_category[category] = by_category.get(category, 0) + amount
        
        # Find top spending category
        top_category = max(by_category.items(), key=lambda x: x[1]) if by_category else ('None', 0)
        
        insights = f"""📊 Financial Summary

💰 Total Income: ${total_income:.2f}
💸 Total Expenses: ${total_expenses:.2f}
📈 Net: ${net:.2f}

🎯 Top Spending Category: {top_category[0]} (${top_category[1]:.2f})

💡 Basic Insights:
• Savings Rate: {(net / total_income * 100) if total_income > 0 else 0:.1f}%
• Transaction Count: {len(transactions)}
• Average Transaction: ${(total_expenses / len(transactions)) if transactions else 0:.2f}

⚠️ Note: Enable Claude API in .env for AI-powered insights!
"""
        return insights
