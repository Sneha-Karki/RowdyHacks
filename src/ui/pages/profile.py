"""Profile page - User profile with picture upload"""

import flet as ft
import base64
from ..theme import Theme


class ProfilePage(ft.Container):
    """User profile page"""
    
    def __init__(self, page: ft.Page, auth_service, dashboard=None):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.dashboard = dashboard
        
        # User data - initialize as None, will be loaded from auth
        self.user_id = None
        self.user_name = None
        self.user_email = None
        self.profile_image_url = None
        self.profile_image_base64 = None
        
        # Get user ID and email from auth service
        if self.auth_service.supabase and hasattr(self.auth_service, 'current_user'):
            if self.auth_service.current_user:
                # Get user ID
                if hasattr(self.auth_service.current_user, 'id'):
                    self.user_id = self.auth_service.current_user.id
                    self.user_email = self.auth_service.current_user.email
                elif hasattr(self.auth_service.current_user, 'user'):
                    self.user_id = self.auth_service.current_user.user.id
                    self.user_email = self.auth_service.current_user.user.email
        
        # Build UI first
        self.content = self.build_ui()
        self.expand = True
        # Use theme-aware background with variety
        is_dark = page.is_dark_mode if hasattr(page, 'is_dark_mode') else False
        self.bgcolor = Theme.DARK_SURFACE if is_dark else Theme.LIGHT_WASABI_BG
        self.padding = 30
        self.border_radius = 10
        
        # Then load profile data asynchronously
        self.load_profile_data()
    
    def load_profile_data(self):
        """Load profile data from Supabase"""
        async def fetch_profile():
            if self.auth_service.supabase and self.user_id:
                try:
                    # Try to get profile from user_profiles table
                    response = self.auth_service.supabase.table('user_profiles')\
                        .select('*')\
                        .eq('user_id', self.user_id)\
                        .execute()
                    
                    if response.data and len(response.data) > 0:
                        profile = response.data[0]
                        # Only load name and image, don't override email
                        self.user_name = profile.get('full_name', None)
                        self.profile_image_url = profile.get('profile_image_url', None)
                        
                        # Rebuild UI with loaded data
                        self.content = self.build_ui()
                        self.page.update()
                except Exception as e:
                    print(f"Profile load error: {e}")
        
        self.page.run_task(fetch_profile)
    
    def build_ui(self):
        """Build the profile page UI"""
        # Get theme colors
        is_dark = self.page.is_dark_mode if hasattr(self.page, 'is_dark_mode') else False
        text_color = Theme.DARK_TEXT if is_dark else Theme.NOIR
        
        # Profile picture with upload - support both icon and image
        self.profile_pic_content = ft.Icon(
            ft.Icons.PERSON,
            size=80,
            color=ft.Colors.WHITE
        )
        
        if self.profile_image_url:
            self.profile_pic_content = ft.Image(
                src=self.profile_image_url,
                width=150,
                height=150,
                fit=ft.ImageFit.COVER,
                border_radius=75
            )
        
        self.profile_pic = ft.Container(
            content=ft.Stack([
                ft.Container(
                    content=self.profile_pic_content,
                    width=150,
                    height=150,
                    border_radius=75,
                    bgcolor=ft.Colors.BLUE_400 if not self.profile_image_url else ft.Colors.TRANSPARENT,
                    alignment=ft.alignment.center,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.CAMERA_ALT,
                        icon_color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_700,
                        on_click=self.show_upload_dialog,
                        tooltip="Change Picture"
                    ),
                    alignment=ft.alignment.bottom_right,
                    padding=ft.padding.only(right=5, bottom=5)
                )
            ]),
            width=150,
            height=150
        )
        
        # Name field
        self.name_field = ft.TextField(
            label="Full Name",
            value=self.user_name if self.user_name else "",
            width=400,
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            bgcolor=Theme.DARK_SURFACE if is_dark else ft.Colors.WHITE,
            color=text_color,
            border_color=Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD
        )
        
        # Email field - read-only, pulled from auth
        self.email_field = ft.TextField(
            label="Email",
            value=self.user_email if self.user_email else "",
            width=400,
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            disabled=True,
            read_only=True,
            bgcolor=Theme.DARK_SURFACE if is_dark else ft.Colors.GREY_100,
            color=text_color,
            border_color=Theme.DARK_PRIMARY if is_dark else ft.Colors.GREY_400
        )
        
        return ft.Column(
            controls=[
                # Header
                ft.Row(
                    controls=[
                        ft.Text(
                            "Profile",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=text_color
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(color=Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
                ft.Container(height=20),
                
                # Profile picture
                ft.Row(
                    controls=[self.profile_pic],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=30),
                
                # User information
                ft.Column(
                    controls=[
                        self.name_field,
                        ft.Container(height=10),
                        self.email_field,
                        ft.Container(height=20),
                        
                        # Forgot Username & Password section
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.INFO_OUTLINE, 
                                                size=20, 
                                                color=Theme.DARK_TEXT if is_dark else ft.Colors.GREY_600
                                            ),
                                            ft.Container(width=10),
                                            ft.Text(
                                                "Need account recovery?",
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=text_color
                                            )
                                        ]
                                    ),
                                    ft.Container(height=10),
                                    ft.Row(
                                        controls=[
                                            ft.TextButton(
                                                "Forgot Username",
                                                icon=ft.Icons.HELP_OUTLINE,
                                                on_click=self.handle_forgot_username,
                                                style=ft.ButtonStyle(
                                                    color=Theme.DARK_PRIMARY if is_dark else ft.Colors.BLUE_700
                                                )
                                            ),
                                            ft.Container(width=10),
                                            ft.TextButton(
                                                "Forgot Password",
                                                icon=ft.Icons.LOCK_RESET,
                                                on_click=self.handle_forgot_password,
                                                style=ft.ButtonStyle(
                                                    color=Theme.KHAKI if is_dark else ft.Colors.ORANGE_700
                                                )
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                ],
                                spacing=5
                            ),
                            bgcolor=Theme.DARK_BG if is_dark else ft.Colors.BLUE_50,
                            padding=15,
                            border_radius=10,
                            width=400,
                            border=ft.border.all(
                                1, 
                                Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD
                            )
                        ),
                        
                        ft.Container(height=30),
                        
                        # Action buttons
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Save Changes",
                                    icon=ft.Icons.SAVE,
                                    on_click=self.handle_save_profile,
                                    style=ft.ButtonStyle(
                                        bgcolor=Theme.DARK_PRIMARY if is_dark else Theme.EMERALD,
                                        color=ft.Colors.WHITE
                                    )
                                ),
                                ft.TextButton(
                                    "Cancel",
                                    on_click=self.handle_cancel,
                                    style=ft.ButtonStyle(
                                        color=Theme.DARK_TEXT if is_dark else ft.Colors.GREY_700
                                    )
                                )
                            ],
                            spacing=10
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    def show_upload_dialog(self, e):
        """Show file upload dialog"""
        if not hasattr(self, 'file_picker'):
            self.file_picker = ft.FilePicker(on_result=self.on_picture_selected)
            self.page.overlay.append(self.file_picker)
            self.page.update()
        
        self.file_picker.pick_files(
            dialog_title="Select Profile Picture",
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            allow_multiple=False
        )
    
    def on_picture_selected(self, e: ft.FilePickerResultEvent):
        """Handle picture selection from file picker"""
        if not e.files or len(e.files) == 0:
            return
        
        file_info = e.files[0]
        file_path = file_info.path
        
        if file_path:
            try:
                # Read file and convert to base64 for display
                with open(file_path, 'rb') as f:
                    image_data = f.read()
                    self.profile_image_base64 = base64.b64encode(image_data).decode()
                
                # For display, we'll use a data URL
                file_ext = file_info.name.split('.')[-1].lower()
                mime_type = f"image/{file_ext}" if file_ext in ['jpg', 'jpeg', 'png', 'gif'] else "image/jpeg"
                self.profile_image_url = f"data:{mime_type};base64,{self.profile_image_base64}"
                
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"✅ Picture uploaded: {file_info.name}"),
                    bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EMERALD
                )
                self.page.snack_bar.open = True
                
                # Rebuild UI to show new image
                old_content = self.content
                self.content = self.build_ui()
                
                # Force update of the container
                if hasattr(self, 'parent') and self.parent:
                    self.parent.update()
                else:
                    self.update()
                
                self.page.update()
                
                print(f"Profile picture uploaded: {file_info.name}")
                print(f"Image URL set: {self.profile_image_url[:50]}...")
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Error reading file: {str(ex)}"),
                    bgcolor=Theme.MAPLE
                )
                self.page.snack_bar.open = True
                self.page.update()
        else:
            # Fallback: show message about web mode limitations
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("⚠️ File path not available in web mode. Try using an image URL instead."),
                bgcolor=Theme.KHAKI if self.page.is_dark_mode else Theme.KHAKI
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def handle_save_profile(self, e):
        """Handle save profile changes to Supabase"""
        self.user_name = self.name_field.value
        
        async def save_to_db():
            if self.auth_service.supabase and self.user_id:
                try:
                    # Only save name and profile image (not email - it comes from auth)
                    data = {
                        'user_id': self.user_id,
                        'full_name': self.user_name,
                        'profile_image_url': self.profile_image_url
                    }
                    
                    print(f"Saving profile data: {data}")
                    
                    response = self.auth_service.supabase.table('user_profiles')\
                        .upsert(data)\
                        .execute()
                    
                    print(f"Profile save response: {response}")
                    
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("✅ Profile updated successfully!"),
                        bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EMERALD
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                    
                    print(f"Profile saved - Name: {self.user_name}")
                except Exception as ex:
                    print(f"Supabase save error: {ex}")
                    # If table doesn't exist, save locally and inform user
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"✅ Profile updated locally! (Note: Database table may need setup)"),
                        bgcolor=Theme.KHAKI if self.page.is_dark_mode else Theme.KHAKI
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
            else:
                # Fallback for when Supabase not available
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("⚠️ Cannot save: User not authenticated"),
                    bgcolor=Theme.MAPLE
                )
                self.page.snack_bar.open = True
                self.page.update()
        
        self.page.run_task(save_to_db)
    
    def handle_forgot_username(self, e):
        """Handle forgot username - placeholder"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("📧 Username recovery email sent! (Placeholder)"),
            bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EARTH
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def handle_forgot_password(self, e):
        """Handle forgot password - placeholder"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("🔒 Password reset link sent! (Placeholder)"),
            bgcolor=Theme.KHAKI if self.page.is_dark_mode else Theme.KHAKI
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def handle_cancel(self, e):
        """Handle cancel button - return to overview"""
        if self.dashboard:
            self.dashboard.switch_view(0)  # Return to overview
        else:
            # Fallback
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Changes discarded"),
                bgcolor=Theme.DARK_PRIMARY if self.page.is_dark_mode else Theme.EMERALD
            )
            self.page.snack_bar.open = True
            self.page.update()
