"""Randy's dedicated page"""

import flet as ft
from src.ui.components.randy_pet import RandyPet
from src.services.ai_chat import AIChatService
from src.services.api_client import APIClient

class RandyPage(ft.Container):
    """A dedicated page for Randy with more interactions"""
    
    def __init__(self, page: ft.Page = None, auth_service = None):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.ai_chat_service = AIChatService()
        self.api_client = APIClient()
        self.conversation_history = []
        self.user_context = {}
        
        # Initialize chat components
        self.chat_input = ft.TextField(
            hint_text="Ask Randy something...",
            border_radius=10,
            expand=True,
            on_submit=self.send_message
        )
        
        self.chat_view = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=True
        )
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        # Use theme-aware background
        is_dark = page.is_dark_mode if page and hasattr(page, 'is_dark_mode') else False
        self.bgcolor = "#2C2C2C" if is_dark else "#FAF6E9"  # Light cream background
        
        # Load user financial context
        self.load_user_context()
        
        # Add welcome message
        welcome_msg = "Hi there! I'm Randy, your friendly financial advisor snake! 🐍 Ask me anything about budgeting, saving, or managing your money!"
        welcome_bubble = self.create_message_bubble(welcome_msg, is_user=False)
        self.chat_view.controls.append(welcome_bubble)
    
    def build_ui(self):
        """Build Randy's page UI"""
        # Title
        title = ft.Text(
            "Randy's Room 🏠",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE
        )
        
        # Randy container with more space
        randy_container = ft.Container(
            content=RandyPet(),
            bgcolor=ft.Colors.WHITE,
            padding=40,
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            margin=ft.margin.symmetric(horizontal=40, vertical=20)
        )
        
        # Chat container
        chat_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Chat with Randy 💬",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE
                    ),
                    self.chat_view,
                    ft.Row(
                        controls=[
                            self.chat_input,
                            ft.IconButton(
                                icon=ft.Icons.SEND_ROUNDED,
                                icon_color=ft.Colors.BLUE,
                                on_click=self.send_message
                            )
                        ],
                        spacing=10
                    )
                ],
                spacing=10,
                expand=True
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            margin=ft.margin.symmetric(horizontal=40, vertical=10),
            expand=True
        )
        
        # Fun facts about Randy
        facts_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "About Randy 🐍",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE
                    ),
                    ft.Text(
                        "• Randy is your personal finance companion",
                        size=16
                    ),
                    ft.Text(
                        "• His mood reflects your budget health",
                        size=16
                    ),
                    ft.Text(
                        "• Feed him apples to boost his energy",
                        size=16
                    ),
                    ft.Text(
                        "• Keep him happy by maintaining a healthy budget",
                        size=16
                    )
                ],
                spacing=10
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            margin=ft.margin.symmetric(horizontal=40, vertical=10)
        )
        
        # Layout with two columns
        return ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Row(
                        controls=[title],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=20
                ),
                # Main content in two columns
                ft.Row(
                    controls=[
                        # Left column - Randy and facts
                        ft.Column(
                            controls=[randy_container, facts_container],
                            expand=True
                        ),
                        # Right column - Chat
                        chat_container
                    ],
                    expand=True
                )
            ],
            expand=True
        )
    
    def create_message_bubble(self, text: str, is_user: bool):
        """Create a chat message bubble"""
        return ft.Container(
            content=ft.Text(text, color=ft.Colors.WHITE if is_user else ft.Colors.BLACK),
            bgcolor=ft.Colors.BLUE if is_user else ft.Colors.GREY_200,
            padding=15,
            border_radius=10,
            alignment=ft.alignment.center_right if is_user else ft.alignment.center_left
        )
    
    def load_user_context(self):
        """Load user's financial context for personalized AI responses"""
        async def load_context():
            try:
                user_id = 'demo'
                if self.auth_service and hasattr(self.auth_service, 'current_user'):
                    user_id = str(self.auth_service.current_user)
                
                summary_data = await self.api_client.get_summary(user_id)
                self.user_context = {
                    'balance': summary_data.get('balance', 0),
                    'income': summary_data.get('summary', {}).get('income', 0),
                    'expenses': summary_data.get('summary', {}).get('expenses', 0),
                    'savings_rate': summary_data.get('summary', {}).get('savings_rate', 0)
                }
            except Exception as e:
                print(f"⚠️ Could not load user context: {e}")
                self.user_context = {}
        
        if self.page:
            self.page.run_task(load_context)
    
    def send_message(self, e):
        """Handle sending a message with AI response"""
        if not self.chat_input.value or not self.chat_input.value.strip():
            return
        
        user_message = self.chat_input.value.strip()
        self.chat_input.value = ""
        if self.page:
            self.page.update()
        
        # Add user message to chat
        user_bubble = self.create_message_bubble(user_message, is_user=True)
        self.chat_view.controls.append(user_bubble)
        self.update()
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Show loading indicator
        loading = ft.Container(
            content=ft.Row([
                ft.ProgressRing(width=16, height=16, stroke_width=2),
                ft.Text("Randy is thinking...", size=12, color=ft.Colors.BLUE),
            ], spacing=10),
            padding=10,
        )
        self.chat_view.controls.append(loading)
        self.update()
        
        # Get AI response asynchronously
        async def get_response():
            try:
                response = await self.ai_chat_service.chat(
                    user_message,
                    conversation_history=self.conversation_history.copy(),
                    user_context=self.user_context
                )
                
                # Remove loading indicator
                if loading in self.chat_view.controls:
                    self.chat_view.controls.remove(loading)
                
                # Add Randy's response
                randy_bubble = self.create_message_bubble(response, is_user=False)
                self.chat_view.controls.append(randy_bubble)
                
                # Add to conversation history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                self.update()
            except Exception as e:
                print(f"❌ Error getting AI response: {e}")
                # Remove loading indicator
                if loading in self.chat_view.controls:
                    self.chat_view.controls.remove(loading)
                
                error_msg = "Oops! I'm having trouble connecting right now. Make sure you have your CLAUDE_API_KEY set in the .env file! 🐍"
                error_bubble = self.create_message_bubble(error_msg, is_user=False)
                self.chat_view.controls.append(error_bubble)
                self.update()
        
        if self.page:
            self.page.run_task(get_response)