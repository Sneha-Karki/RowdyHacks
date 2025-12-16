"""Dashboard page - main app interface"""

import flet as ft
from datetime import datetime
from src.ui.components.randy_pet import RandyPet
from src.ui.pages.randy_page import RandyPage
from src.ui.pages.transactions_page import TransactionsPage
from src.ui.pages.budget import BudgetsPage
from src.ui.pages.leaderboard import InsightsPage
from src.ui.pages.profile import ProfilePage
from src.ui.pages.settings import SettingsPage
from ...services.api_client import APIClient
from ..theme import Theme


class DashboardPage(ft.Container):
    """Main dashboard with navigation and content area"""
    
    def __init__(self, page: ft.Page, auth_service):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.api_client = APIClient()
        self.current_view = "overview"
        
        # Initialize theme
        if not hasattr(page, 'is_dark_mode'):
            page.is_dark_mode = False
        
        # Data storage
        self.balance = 0.0
        self.monthly_summary = {}
        self.transactions = []
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        self.bgcolor = ft.Colors.TRANSPARENT  # Make container transparent to show background
        
        # Load data
        self.load_dashboard_data()
    
    def build_ui(self):
        """Build the dashboard UI"""
        # Get current theme colors
        is_dark = self.page.is_dark_mode if hasattr(self.page, 'is_dark_mode') else False
        # Use background images like signup page
        bg_image = "signupbg.png" if not is_dark else "signupbg.png"  # Can use different image for dark mode
        
        return ft.Stack([
            # Background image (like signup page)
            ft.Container(
                content=ft.Image(
                    src=bg_image,
                    width=float("inf"),
                    height=float("inf"),
                    fit=ft.ImageFit.COVER,
                    expand=True
                ),
                expand=True
            ),
            # Main content
            self.build_main_content()
        ])
    
    def build_main_content(self):
        """Build main content area"""
        # Get theme colors
        is_dark = self.page.is_dark_mode if hasattr(self.page, 'is_dark_mode') else False
        nav_bg = Theme.DARK_SURFACE if is_dark else ft.Colors.WHITE
        app_bar_bg = Theme.DARK_SURFACE if is_dark else ft.Colors.WHITE
        text_color = Theme.DARK_TEXT if is_dark else Theme.NOIR
        
        # Navigation rail
        nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="Overview"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PETS_OUTLINED,
                    selected_icon=ft.Icons.PETS,
                    label="Randy"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CATEGORY_OUTLINED,
                    selected_icon=ft.Icons.CATEGORY,
                    label="Budgets"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.LEADERBOARD_OUTLINED,
                    selected_icon=ft.Icons.LEADERBOARD,
                    label="Leaderboard"
                ),
            ],
            on_change=self.handle_nav_change,
            bgcolor=nav_bg
        )
        
        # Main content area
        self.content_area = ft.Container(
            content=self.build_overview(),
            expand=True,
            padding=30
        )
        
        # Top app bar with full-width background image
        app_bar = ft.Stack(
            controls=[
                # Background image that fills the entire banner
                ft.Container(
                    content=ft.Image(
                        src="nav-banner.png",  # Put your banner image in assets folder
                        width=float("inf"),
                        height=150,
                        fit=ft.ImageFit.COVER,  # Use COVER to fill, or FIT_WIDTH to maintain aspect ratio
                    ),
                    expand=True,
                ),
                # Semi-transparent overlay (darker in light mode, lighter in dark mode)
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK) if not is_dark else ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    expand=True,
                ),
                # Overlay content (buttons and text)
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                "Big $hot",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,  # White text to stand out on image
                            ),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.UPLOAD_FILE,
                                tooltip="Import CSV",
                                on_click=self.handle_csv_import,
                                icon_color=ft.Colors.WHITE,
                                icon_size=20,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                                tooltip="Notifications",
                                icon_color=ft.Colors.WHITE,
                                icon_size=20,
                            ),
                            ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(
                                        text="Profile",
                                        icon=ft.Icons.PERSON,
                                        on_click=self.show_profile_page
                                    ),
                                    ft.PopupMenuItem(
                                        text="Settings",
                                        icon=ft.Icons.SETTINGS,
                                        on_click=self.show_settings_page
                                    ),
                                    ft.PopupMenuItem(),
                                    ft.PopupMenuItem(
                                        text="Sign Out",
                                        icon=ft.Icons.LOGOUT,
                                        on_click=self.handle_logout
                                    ),
                                ],
                                icon_color=ft.Colors.WHITE,
                                icon_size=20,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=10,
                )
            ],
            height=50,
        )
        
        return ft.Column(
            controls=[
                app_bar,
                ft.Row(
                    controls=[
                        nav_rail,
                        ft.VerticalDivider(width=1),
                        self.content_area
                    ],
                    expand=True,
                    spacing=0
                )
            ],
            spacing=0,
            expand=True
        )
    
    def load_dashboard_data(self):
        """Load dashboard data from API"""
        async def load_data():
            user_id = 'demo'
            if self.auth_service.supabase and hasattr(self.auth_service, 'current_user'):
                if hasattr(self.auth_service.current_user, 'id'):
                    user_id = self.auth_service.current_user.id
                else:
                    user_id = str(self.auth_service.current_user)
            
            print(f"📊 Loading dashboard data for user: {user_id}")
            summary_data = await self.api_client.get_summary(user_id)
            print(f"📊 Summary data: {summary_data}")
            self.balance = summary_data['balance']
            self.monthly_summary = summary_data['summary']
            print(f"📊 Balance: ${self.balance}, Monthly: {self.monthly_summary}")
            self.transactions = await self.api_client.get_transactions(user_id, 10)
            print(f"📊 Loaded {len(self.transactions)} transactions")
            self.update_overview_data()
        
        self.page.run_task(load_data)
    
    def update_overview_data(self):
        """Update overview UI with loaded data"""
        if hasattr(self, 'content_area') and self.current_view == "overview":
            self.content_area.content = self.build_overview()
            self.page.update()
    
    def build_overview(self):
        """Build overview dashboard"""
        # Get theme colors
        is_dark = self.page.is_dark_mode if hasattr(self.page, 'is_dark_mode') else False
        text_color = Theme.DARK_TEXT if is_dark else Theme.NOIR
        # Use light emerald background for light mode instead of white
        card_bg = Theme.DARK_SURFACE if is_dark else Theme.LIGHT_EMERALD_BG
        
        # Summary cards with theme-aware colors
        balance_card = self.create_stat_card(
            "Total Balance",
            f"${self.balance:,.2f}",
            ft.Icons.ACCOUNT_BALANCE_WALLET,
            Theme.WASABI if is_dark else Theme.EARTH
        )
        
        income = self.monthly_summary.get('income', 0)
        income_card = self.create_stat_card(
            "Monthly Income",
            f"${income:,.2f}",
            ft.Icons.TRENDING_UP,
            Theme.WASABI if is_dark else Theme.EMERALD
        )
        
        expenses = self.monthly_summary.get('expenses', 0)
        expenses_card = self.create_stat_card(
            "Monthly Expenses",
            f"${expenses:,.2f}",
            ft.Icons.TRENDING_DOWN,
            Theme.MAPLE if is_dark else Theme.MAPLE
        )
        
        savings_rate = self.monthly_summary.get('savings_rate', 0)
        savings_card = self.create_stat_card(
            "Savings Rate",
            f"{savings_rate:.1f}%",
            ft.Icons.SAVINGS,
            Theme.KHAKI if is_dark else Theme.KHAKI
        )
        
        transaction_controls = [
            ft.Text("Recent Transactions", size=20, weight=ft.FontWeight.BOLD, color=text_color),
            ft.Divider(color=Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
        ]
        
        for txn in self.transactions[:5]:
            amount_str = f"+${txn['amount']:,.2f}" if txn['transaction_type'] == 'income' else f"-${txn['amount']:,.2f}"
            txn_date = datetime.fromisoformat(txn['transaction_date']) if isinstance(txn['transaction_date'], str) else txn['transaction_date']
            transaction_controls.append(
                self.create_transaction_item(
                    txn['description'],
                    amount_str,
                    txn['category'],
                    txn_date
                )
            )
        
        transaction_controls.extend([
            ft.Container(height=10),
            ft.TextButton(
                "View All Transactions →",
                on_click=self.show_transactions_page
            )
        ])
        
        transactions_list = ft.Container(
            content=ft.Column(
                controls=transaction_controls,
                spacing=10
            ),
            bgcolor=card_bg,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        quick_actions = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Quick Actions", size=20, weight=ft.FontWeight.BOLD, color=text_color),
                    ft.Divider(color=Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
                    ft.ElevatedButton(
                        "Add Transaction",
                        icon=ft.Icons.ADD,
                        width=200,
                        on_click=self.show_transactions_page,
                        style=ft.ButtonStyle(
                            bgcolor=Theme.DARK_PRIMARY if is_dark else Theme.EMERALD, 
                            color=ft.Colors.WHITE
                        )
                    ),
                    ft.ElevatedButton(
                        "Import CSV",
                        icon=ft.Icons.UPLOAD_FILE,
                        width=200,
                        on_click=self.handle_csv_import,
                        style=ft.ButtonStyle(
                            bgcolor=Theme.WASABI if is_dark else ft.Colors.GREEN, 
                            color=ft.Colors.WHITE
                        )
                    ),
                    ft.ElevatedButton(
                        "Connect Bank (Plaid)",
                        icon=ft.Icons.ACCOUNT_BALANCE,
                        width=200,
                        on_click=self.handle_connect_bank,
                        style=ft.ButtonStyle(
                            bgcolor=Theme.KHAKI if is_dark else ft.Colors.ORANGE, 
                            color=Theme.NOIR
                        )
                    ),
                    ft.ElevatedButton(
                        "Manage Friends",
                        icon=ft.Icons.PEOPLE,
                        width=200,
                        on_click=self.handle_friends_dialog,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL, color=ft.Colors.WHITE)
                    ),
                    ft.ElevatedButton(
                        "AI Insights",
                        icon=ft.Icons.AUTO_AWESOME,
                        width=200,
                        style=ft.ButtonStyle(
                            bgcolor=Theme.EARTH if is_dark else ft.Colors.PURPLE, 
                            color=ft.Colors.WHITE
                        )
                    ),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=card_bg,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[balance_card, income_card, expenses_card, savings_card],
                    spacing=20,
                    wrap=True
                ),
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        ft.Container(content=quick_actions, expand=1),
                        ft.Container(content=transactions_list, expand=2)
                    ],
                    spacing=20,
                    expand=True
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    
    def create_stat_card(self, title: str, value: str, icon, color):
        """Create a statistics card"""
        is_dark = self.page.is_dark_mode if hasattr(self.page, 'is_dark_mode') else False
        text_color = Theme.DARK_TEXT if is_dark else Theme.NOIR
        card_bg = Theme.DARK_SURFACE if is_dark else Theme.LIGHT_EMERALD_BG
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icon, color=color, size=30),
                            ft.Container(expand=True),
                        ]
                    ),
                    ft.Text(title, size=14, color=Theme.DARK_TEXT if is_dark else ft.Colors.GREY_600),
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=text_color),
                ],
                spacing=10
            ),
            bgcolor=card_bg,
            padding=20,
            border_radius=10,
            width=250,
            border=ft.border.all(1, Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
    
    def create_transaction_item(self, title: str, amount: str, category: str, date: datetime):
        """Create a transaction list item"""
        is_dark = self.page.is_dark_mode if hasattr(self.page, 'is_dark_mode') else False
        text_color = Theme.DARK_TEXT if is_dark else Theme.NOIR
        is_income = amount.startswith("+")
        color = Theme.WASABI if is_income else Theme.MAPLE
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.ARROW_CIRCLE_UP if is_income else ft.Icons.ARROW_CIRCLE_DOWN,
                        color=color
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(title, weight=ft.FontWeight.BOLD, color=text_color),
                            ft.Text(category, size=12, color=Theme.DARK_TEXT if is_dark else ft.Colors.GREY_600)
                        ],
                        spacing=2,
                        expand=True
                    ),
                    ft.Text(amount, size=16, weight=ft.FontWeight.BOLD, color=color)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=10,
            border=ft.border.all(1, Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
            border_radius=8
        )
    
    def handle_friends_dialog(self, e):
        """Handle friends management dialog"""
        pass
    
    def handle_nav_change(self, e):
        """Handle navigation rail selection change"""
        self.switch_view(e.control.selected_index)
    
    def switch_view(self, index: int):
        """Switch between different views"""
        views = {
            0: "overview",
            1: "randy",
            2: "budgets",
            3: "insights"
        }
        
        self.current_view = views.get(index, "overview")
        
        if self.current_view == "overview":
            self.content_area.content = self.build_overview()
        elif self.current_view == "randy":
            self.content_area.content = RandyPage(self.page, self.auth_service)
        elif self.current_view == "budgets":
            self.content_area.content = BudgetsPage(self.page, self.auth_service)
        elif self.current_view == "insights":
            self.content_area.content = InsightsPage(self.page, self.auth_service)
        else:
            self.content_area.content = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.CONSTRUCTION, size=100, color=ft.Colors.GREY_400),
                        ft.Text(
                            f"{self.current_view.title()} view coming soon!",
                            size=24,
                            color=ft.Colors.GREY_600
                        ),
                        ft.Text(
                            "This feature is under development for the hackathon",
                            size=14,
                            color=ft.Colors.GREY_500
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        
        self.page.update()
    
    def show_transactions_page(self, e):
        """Show the full transactions page"""
        self.content_area.content = TransactionsPage(self.page, self.auth_service, self)
        self.page.update()
    
    def handle_load_sample(self, e):
        """Load sample transactions from CSV via API"""
        async def load_sample():
            try:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Loading sample data..."),
                    bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EARTH
                )
                self.page.snack_bar.open = True
                self.page.update()
                
                user_id = 'demo'
                if self.auth_service.supabase and hasattr(self.auth_service, 'current_user'):
                    if hasattr(self.auth_service.current_user, 'id'):
                        user_id = self.auth_service.current_user.id
                
                # Use the sample CSV file
                sample_path = "C:/dev/BudgetingSoftware/assets/data/sample_transactions.csv"
                print(f"🔵 Loading sample data from {sample_path}")
                
                result = await self.api_client.upload_csv(sample_path, user_id)
                
                if result.get('success'):
                    imported = result.get('imported', 0)
                    print(f"✅ Loaded {imported} sample transactions")
                    
                    self.load_dashboard_data()
                    
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"✅ Loaded {imported} sample transactions!"),
                        bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EMERALD,
                        duration=3000
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                else:
                    error = result.get('error', 'Unknown error')
                    print(f"❌ Error: {error}")
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"❌ Error: {error[:100]}"),
                        bgcolor=Theme.MAPLE,
                        duration=5000
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
            except Exception as ex:
                print(f"❌ Exception: {ex}")
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Failed: {str(ex)[:100]}"),
                    bgcolor=Theme.MAPLE,
                    duration=5000
                )
                self.page.snack_bar.open = True
                self.page.update()
        
        self.page.run_task(load_sample)
    
    def handle_csv_import(self, e):
        """Handle CSV import via FastAPI"""
        if not hasattr(self, 'file_picker'):
            self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
            self.page.overlay.append(self.file_picker)
            self.page.update()
        
        self.file_picker.pick_files(
            dialog_title="Select CSV File",
            allowed_extensions=["csv"],
            allow_multiple=False
        )
    
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        """Handle file selection and upload to API"""
        if not e.files or len(e.files) == 0:
            print("❌ No file selected")
            return
        
        file_info = e.files[0]
        file_path = file_info.path
        
        print(f"📁 File selected: {file_info.name}")
        print(f"📁 File path: {file_path}")
        
        # WORKAROUND: If path is None, use sample CSV directly
        if not file_path:
            print("⚠️ File path is None, using sample CSV as workaround")
            file_path = "C:/dev/BudgetingSoftware/assets/data/sample_transactions.csv"
            
            # Ask user if they want to proceed with sample data
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("⚠️ File picker returned no path. Loading sample CSV instead..."),
                bgcolor=ft.Colors.ORANGE,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        
        async def upload_to_api():
            try:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Uploading {file_info.name} to API..."),
                    bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EARTH
                )
                self.page.snack_bar.open = True
                self.page.update()
                
                user_id = 'demo'
                if self.auth_service.supabase and hasattr(self.auth_service, 'current_user'):
                    if hasattr(self.auth_service.current_user, 'id'):
                        user_id = self.auth_service.current_user.id
                
                print(f"🔵 Uploading CSV to API for user_id={user_id}")
                result = await self.api_client.upload_csv(file_path, user_id)
                
                if result.get('success'):
                    imported = result.get('imported', 0)
                    skipped = result.get('skipped', 0)
                    
                    print(f"✅ API imported {imported} transactions")
                    
                    self.load_dashboard_data()
                    
                    # Show alert dialog if all transactions were duplicates
                    if imported == 0 and skipped > 0:
                        def close_dialog(e):
                            duplicate_dialog.open = False
                            self.page.update()
                        
                        duplicate_dialog = ft.AlertDialog(
                            modal=True,
                            title=ft.Row([
                                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.ORANGE, size=30),
                                ft.Text("Duplicate Transactions Detected", size=20, weight=ft.FontWeight.BOLD)
                            ]),
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text(
                                        "You already uploaded these transactions!",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.ORANGE
                                    ),
                                    ft.Divider(),
                                    ft.Text(
                                        f"All {skipped} transactions in this CSV file already exist in your database.",
                                        size=16
                                    ),
                                    ft.Text(
                                        "No new transactions were added.",
                                        size=14,
                                        italic=True,
                                        color=ft.Colors.GREY_700
                                    )
                                ], spacing=10),
                                padding=10
                            ),
                            actions=[
                                ft.TextButton(
                                    "Got it!",
                                    on_click=close_dialog,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.ORANGE
                                    )
                                )
                            ],
                            actions_alignment=ft.MainAxisAlignment.END,
                        )
                        self.page.dialog = duplicate_dialog
                        duplicate_dialog.open = True
                        self.page.update()
                    else:
                        message = f"Imported {imported} transactions!"
                        if skipped > 0:
                            message += f" ({skipped} duplicates skipped)"
                        
                        self.page.snack_bar = ft.SnackBar(
                            content=ft.Text(message),
                            bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EMERALD,
                            duration=3000
                        )
                        self.page.snack_bar.open = True
                        self.page.update()
                else:
                    error = result.get('error', 'Unknown error')
                    print(f"❌ API Error: {error}")
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"❌ API Error: {error[:100]}"),
                        bgcolor=Theme.MAPLE,
                        duration=5000
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                
            except Exception as ex:
                error_msg = str(ex)
                print(f"❌ Upload Exception: {ex}")
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Upload failed: {error_msg[:100]}"),
                    bgcolor=Theme.MAPLE,
                    duration=5000
                )
                self.page.snack_bar.open = True
                self.page.update()
                import traceback
                traceback.print_exc()
        
        self.page.run_task(upload_to_api)
    
    def handle_connect_bank(self, e):
        """Handle bank connection via Plaid API"""
        print("🔵 Connect Bank clicked!")
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Connecting to Plaid via API..."),
            bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EARTH
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        async def connect_plaid():
            print("🔵 Starting Plaid connection...")
            
            user_id = 'demo'
            if self.auth_service.supabase and hasattr(self.auth_service, 'current_user'):
                if hasattr(self.auth_service.current_user, 'id'):
                    user_id = self.auth_service.current_user.id
                else:
                    user_id = str(self.auth_service.current_user)
            
            print(f"🔵 User ID: {user_id}")
            print("🔵 Calling API create_plaid_link_token...")
            
            link_token = await self.api_client.create_plaid_link_token(user_id)
            print(f"🔵 API response: {link_token}")
            
            if link_token:
                # Open Plaid Link in browser via API endpoint
                import webbrowser
                
                # Get user ID
                user_id = 'demo'
                if self.auth_service.supabase and hasattr(self.auth_service, 'current_user'):
                    if hasattr(self.auth_service.current_user, 'id'):
                        user_id = self.auth_service.current_user.id
                
                # Build URL through API
                plaid_url = f"http://localhost:8000/plaid-link?link_token={link_token}&user_id={user_id}"
                
                print(f"✅ Opening Plaid Link: {plaid_url}")
                webbrowser.open(plaid_url)
                
                # Show success message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("✅ Plaid Link opened in browser! Select your bank and log in."),
                    bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EMERALD,
                    duration=8000
                )
                self.page.snack_bar.open = True
                self.page.update()
                
                print(f"✅ Token: {link_token[:30]}...")
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("❌ Failed to create Plaid link token"),
                    bgcolor=Theme.MAPLE,
                    duration=5000
                )
                self.page.snack_bar.open = True
                self.page.update()
                print("❌ Link token creation failed")
        
        self.page.run_task(connect_plaid)
    
    def show_profile_page(self, e):
        """Show the profile page"""
        self.content_area.content = ProfilePage(self.page, self.auth_service, self)
        self.page.update()
    
    def show_settings_page(self, e):
        """Show the settings page"""
        self.content_area.content = SettingsPage(self.page, self.auth_service, self)
        self.page.update()
    
    def refresh_with_theme(self):
        """Refresh dashboard with current theme"""
        # Rebuild entire UI with new theme - just rebuild everything
        old_content = self.content
        self.content = self.build_ui()
        
        # Restore the current view
        if self.current_view == "overview":
            self.content_area.content = self.build_overview()
        elif self.current_view == "randy":
            self.content_area.content = RandyPage(self.page, self.auth_service)
        elif self.current_view == "budgets":
            self.content_area.content = BudgetsPage(self.page, self.auth_service)
        elif self.current_view == "insights":
            self.content_area.content = InsightsPage(self.page, self.auth_service)
        
        self.update()
        self.page.update()
    
    def close_dialog(self):
        """Close the open dialog"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    async def handle_logout(self, e):
        """Handle logout"""
        await self.auth_service.sign_out()
        self.page.go("/")
