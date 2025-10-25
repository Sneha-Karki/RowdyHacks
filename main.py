"""Main application entry point"""

import flet as ft
from src.utils.config import Config
from src.auth.auth_service import AuthService
from src.ui.pages.login import LoginPage
from src.ui.pages.signup import SignupPage
from src.ui.pages.dashboard import DashboardPage


class BudgetBuddyApp:
    """Main application class"""
    
    def __init__(self):
        self.auth_service = AuthService()
        self.page = None
    
    def main(self, page: ft.Page):
        """Main application entry point"""
        self.page = page
        
        # Page configuration
        page.title = Config.APP_NAME
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.window_width = 1200
        page.window_height = 800
        page.window_min_width = 800
        page.window_min_height = 600
        
        # Session management
        if not hasattr(page, "session"):
            page.session = {}
        
        # Routing
        def route_change(route):
            page.views.clear()
            
            # Check authentication status
            is_authenticated = self.auth_service.is_authenticated()
            
            # Route to appropriate page
            if page.route == "/":
                page.views.append(
                    ft.View(
                        "/",
                        [LoginPage(page, self.auth_service)],
                        padding=0
                    )
                )
            elif page.route == "/signup":
                page.views.append(
                    ft.View(
                        "/signup",
                        [SignupPage(page, self.auth_service)],
                        padding=0
                    )
                )
            elif page.route == "/dashboard":
                if is_authenticated:
                    page.views.append(
                        ft.View(
                            "/dashboard",
                            [DashboardPage(page, self.auth_service)],
                            padding=0
                        )
                    )
                else:
                    page.route = "/"
                    page.update()
                    return
            
            page.update()
        
        def view_pop(view):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        
        page.on_route_change = route_change
        page.on_view_pop = view_pop
        
        # Show configuration warning if not set up
        if not Config.is_configured():
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "Please configure your .env file with Supabase credentials",
                    color=ft.Colors.WHITE
                ),
                bgcolor=ft.Colors.ORANGE,
                duration=5000
            )
            page.snack_bar.open = True
        
        # Start with login page
        page.go("/")


def main():
    """Application entry point"""
    app = BudgetBuddyApp()
    ft.app(target=app.main, view=ft.AppView.WEB_BROWSER)


if __name__ == "__main__":
    main()
