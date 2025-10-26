"""Randy's dedicated page"""

import flet as ft
from src.ui.components.randy_pet import RandyPet
from src.services.ai_insights import AIInsightsService

class RandyPage(ft.Container):
    """A dedicated page for Randy with more interactions"""
    
    def __init__(self, page: ft.Page = None, auth_service = None):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.ai_service = AIInsightsService()
        self.messages = []
        
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
        self.bgcolor = ft.Colors.GREY_50
    
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
    
    def send_message(self, e):
        """Handle sending a message"""
        if not self.chat_input.value:
            return
            
        # Add user message
        user_message = self.create_message_bubble(self.chat_input.value, True)
        self.chat_view.controls.append(user_message)
        
        # Get Randy's response
        response = self.get_randy_response(self.chat_input.value)
        randy_message = self.create_message_bubble(response, False)
        self.chat_view.controls.append(randy_message)
        
        # Clear input and update
        self.chat_input.value = ""
        self.update()
    
    def get_randy_response(self, message: str) -> str:
        """Get Randy's response to a message"""
        greetings = ["hi", "hello", "hey"]
        feelings = ["how are you", "how do you feel"]
        finance_questions = ["budget", "money", "spending", "save"]
        
        message = message.lower()
        
        # Handle greetings
        if any(greeting in message for greeting in greetings):
            return "Hi there! I'm Randy, your friendly finance snake! 🐍 How can I help you today?"
            
        # Handle feelings
        if any(feeling in message for feeling in feelings):
            return "I'm feeling great! Ready to help you with your finances! Want to check your budget? 📊"
            
        # Handle finance questions
        if any(topic in message for topic in finance_questions):
            return "I'd love to help you with your finances! Let's look at your spending habits and find ways to save money. 💰 What specific aspect would you like to focus on?"
            
        # Default response with financial wisdom
        responses = [
            "Remember, tracking your expenses is the first step to financial freedom! 📝",
            "Want to know a secret? Small savings add up to big results over time! 🌱",
            "I'm here to help you reach your financial goals! What would you like to know? 🎯",
            "Let's work together to improve your financial health! 💪",
            "Have you checked your budget today? It's always a good time to review! 📊"
        ]
        import random
        return random.choice(responses)