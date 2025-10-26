"""Login page"""

import flet as ft


class LoginPage(ft.Container):
    """Login page with email/password authentication"""
    
    def __init__(self, page: ft.Page, auth_service):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        
        # Form fields
        self.email_field = ft.TextField(
            label="Email",
            width=300,
            keyboard_type=ft.KeyboardType.EMAIL,
            prefix_icon=ft.Icons.EMAIL,
        )
        
        self.password_field = ft.TextField(
            label="Password",
            width=300,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
        )
        
        self.error_text = ft.Text(
            value="",
            color=ft.Colors.RED,
            size=12,
            visible=False
        )
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
    
    def build_ui(self):
        """Build the login UI"""
        return ft.Stack(
            controls=[
                # Background image
                ft.Image(
                    src="background.png",
                    width=float("inf"),
                    height=float("inf"),
                    fit=ft.ImageFit.COVER,
                ),
                # Content overlay
                ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                        controls=[
                            # Header
                            ft.Container(height=50),
                            ft.Image(
                                src="logo.png",
                                width=80,
                                height=80,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.Text(
                                "Budget Buddy",
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE
                            ),
                            ft.Text(
                                "Your Personal Finance Manager",
                                size=16,
                                color=ft.Colors.GREY_700
                            ),
                            ft.Container(height=40),
                            
                            # Login form
                            self.email_field,
                            ft.Container(height=10),
                            self.password_field,
                            ft.Container(height=5),
                            self.error_text,
                            ft.Container(height=20),
                            
                            # Login button
                            ft.ElevatedButton(
                                "Sign In",
                                width=300,
                                height=50,
                                on_click=self.handle_login,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE,
                                    color=ft.Colors.WHITE,
                                )
                            ),
                            
                            ft.Container(height=20),
                            
                            # Sign up link
                            ft.Row(
                                controls=[
                                    ft.Text("Don't have an account?"),
                                    ft.TextButton(
                                        "Sign Up",
                                        on_click=lambda _: self.page.go("/signup")
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            
                            # Demo mode info
                            ft.Container(height=40),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "🚀 Hackathon Demo Mode",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.ORANGE
                                        ),
                                        ft.Text(
                                            "Configure .env with Supabase credentials for full features",
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                            text_align=ft.TextAlign.CENTER
                                        )
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5
                                ),
                                padding=15,
                                bgcolor=ft.Colors.ORANGE_50,
                                border_radius=10,
                                width=350
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                    ),
                    alignment=ft.alignment.center
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    ]
)
    
    async def handle_login(self, e):
        """Handle login button click"""
        email = self.email_field.value
        password = self.password_field.value
        
        # Validation
        if not email or not password:
            self.show_error("Please enter email and password")
            return
        
        # Attempt login
        success, message = await self.auth_service.sign_in(email, password)
        
        if success:
            self.page.go("/dashboard")
        else:
            self.show_error(message)
    
    def show_error(self, message: str):
        """Display error message"""
        self.error_text.value = message
        self.error_text.visible = True
        self.page.update()