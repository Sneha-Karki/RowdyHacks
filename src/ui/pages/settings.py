"""Settings page - App settings with theme toggle"""

import flet as ft
from ..theme import Theme


class SettingsPage(ft.Container):
    """Settings page with theme toggle"""
    
    def __init__(self, page: ft.Page, auth_service, dashboard=None):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.dashboard = dashboard
        
        # Initialize dark mode state
        if not hasattr(page, 'is_dark_mode'):
            page.is_dark_mode = False
        
        self.is_dark_mode = page.is_dark_mode
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        # Use light emerald for settings page in light mode
        self.bgcolor = Theme.DARK_SURFACE if self.is_dark_mode else Theme.LIGHT_EMERALD_BG
        self.padding = 30
        self.border_radius = 10
    
    def build_ui(self):
        """Build the settings page UI"""
        text_color = Theme.DARK_TEXT if self.is_dark_mode else Theme.NOIR
        
        # Theme toggle switch
        self.theme_switch = ft.Switch(
            label="Dark Mode",
            value=self.is_dark_mode,
            on_change=self.handle_theme_toggle,
            active_color=Theme.LIGHT_EMERALD if not self.is_dark_mode else Theme.DARK_PRIMARY
        )
        
        return ft.Column(
            controls=[
                # Header with back button
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            tooltip="Back",
                            on_click=self.handle_back,
                            icon_color=text_color
                        ),
                        ft.Text(
                            "Settings",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=text_color
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(),
                ft.Container(height=20),
                
                # Theme Setting
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.PALETTE_OUTLINED,
                                        size=30,
                                        color=Theme.LIGHT_EMERALD if not self.is_dark_mode else Theme.DARK_PRIMARY
                                    ),
                                    ft.Container(width=15),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Appearance",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                color=text_color
                                            ),
                                            ft.Text(
                                                "Toggle between light and dark mode",
                                                size=12,
                                                color=Theme.DARK_TEXT if self.is_dark_mode else "#666666"
                                            )
                                        ],
                                        spacing=2,
                                        expand=True
                                    ),
                                    self.theme_switch
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Container(height=10),
                            ft.Divider(),
                            ft.Container(height=10),
                            
                            # Color palette preview
                            ft.Text(
                                "Color Palette:",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=text_color
                            ),
                            ft.Container(height=5),
                            self.build_color_preview()
                        ],
                        spacing=5
                    ),
                    bgcolor=ft.Colors.WHITE if not self.is_dark_mode else Theme.DARK_BG,
                    padding=20,
                    border_radius=10,
                    border=ft.border.all(
                        1,
                        Theme.LIGHT_EMERALD if not self.is_dark_mode else Theme.DARK_PRIMARY
                    )
                ),
                
                ft.Container(height=20),
                
                # Additional settings placeholder
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "More settings coming soon...",
                                size=14,
                                color=Theme.DARK_TEXT if self.is_dark_mode else "#666666",
                                italic=True
                            )
                        ]
                    ),
                    padding=20
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    
    def build_color_preview(self):
        """Build color palette preview"""
        if self.is_dark_mode:
            colors = [
                ("Primary", Theme.DARK_PRIMARY),
                ("Secondary", Theme.DARK_SECONDARY),
                ("Accent", Theme.DARK_ACCENT),
                ("Background", Theme.DARK_BG),
                ("Text", Theme.DARK_TEXT)
            ]
        else:
            colors = [
                ("Emerald", Theme.EMERALD),
                ("Lt Emerald", Theme.LIGHT_EMERALD),
                ("Wasabi", Theme.WASABI),
                ("Lt Wasabi", Theme.LIGHT_WASABI),
                ("Khaki", Theme.KHAKI),
                ("Lt Khaki", Theme.LIGHT_KHAKI),
                ("Earth", Theme.EARTH),
                ("Lt Earth", Theme.LIGHT_EARTH),
            ]
        
        color_boxes = []
        for name, color in colors:
            color_boxes.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                bgcolor=color,
                                width=60,
                                height=60,
                                border_radius=10,
                                border=ft.border.all(2, ft.Colors.GREY_400)
                            ),
                            ft.Text(
                                name,
                                size=10,
                                color=Theme.DARK_TEXT if self.is_dark_mode else Theme.NOIR,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5
                    ),
                    padding=5
                )
            )
        
        return ft.Row(
            controls=color_boxes,
            spacing=10,
            wrap=True
        )
    
    def handle_theme_toggle(self, e):
        """Handle theme toggle"""
        self.is_dark_mode = e.control.value
        self.page.is_dark_mode = self.is_dark_mode
        
        # Apply theme to page
        if self.is_dark_mode:
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # Show message
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"✅ Switched to {'Dark' if self.is_dark_mode else 'Light'} Mode"
            ),
            bgcolor=Theme.DARK_PRIMARY if self.is_dark_mode else Theme.LIGHT_EMERALD
        )
        self.page.snack_bar.open = True
        
        # Rebuild settings UI with new theme
        self.bgcolor = Theme.DARK_SURFACE if self.is_dark_mode else ft.Colors.WHITE
        self.content = self.build_ui()
        
        # Update page first
        self.page.update()
        
        # Refresh dashboard if available
        if self.dashboard:
            self.dashboard.refresh_with_theme()
    
    def handle_back(self, e):
        """Handle back button - return to overview"""
        if self.dashboard:
            self.dashboard.switch_view(0)  # Return to overview
        else:
            self.page.go("/")
