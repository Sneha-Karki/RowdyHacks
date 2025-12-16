"""AI Chat Service for Randy the Financial Advisor Snake"""

import os
from dotenv import load_dotenv

load_dotenv()

# Try to import OpenAI, fallback if not available
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIChatService:
    """Service for interacting with OpenAI as Randy"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and OPENAI_AVAILABLE:
            self.client = AsyncOpenAI(api_key=api_key)
            self.model = "gpt-4o-mini"
            print("✅ AI Chat service initialized with OpenAI API")
        else:
            self.client = None
            self.model = None
            if not OPENAI_AVAILABLE:
                print("⚠️ OpenAI library not installed - using fallback responses")
            else:
                print("⚠️ AI Chat service running without API key - using fallback responses")
    
    async def chat(self, message: str, conversation_history: list = None, user_context: dict = None):
        """
        Send message to OpenAI and get Randy's response
        
        Args:
            message: User's message
            conversation_history: List of previous messages in format [{"role": "user/assistant", "content": "..."}]
            user_context: Optional dict with user's financial data (balance, expenses, etc.)
        
        Returns:
            Randy's response as a string
        """
        # If no API key, use fallback responses
        if not self.client:
            return self._get_fallback_response(message, user_context)
        
        # Build system prompt with Randy's personality
        system_prompt = self._build_system_prompt(user_context)
        
        # Build message history for OpenAI format
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": message})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ AI Chat Error: {e}")
            return self._get_fallback_response(message, user_context)
    
    def _build_system_prompt(self, user_context: dict = None):
        """Build Randy's system prompt with personality and context"""
        base_prompt = """You are Randy, a friendly and wise financial advisor snake! 🐍
        
Your personality:
- You're enthusiastic about helping people manage their money
- You occasionally make snake-related puns and references (but don't overdo it!)
- You're encouraging and supportive, never judgmental
- You give practical, actionable financial advice
- You keep responses concise and conversational

Your expertise:
- Budgeting and expense tracking
- Savings strategies
- Debt management
- Financial goal setting
- Smart spending habits

Guidelines:
- Keep responses under 150 words when possible
- Use emojis occasionally (especially 🐍💰📊)
- Be specific and actionable with advice
- Ask clarifying questions when needed
- Celebrate user's financial wins!"""

        # Add user context if available
        if user_context:
            context_str = "\n\nCurrent user financial snapshot:"
            if 'balance' in user_context:
                context_str += f"\n- Total Balance: ${user_context['balance']:,.2f}"
            if 'income' in user_context:
                context_str += f"\n- Monthly Income: ${user_context['income']:,.2f}"
            if 'expenses' in user_context:
                context_str += f"\n- Monthly Expenses: ${user_context['expenses']:,.2f}"
            if 'savings_rate' in user_context:
                context_str += f"\n- Savings Rate: {user_context['savings_rate']:.1f}%"
            
            base_prompt += context_str + "\n\nUse this context to give personalized advice when relevant."
        
        return base_prompt
    
    def _get_fallback_response(self, message: str, user_context: dict = None):
        """Provide fallback responses when API is not available"""
        import random
        
        message_lower = message.lower()
        
        # Check for greetings
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'howdy', 'sup', 'yo']):
            context_msg = ""
            if user_context:
                balance = user_context.get('balance', 0)
                savings_rate = user_context.get('savings_rate', 0)
                if balance > 0:
                    context_msg = f" I can see you have ${balance:,.2f} in your account"
                    if savings_rate > 0:
                        context_msg += f" and you're saving {savings_rate:.1f}% of your income!"
            return f"Hi there! I'm Randy, your financial advisor snake! 🐍{context_msg} How can I help you with your finances today?"
        
        # Check for budget questions
        if any(word in message_lower for word in ['budget', 'spending', 'expense']):
            if user_context and user_context.get('expenses'):
                expenses = user_context['expenses']
                income = user_context.get('income', 0)
                if income > 0:
                    expense_percent = (expenses / income) * 100
                    return f"Let's talk about budgeting! You're spending ${expenses:,.2f} per month (that's {expense_percent:.1f}% of your income). I recommend the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings. Want me to break down how that would look for your income? 📊"
                return f"I see you're spending ${expenses:,.2f} per month. The key to good budgeting is categorizing your expenses: needs, wants, and savings. Try tracking where every dollar goes! 💰"
            return "Great question about budgeting! The key is tracking every expense and categorizing them. Try the 50/30/20 rule: 50% for needs (rent, food, bills), 30% for wants (entertainment, dining out), and 20% for savings and debt! 💰"
        
        # Check for saving questions
        if any(word in message_lower for word in ['save', 'saving', 'savings', 'emergency fund']):
            if user_context and user_context.get('savings_rate') is not None:
                rate = user_context['savings_rate']
                income = user_context.get('income', 0)
                if rate >= 20:
                    monthly_savings = (rate / 100) * income
                    annual = monthly_savings * 12
                    return f"Excellent work! You're saving {rate:.1f}% of your income - that's ${monthly_savings:,.2f}/month or ${annual:,.2f}/year! You're crushing it! 🌟🐍 Keep this up and you'll build serious wealth!"
                elif rate > 0:
                    current_savings = (rate / 100) * income
                    target_savings = (20 / 100) * income
                    difference = target_savings - current_savings
                    return f"You're saving {rate:.1f}% (${current_savings:,.2f}/month). To hit the 20% target, try saving an extra ${difference:,.2f}/month. Small wins add up! 💪 Can you cut one subscription or dining expense?"
                else:
                    target = (20 / 100) * income if income > 0 else 100
                    return f"Let's start building your savings! Even starting with ${target:,.2f}/month (20% of income) can make a huge difference. That's ${target * 12:,.2f}/year! Start small if needed - even $50/month is better than nothing! 🌱"
            return "Saving money is all about consistency! Aim for at least 20% of your income. Start with an emergency fund (3-6 months of expenses), then invest for the future. Automate it so you don't even see the money! 🌱"
        
        # Check for income questions
        if any(word in message_lower for word in ['income', 'earn', 'salary', 'money', 'raise', 'side hustle']):
            if user_context and user_context.get('income'):
                income = user_context['income']
                return f"Your monthly income is ${income:,.2f}. Income is important, but what matters most is your savings rate! Are you maximizing what you keep? Consider side hustles, asking for a raise, or developing new skills to boost your earning power! 📈"
            return "Income growth is important, but it's really about what you DO with it that counts! Focus on: 1) Increasing income (skills, side hustles, raises), 2) Keeping expenses stable, 3) Saving the difference. That's how wealth is built! 📈"
        
        # Check for debt questions
        if any(word in message_lower for word in ['debt', 'loan', 'credit card', 'owe', 'payment']):
            return "Debt can feel overwhelming, but you can conquer it! Two strategies: 1) Avalanche method - pay off highest interest debt first (saves most money), 2) Snowball method - pay off smallest debts first (builds momentum). Which approach sounds better for you? 💳"
        
        # Check for investment questions
        if any(word in message_lower for word in ['invest', 'stock', 'retirement', '401k', 'ira', 'crypto']):
            return "Smart thinking about investing! Key principles: 1) Start early (time is your friend!), 2) Diversify (don't put all eggs in one basket), 3) Low-cost index funds are great for beginners, 4) Max out 401k match if available (free money!). What's your timeline? 📊"
        
        # Provide context-aware default response
        if user_context:
            balance = user_context.get('balance', 0)
            savings_rate = user_context.get('savings_rate', 0)
            
            if balance > 1000 and savings_rate >= 15:
                return "You're doing great with your finances! Want to discuss optimizing your budget, increasing savings, or investing strategies? 🎯"
            elif savings_rate < 10:
                return "I'd love to help you boost your savings rate! Currently, experts recommend saving at least 20% of your income. What's your biggest financial challenge right now? 💰"
        
        # Default helpful responses
        responses = [
            "I'm here to help with your finances! Ask me about budgeting, saving strategies, debt management, or investing basics! 🐍💡",
            "Financial health is all about balance - just like a snake needs balance to slither! What's your biggest money goal right now? 🎯",
            "Small financial wins add up to big success! Want to talk about building better money habits? I'm here to help! 🌟",
            "Let's work on your financial wellness together! Whether it's budgeting, saving, or planning for the future, I've got your back! 💪🐍"
        ]
        
        return random.choice(responses)
