"""Profile page - User settings and information"""

import flet as ft
from ...services.api_client import APIClient


class ProfilePage(ft.Container):
    """Profile management and settings"""
    
    def __init__(self, page: ft.Page, auth_service):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.api_client = APIClient()
        
        # User data
        self.user_data = {
            'email': self.auth_service.current_user.email if hasattr(self.auth_service.current_user, 'email') else 'demo@example.com',
            'name': 'Demo User',
            'joined_date': 'October 2025',
            'preferred_currency': 'USD',
            'notification_settings': {
                'email_notifications': True,
                'budget_alerts': True,
                'spending_insights': True
            }
        }
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        self.bgcolor = ft.Colors.WHITE
        self.padding = 0  # No padding as we'll use the Stack for layout
        
    def build_ui(self):
        """Build the profile page UI"""
        return ft.Stack([
            # Background banner
            ft.Container(
                content=ft.Image(
                    src="/Users/perfectsylvester/dev/RowdyHacks/assets/nav-banner.png",
                    width=float("inf"),
                    height=float("inf"),
                    fit=ft.ImageFit.COVER,
                ),
                expand=True,
            ),
            # Content overlay
            ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=ft.Colors.WHITE),
                            ft.Text("Profile Settings", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Edit Profile",
                                icon_color=ft.Colors.WHITE,
                                on_click=self.handle_edit_profile
                            )
                        ]),
                        padding=30
                    ),
                    # Main content with white background
                    ft.Container(
                        content=ft.Column([
                            # Basic Information Section
                            self.create_section(
                                "Basic Information",
                                ft.Column([
                                    self.create_info_row("Email", self.user_data['email']),
                                    self.create_info_row("Display Name", self.user_data['name']),
                                    self.create_info_row("Member Since", self.user_data['joined_date']),
                                    ft.Container(
                                        content=ft.ElevatedButton(
                                            "Change Password",
                                            icon=ft.Icons.LOCK_RESET,
                                            on_click=self.handle_change_password
                                        ),
                                        margin=ft.margin.only(top=10)
                                    )
                                ])
                            ),
                            # Preferences Section
                            self.create_section(
                                "Preferences",
                                ft.Column([
                                    self.create_dropdown(
                                        "Preferred Currency",
                                        ["USD", "EUR", "GBP", "JPY", "CAD"],
                                        self.user_data['preferred_currency']
                                    ),
                                    self.create_toggle(
                                        "Email Notifications",
                                        "Receive important updates and insights",
                                        self.user_data['notification_settings']['email_notifications']
                                    ),
                                    self.create_toggle(
                                        "Budget Alerts",
                                        "Get notified when approaching budget limits",
                                        self.user_data['notification_settings']['budget_alerts']
                                    ),
                                    self.create_toggle(
                                        "Spending Insights",
                                        "Weekly analysis of your spending patterns",
                                        self.user_data['notification_settings']['spending_insights']
                                    )
                                ])
                            ),
                            # Data & Privacy Section
                            self.create_section(
                                "Data & Privacy",
                                ft.Column([
                                    ft.ElevatedButton(
                                        "Export My Data",
                                        icon=ft.Icons.DOWNLOAD,
                                        on_click=self.handle_export_data
                                    ),
                                    ft.Container(height=10),
                                    ft.ElevatedButton(
                                        "Delete Account",
                                        icon=ft.Icons.DELETE_FOREVER,
                                        style=ft.ButtonStyle(
                                            color=ft.Colors.WHITE,
                                            bgcolor=ft.Colors.RED_600
                                        ),
                                        on_click=self.handle_delete_account
                                    )
                                ])
                            )
                        ], scroll=ft.ScrollMode.AUTO),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=ft.border_radius.only(
                            top_left=30,
                            top_right=30
                        ),
                        padding=30,
                        expand=True
                    )
                ]),
                expand=True
            )
        ])
    
    def create_section(self, title: str, content: ft.Control):
        """Create a section with title and content"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                content
            ]),
            border=ft.border.all(1, ft.Colors.BLACK12),
            border_radius=10,
            padding=20,
            margin=ft.margin.only(bottom=20)
        )
    
    def create_info_row(self, label: str, value: str):
        """Create an information row with label and value"""
        return ft.Container(
            content=ft.Row([
                ft.Text(label, size=16, color=ft.Colors.GREY_700),
                ft.Container(expand=True),
                ft.Text(value, size=16, weight=ft.FontWeight.W_500)
            ]),
            margin=ft.margin.only(bottom=10)
        )
    
    def create_dropdown(self, label: str, options: list, value: str):
        """Create a dropdown setting"""
        return ft.Container(
            content=ft.Column([
                ft.Text(label, size=16, color=ft.Colors.GREY_700),
                ft.Dropdown(
                    value=value,
                    options=[ft.dropdown.Option(opt) for opt in options],
                    width=200,
                    on_change=self.handle_setting_change
                )
            ]),
            margin=ft.margin.only(bottom=15)
        )
    
    def create_toggle(self, label: str, description: str, value: bool):
        """Create a toggle setting with description"""
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(label, size=16, color=ft.Colors.GREY_700),
                    ft.Text(description, size=12, color=ft.Colors.GREY_600)
                ], expand=True),
                ft.Switch(value=value, on_change=self.handle_setting_change)
            ]),
            margin=ft.margin.only(bottom=15)
        )
    
    def handle_edit_profile(self, e):
        """Handle editing basic profile information"""
        def save_changes(e):
            name_value = name_field.value.strip()
            if name_value:
                self.user_data['name'] = name_value
                self.content = self.build_ui()
                self.page.update()
            dialog.open = False
            self.page.update()
        
        name_field = ft.TextField(
            label="Display Name",
            value=self.user_data['name'],
            width=300
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Edit Profile"),
            content=ft.Column([
                ft.Text("Email (cannot be changed)", size=12, color=ft.Colors.GREY_600),
                ft.Text(self.user_data['email'], size=16),
                ft.Container(height=20),
                name_field
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.ElevatedButton("Save", on_click=save_changes)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def handle_change_password(self, e):
        """Handle password change request"""
        def validate_and_change(e):
            current = current_password.value
            new = new_password.value
            confirm = confirm_password.value
            
            if not all([current, new, confirm]):
                error_text.value = "Please fill in all fields"
                self.page.update()
                return
            
            if new != confirm:
                error_text.value = "New passwords don't match"
                self.page.update()
                return
            
            if len(new) < 8:
                error_text.value = "Password must be at least 8 characters"
                self.page.update()
                return
            
            # Here you would integrate with your auth service
            # self.auth_service.change_password(current, new)
            
            dialog.open = False
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Password changed successfully!"),
                    bgcolor=ft.Colors.GREEN
                )
            )
            self.page.update()
        
        current_password = ft.TextField(
            label="Current Password",
            password=True,
            can_reveal_password=True,
            width=300
        )
        
        new_password = ft.TextField(
            label="New Password",
            password=True,
            can_reveal_password=True,
            width=300
        )
        
        confirm_password = ft.TextField(
            label="Confirm New Password",
            password=True,
            can_reveal_password=True,
            width=300
        )
        
        error_text = ft.Text("", color=ft.Colors.RED_600)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Change Password"),
            content=ft.Column([
                error_text,
                current_password,
                new_password,
                confirm_password
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.ElevatedButton("Change Password", on_click=validate_and_change)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def handle_setting_change(self, e):
        """Handle changes to settings"""
        # Here you would integrate with your API to save settings
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Settings updated!"),
                bgcolor=ft.Colors.GREEN
            )
        )
        self.page.update()
    
    def handle_export_data(self, e):
        """Handle data export request"""
        # Here you would integrate with your API to export user data
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Your data export is being prepared. You'll receive an email when it's ready."),
                bgcolor=ft.Colors.BLUE
            )
        )
        self.page.update()
    
    def handle_delete_account(self, e):
        """Handle account deletion request"""
        def confirm_delete(e):
            if confirm_field.value == "DELETE":
                # Here you would integrate with your auth service and API
                # self.auth_service.delete_account()
                dialog.open = False
                self.page.go("/")  # Redirect to login
            else:
                error_text.value = "Please type DELETE to confirm"
            self.page.update()
        
        confirm_field = ft.TextField(
            label="Type DELETE to confirm",
            width=300
        )
        
        error_text = ft.Text("", color=ft.Colors.RED_600)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Delete Account"),
            content=ft.Column([
                ft.Text(
                    "⚠️ This action cannot be undone. All your data will be permanently deleted.",
                    color=ft.Colors.RED_600,
                    size=14
                ),
                ft.Container(height=20),
                error_text,
                confirm_field
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.ElevatedButton(
                    "Delete Account",
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED_600
                    ),
                    on_click=confirm_delete
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()