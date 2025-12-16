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
        
        # Initialize dark mode state on page if not exists
        if not hasattr(page, 'is_dark_mode'):
            page.is_dark_mode = False
        
        # Initialize page visibility settings
        if not hasattr(page, 'visible_pages'):
            page.visible_pages = {
                'overview': True,
                'randy': True,
                'budgets': True,
                'leaderboard': True
            }
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        # Use light emerald for settings page in light mode
        self.bgcolor = Theme.DARK_SURFACE if self.get_dark_mode() else Theme.LIGHT_EMERALD_BG
        self.padding = 30
        self.border_radius = 10
    
    def get_dark_mode(self):
        """Get current dark mode state from page (source of truth)"""
        page = self.page if self.page else (self.dashboard.page if self.dashboard else None)
        return page.is_dark_mode if page and hasattr(page, 'is_dark_mode') else False
    
    def build_ui(self):
        """Build the settings page UI"""
        is_dark_mode = self.get_dark_mode()
        text_color = Theme.DARK_TEXT if is_dark_mode else Theme.NOIR
        
        # Theme toggle switch
        self.theme_switch = ft.Switch(
            label="Dark Mode",
            value=is_dark_mode,
            on_change=self.handle_theme_toggle,
            active_color=Theme.LIGHT_EMERALD if not is_dark_mode else Theme.DARK_PRIMARY
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
                                        color=Theme.LIGHT_EMERALD if not is_dark_mode else Theme.DARK_PRIMARY
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
                                                color=Theme.DARK_TEXT if is_dark_mode else "#666666"
                                            )
                                        ],
                                        spacing=2,
                                        expand=True
                                    ),
                                    self.theme_switch
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ],
                        spacing=5
                    ),
                    bgcolor=ft.Colors.WHITE if not is_dark_mode else Theme.DARK_BG,
                    padding=20,
                    border_radius=10,
                    border=ft.border.all(
                        1,
                        Theme.LIGHT_EMERALD if not is_dark_mode else Theme.DARK_PRIMARY
                    )
                ),
                
                ft.Container(height=20),
                
                # Page Visibility Settings
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.VISIBILITY_OUTLINED,
                                        size=30,
                                        color=Theme.LIGHT_EMERALD if not is_dark_mode else Theme.DARK_PRIMARY
                                    ),
                                    ft.Container(width=15),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Page Visibility",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                color=text_color
                                            ),
                                            ft.Text(
                                                "Toggle which pages appear in navigation",
                                                size=12,
                                                color=Theme.DARK_TEXT if is_dark_mode else "#666666"
                                            )
                                        ],
                                        spacing=2,
                                        expand=True
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Container(height=10),
                            ft.Divider(),
                            ft.Container(height=10),
                            
                            # Page toggles
                            self.build_page_toggle("Overview", "overview", ft.Icons.DASHBOARD),
                            self.build_page_toggle("Randy", "randy", ft.Icons.PETS),
                            self.build_page_toggle("Budgets", "budgets", ft.Icons.CATEGORY),
                            self.build_page_toggle("Leaderboard", "leaderboard", ft.Icons.LEADERBOARD),
                        ],
                        spacing=5
                    ),
                    bgcolor=ft.Colors.WHITE if not is_dark_mode else Theme.DARK_BG,
                    padding=20,
                    border_radius=10,
                    border=ft.border.all(
                        1,
                        Theme.LIGHT_EMERALD if not is_dark_mode else Theme.DARK_PRIMARY
                    )
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    
    def build_color_preview(self):
        """Build color palette preview"""
        is_dark_mode = self.get_dark_mode()
        if is_dark_mode:
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
                                color=Theme.DARK_TEXT if is_dark_mode else Theme.NOIR,
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
        """Handle theme toggle - update state first, then rebuild"""
        new_dark_mode = e.control.value
        
        # Get page reference
        page = self.page if self.page else (self.dashboard.page if self.dashboard else None)
        if not page:
            return
        
        # CRITICAL: Update page theme state FIRST (source of truth)
        page.is_dark_mode = new_dark_mode
        page.theme_mode = ft.ThemeMode.DARK if new_dark_mode else ft.ThemeMode.LIGHT
        
        # Force page update to apply theme change
        page.update()
        
        # NOW rebuild settings page content with new colors (will read from page.is_dark_mode)
        self.bgcolor = Theme.DARK_SURFACE if new_dark_mode else Theme.LIGHT_EMERALD_BG
        self.content = self.build_ui()
        self.update()
        
        # Update dashboard colors if it exists
        if self.dashboard:
            self.dashboard.update_colors()
        
        # Final update
        page.update()
        
        # Show success message
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"✅ Switched to {'Dark' if new_dark_mode else 'Light'} Mode"),
            bgcolor=Theme.DARK_PRIMARY if new_dark_mode else Theme.LIGHT_EMERALD
        )
        page.snack_bar.open = True
        page.update()
    
    def build_page_toggle(self, label: str, page_key: str, icon):
        """Build a toggle switch for page visibility"""
        is_dark_mode = self.get_dark_mode()
        text_color = Theme.DARK_TEXT if is_dark_mode else Theme.NOIR
        
        # Get page reference safely
        page = self.page if self.page else (self.dashboard.page if self.dashboard else None)
        current_value = page.visible_pages.get(page_key, True) if page else True
        
        toggle = ft.Switch(
            value=current_value,
            on_change=lambda e: self.handle_page_visibility_toggle(page_key, e.control.value, e.control),
            active_color=Theme.LIGHT_EMERALD if not is_dark_mode else Theme.DARK_PRIMARY
        )
        
        return ft.Row(
            controls=[
                ft.Icon(icon, size=20, color=text_color),
                ft.Container(width=10),
                ft.Text(
                    label,
                    size=14,
                    color=text_color,
                    expand=True
                ),
                toggle
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    def handle_page_visibility_toggle(self, page_key: str, is_visible: bool, toggle_control=None):
        """Handle page visibility toggle"""
        # Get page reference from dashboard if self.page is None
        page = self.page if self.page else (self.dashboard.page if self.dashboard else None)
        if not page:
            return
        
        # Check if trying to disable all pages
        if not is_visible:
            visible_count = sum(1 for v in page.visible_pages.values() if v)
            if visible_count <= 1:
                # Show warning - can't disable all pages
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("⚠️ You must keep at least one page visible!"),
                    bgcolor=ft.Colors.ORANGE_800
                )
                page.snack_bar.open = True
                # Reset the toggle back to True directly
                if toggle_control:
                    toggle_control.value = True
                    toggle_control.update()
                page.update()
                return
        
        page.visible_pages[page_key] = is_visible
        
        # Show notification
        page_names = {
            'overview': 'Overview',
            'randy': 'Randy',
            'budgets': 'Budgets',
            'leaderboard': 'Leaderboard'
        }
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"{'✅ Enabled' if is_visible else '❌ Disabled'} {page_names.get(page_key, page_key)} page"
            ),
            bgcolor=Theme.DARK_PRIMARY if self.get_dark_mode() else Theme.LIGHT_EMERALD
        )
        page.snack_bar.open = True
        page.update()
        
        # Update navigation rail without changing current view
        if self.dashboard:
            self.dashboard.update_navigation_rail()
    
    def handle_back(self, e):
        """Handle back button - return to overview"""
        if self.dashboard:
            self.dashboard.switch_view(0)  # Return to overview
        else:
            self.page.go("/")
