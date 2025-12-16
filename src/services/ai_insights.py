from typing import List, Dict, Any
from src.utils.config import Config
from openai import OpenAI

class AIInsightsService:
    """Generate financial insights using OpenAI"""

    def __init__(self):
        self.client = None
        if Config.OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
                print("OpenAI client initialized successfully.")
            except Exception as e:
                print(f"OpenAI init error: {e}")
                self.client = None

    def analyze_spending(self, transactions: List[Dict[str, Any]]) -> str:
        """Analyze spending patterns using OpenAI with friendly, advanced tone."""
        if not transactions:
            return "No transaction data available for analysis."

        summary = self._prepare_transaction_summary(transactions)

        if not self.client:
            return self._generate_basic_insights(transactions)

        prompt = f"""
Analyze these financial transactions and provide helpful insights:

{summary}

Please provide:
1. Key spending patterns
2. Budget recommendations
3. Areas to save money
4. Overall financial health assessment

Keep it concise, friendly, and actionable.
"""

        # Friendly examples to guide tone
        examples = [
            {"role": "user", "content": "Text: 'Housing cost $4,800, food $2,533, transportation $1,179.'\nSummary: 'You’re doing well managing your major expenses. Housing and food are the largest costs, so small adjustments in dining habits or housing efficiency could free up extra cash for savings or fun activities.'"},
            {"role": "user", "content": "Text: 'Net income $34,499.'\nSummary: 'Fantastic! Your net income is strong. Consider allocating a portion to an emergency fund or investments to strengthen financial stability and future-proof your finances.'"}
        ]

        def _try_model(model_name: str) -> str | None:
            try:
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a financial assistant that provides professional, friendly, and actionable insights. Use approachable language and advanced vocabulary when appropriate. Avoid markdown formatting."}
                    ] + examples + [{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=700
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI call error for model {model_name}: {e}")
                return None

        # Try models in order
        for model in ("gpt-4o-mini", "gpt-3.5-turbo", "gpt-3.5-turbo-0125"):
            content = _try_model(model)
            if content:
                print(f"OpenAI returned content from model {model}: {content[:200]}...")
                return content

        # Fallback
        print("OpenAI did not return usable content; using fallback.")
        return f"⚠️ OpenAI analysis unavailable, showing fallback insights below.\n\n{self._generate_basic_insights(transactions)}"

    def _prepare_transaction_summary(self, transactions: List[Dict[str, Any]]) -> str:
        """Prepare transaction data for AI analysis"""
        if not transactions:
            return "No transactions available"

        by_category = {}
        total_income = 0
        total_expenses = 0

        for t in transactions:
            category = t.get("category", "Uncategorized")
            amount = t.get("amount", 0)

            if amount > 0:
                total_income += amount
            else:
                total_expenses += abs(amount)

            by_category[category] = by_category.get(category, 0) + abs(amount)

        summary = (
            f"Total Income: ${total_income:.2f}\n"
            f"Total Expenses: ${total_expenses:.2f}\n"
            f"Net: ${total_income - total_expenses:.2f}\n\n"
            "Spending by Category:\n"
        )

        for category, amount in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            summary += f"  - {category}: ${amount:.2f}\n"

        return summary

    def _generate_basic_insights(self, transactions: List[Dict[str, Any]]) -> str:
        """Fallback insights if OpenAI is unavailable"""
        total_income = sum(t["amount"] for t in transactions if t["amount"] > 0)
        total_expenses = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
        net = total_income - total_expenses

        by_category = {}
        for t in transactions:
            category = t.get("category", "Uncategorized")
            amount = abs(t.get("amount", 0))
            by_category[category] = by_category.get(category, 0) + amount

        top_category = max(by_category.items(), key=lambda x: x[1]) if by_category else ("None", 0)

        # Friendly, narrative-style fallback
        return f"""
Hello! Here's a quick look at your finances:

💰 Total Income: ${total_income:.2f}
💸 Total Expenses: ${total_expenses:.2f}
📈 Net Savings: ${net:.2f}

Your largest spending category is {top_category[0]} (${top_category[1]:.2f}).

Quick tips:
- Keep an eye on your top spending categories and consider small adjustments to save more.
- Your savings rate is {(net / total_income * 100) if total_income > 0 else 0:.1f}% — good start!
- Track your transactions regularly to stay on top of your budget.

Even without AI, these insights can help you plan smarter and save effectively.
"""