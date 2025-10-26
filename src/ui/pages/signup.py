"""Sign up page"""

import flet as ft


class SignupPage(ft.Container):
    """Sign up page for new user registration"""

    def __init__(self, page: ft.Page, auth_service):
        super().__init__()
        self.page = page
        self.auth_service = auth_service

        self.email_field = ft.TextField(
            label="Email",
            width=300,
            keyboard_type=ft.KeyboardType.EMAIL,
            prefix_icon=ft.Icons.EMAIL,
            color=ft.Colors.BLACK,       # text color inside the box
            bgcolor=ft.Colors.WHITE,     # box background
            border_radius=5,             # optional: rounded corners
        )

        self.password_field = ft.TextField(
            label="Password",
            width=300,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=5,
        )

        self.confirm_password_field = ft.TextField(
            label="Confirm Password",
            width=300,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=5,
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
        return ft.Stack(
            controls=[
                # Full-page background image
                ft.Container(ft.Image(
                        src="signupbg.png",
                        width=float("inf"),
                        height=float("inf"),
                        fit=ft.ImageFit.COVER,   # fills the container fully, cropping if needed
                        expand=True
                    ),
                    #alignment=ft.alignment.center,  # centers the image
                )
,

                # Foreground content container with right shift
                ft.Container(  # move form slightly to the right
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            # Back button
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=lambda _: self.page.go("/")
                                ),
                                alignment=ft.alignment.top_left,
                                padding=20
                            ),

                            # Header
                            ft.Image(
                            src="logo.png",
                            width=200,
                            height=200,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Text(
                            "Create Account",
                            size=36,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        ft.Text(
                            "Join Big $hot today",
                            size=16,
                            color=ft.Colors.WHITE
                        ),
                            

                            # Signup form
                            self.email_field,
                            ft.Container(height=10),
                            self.password_field,
                            ft.Container(height=10),
                            self.confirm_password_field,
                            ft.Container(height=5),
                            self.error_text,
                            ft.Container(height=20),

                            # Signup button
                            ft.ElevatedButton(
                                "Create Account",
                                width=300,
                                height=50,
                                on_click=self.handle_signup,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN,
                                    color=ft.Colors.WHITE,
                                )
                            ),

                            ft.Container(height=20),

                            # Login link
                            ft.Row(
                                controls=[
                                    ft.Text("Already have an account?", 
                                            color=ft.Colors.WHITE
                                            ),
                                    
                                    ft.TextButton(
                                        "Sign In",
                                        on_click=lambda _: self.page.go("/"),
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(
                                                size=15,
                                                color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD
                                            )
                                        )
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    )
                )
            ]
        )

    async def handle_signup(self, e):
        """Handle signup button click"""
        email = self.email_field.value
        password = self.password_field.value
        confirm = self.confirm_password_field.value

        # Validation
        if not email or not password or not confirm:
            self.show_error("Please fill in all fields")
            return

        if password != confirm:
            self.show_error("Passwords do not match")
            return

        if len(password) < 6:
            self.show_error("Password must be at least 6 characters")
            return

        # Attempt signup
        success, message = await self.auth_service.sign_up(email, password)

        if success:
            # Show success message
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor="#008000"
            )
            self.page.snack_bar.open = True
            self.page.update()

            # Redirect to login
            self.page.go("/")
        else:
            self.show_error(message)

    def show_error(self, message: str):
        """Display error message"""
        self.error_text.value = message
        self.error_text.visible = True
        self.page.update()