"""Dashboard page - main app interface"""

import flet as ft
from datetime import datetime
from src.ui.components.randy_pet import RandyPet
from src.ui.pages.randy_page import RandyPage
from src.ui.pages.transactions_page import TransactionsPage
from src.ui.pages.budget import BudgetsPage
from src.ui.pages.leaderboard import InsightsPage
from src.ui.pages.profile import ProfilePage
from ...services.api_client import APIClient


class DashboardPage(ft.Container):
    """Main dashboard with navigation and content area"""
    
    def __init__(self, page: ft.Page, auth_service):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.api_client = APIClient()
        self.current_view = "overview"
        
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
        return ft.Stack([
            # Background image
            ft.Image(
                src="starry-background.png",
                width=float("inf"),
                height=float("inf"),
                fit=ft.ImageFit.COVER,
            ),
            # Main content
            self.build_main_content()
        ])
    
    def build_main_content(self):
        """Build main content area"""
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
            bgcolor=ft.Colors.WHITE
        )
        
        # Main content area
        self.content_area = ft.Container(
            content=self.build_overview(),
            expand=True,
            padding=30
        )
        
        # Top app bar
        app_bar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "Budget Buddy",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.UPLOAD_FILE,
                        tooltip="Import CSV",
                        on_click=self.handle_csv_import
                    ),
                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                        tooltip="Notifications"
                    ),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Profile", icon=ft.Icons.PERSON),
                            ft.PopupMenuItem(text="Settings", icon=ft.Icons.SETTINGS),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                text="Sign Out",
                                icon=ft.Icons.LOGOUT,
                                on_click=self.handle_logout
                            ),
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            bgcolor=ft.Colors.WHITE,
            padding=15,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            ),
            # Add background image using decoration
            decoration=ft.BoxDecoration(
                image=ft.DecorationImage(
                    src="nav-banner.png",     # path to your image
                    fit=ft.ImageFit.COVER,          # or CONTAIN, FILL, etc.
                    opacity=0.9                     # optional transparency
                ),
                border_radius=ft.border_radius.all(0)  # optional rounding
            ),
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
            
            summary_data = await self.api_client.get_summary(user_id)
            self.balance = summary_data['balance']
            self.monthly_summary = summary_data['summary']
            self.transactions = await self.api_client.get_transactions(user_id, 10)
            self.update_overview_data()
        
        self.page.run_task(load_data)
    
    def update_overview_data(self):
        """Update overview UI with loaded data"""
        if hasattr(self, 'content_area') and self.current_view == "overview":
            self.content_area.content = self.build_overview()
            self.page.update()
    
    def build_overview(self):
        """Build overview dashboard"""
        # Summary cards
        balance_card = self.create_stat_card(
            "Total Balance",
            f"${self.balance:,.2f}",
            ft.Icons.ACCOUNT_BALANCE_WALLET,
            ft.Colors.BLUE
        )
        
        income = self.monthly_summary.get('income', 0)
        income_card = self.create_stat_card(
            "Monthly Income",
            f"${income:,.2f}",
            ft.Icons.TRENDING_UP,
            ft.Colors.GREEN
        )
        
        expenses = self.monthly_summary.get('expenses', 0)
        expenses_card = self.create_stat_card(
            "Monthly Expenses",
            f"${expenses:,.2f}",
            ft.Icons.TRENDING_DOWN,
            ft.Colors.RED
        )
        
        savings_rate = self.monthly_summary.get('savings_rate', 0)
        savings_card = self.create_stat_card(
            "Savings Rate",
            f"{savings_rate:.1f}%",
            ft.Icons.SAVINGS,
            ft.Colors.PURPLE
        )
        
        transaction_controls = [
            ft.Text("Recent Transactions", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
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
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        quick_actions = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Quick Actions", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.ElevatedButton(
                        "Add Transaction",
                        icon=ft.Icons.ADD,
                        width=200,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
                    ),
                    ft.ElevatedButton(
                        "Import CSV",
                        icon=ft.Icons.UPLOAD_FILE,
                        width=200,
                        on_click=self.handle_csv_import,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
                    ),
                    ft.ElevatedButton(
                        "Connect Bank (Plaid)",
                        icon=ft.Icons.ACCOUNT_BALANCE,
                        width=200,
                        on_click=self.handle_connect_bank,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE)
                    ),
                    ft.ElevatedButton(
                        "AI Insights",
                        icon=ft.Icons.AUTO_AWESOME,
                        width=200,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE, color=ft.Colors.WHITE)
                    ),
                    ft.ElevatedButton(
                        "Manage Friends",
                        icon=ft.Icons.PEOPLE,
                        width=200,
                        on_click=self.handle_friends_dialog,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL, color=ft.Colors.WHITE)
                    ),
                ],
                spacing=15
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
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
                        ft.Container(content=transactions_list, expand=2),
                        ft.Container(content=quick_actions, expand=1)
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
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icon, color=color, size=30),
                            ft.Container(expand=True),
                        ]
                    ),
                    ft.Text(title, size=14, color=ft.Colors.GREY_600),
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD),
                ],
                spacing=10
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            width=250,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
    
    def create_transaction_item(self, title: str, amount: str, category: str, date: datetime):
        """Create a transaction list item"""
        is_income = amount.startswith("+")
        color = ft.Colors.GREEN if is_income else ft.Colors.RED
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.ARROW_CIRCLE_UP if is_income else ft.Icons.ARROW_CIRCLE_DOWN,
                        color=color
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(title, weight=ft.FontWeight.BOLD),
                            ft.Text(category, size=12, color=ft.Colors.GREY_600)
                        ],
                        spacing=2,
                        expand=True
                    ),
                    ft.Text(amount, size=16, weight=ft.FontWeight.BOLD, color=color)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_200),
            border_radius=8
        )
    
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
        self.content_area.content = TransactionsPage(self.page, self.auth_service)
        self.page.update()
    
    def handle_load_sample(self, e):
        """Load sample transactions from CSV via API"""
        async def load_sample():
            try:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Loading sample data..."),
                    bgcolor=ft.Colors.BLUE
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
                        bgcolor=ft.Colors.GREEN,
                        duration=3000
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                else:
                    error = result.get('error', 'Unknown error')
                    print(f"❌ Error: {error}")
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"❌ Error: {error[:100]}"),
                        bgcolor=ft.Colors.RED,
                        duration=5000
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
            except Exception as ex:
                print(f"❌ Exception: {ex}")
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Failed: {str(ex)[:100]}"),
                    bgcolor=ft.Colors.RED,
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
                    bgcolor=ft.Colors.BLUE
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
                    
                    message = f"✅ Imported {imported} transactions!"
                    if skipped > 0:
                        message += f" ({skipped} skipped)"
                    
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(message),
                        bgcolor=ft.Colors.GREEN,
                        duration=3000
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                else:
                    error = result.get('error', 'Unknown error')
                    print(f"❌ API Error: {error}")
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"❌ API Error: {error[:100]}"),
                        bgcolor=ft.Colors.RED,
                        duration=5000
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                
            except Exception as ex:
                error_msg = str(ex)
                print(f"❌ Upload Exception: {ex}")
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Upload failed: {error_msg[:100]}"),
                    bgcolor=ft.Colors.RED,
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
            bgcolor=ft.Colors.BLUE
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
                    bgcolor=ft.Colors.GREEN,
                    duration=8000
                )
                self.page.snack_bar.open = True
                self.page.update()
                
                print(f"✅ Token: {link_token[:30]}...")
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("❌ Failed to create Plaid link token"),
                    bgcolor=ft.Colors.RED,
                    duration=5000
                )
                self.page.snack_bar.open = True
                self.page.update()
                print("❌ Link token creation failed")
        
        self.page.run_task(connect_plaid)
    
    def close_dialog(self):
        """Close the open dialog"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    def handle_friends_dialog(self, e):
        """Show the friends management dialog"""
        # Friend list data structure
        self.friends_list = getattr(self, 'friends_list', [
            {"email": "friend@example.com", "status": "Active", "shared_budgets": ["Monthly Budget"]},
            {"email": "pending@example.com", "status": "Pending", "shared_budgets": []}
        ])

        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        def add_friend(e):
            email = email_field.value.strip()
            if email:
                # In a real implementation, this would send an invitation via the API
                self.friends_list.append({
                    "email": email,
                    "status": "Pending",
                    "shared_budgets": []
                })
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"✉️ Invitation sent to {email}"),
                        bgcolor=ft.Colors.GREEN,
                        duration=3000
                    )
                )
                email_field.value = ""
                rebuild_friends_list()
                self.page.update()

        def share_budget(email):
            def handle_share(e):
                # This would integrate with your budget sharing API
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"📊 Budget shared with {email}"),
                        bgcolor=ft.Colors.GREEN,
                        duration=3000
                    )
                )
                self.page.update()
            return handle_share

        def remove_friend(email):
            def handle_remove(e):
                self.friends_list = [f for f in self.friends_list if f["email"] != email]
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"❌ Removed {email} from friends"),
                        bgcolor=ft.Colors.RED,
                        duration=3000
                    )
                )
                rebuild_friends_list()
                self.page.update()
            return handle_remove

        email_field = ft.TextField(
            label="Friend's Email",
            hint_text="Enter your friend's email",
            width=300,
            border_color=ft.Colors.BLUE,
            prefix_icon=ft.Icons.EMAIL,
            suffix_text="@example.com"
        )

        friends_column = ft.Column(spacing=5)

        def rebuild_friends_list():
            friends_column.controls = [
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE,
                                color=ft.Colors.BLUE if friend["status"] == "Active" else ft.Colors.GREY_400
                            ),
                            ft.Column([
                                ft.Text(friend["email"], weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    friend["status"],
                                    size=12,
                                    color=ft.Colors.GREEN if friend["status"] == "Active" else ft.Colors.ORANGE,
                                    italic=True
                                )
                            ], spacing=2),
                            ft.Container(expand=True),
                            ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(
                                        text="Share Budget",
                                        icon=ft.Icons.SHARE,
                                        on_click=share_budget(friend["email"])
                                    ),
                                    ft.PopupMenuItem(
                                        text="View Shared",
                                        icon=ft.Icons.FOLDER_SHARED,
                                        disabled=not friend["shared_budgets"]
                                    ),
                                    ft.PopupMenuItem(),  # Divider
                                    ft.PopupMenuItem(
                                        text="Remove",
                                        icon=ft.Icons.PERSON_REMOVE,
                                        on_click=remove_friend(friend["email"])
                                    ),
                                ]
                            )
                        ]),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Shared Budgets:", size=12, color=ft.Colors.GREY_600),
                                ft.Text(
                                    ", ".join(friend["shared_budgets"]) if friend["shared_budgets"] else "No shared budgets",
                                    size=12,
                                    italic=True
                                )
                            ]) if friend["status"] == "Active" else None,
                            padding=ft.padding.only(left=40)
                        )
                    ]),
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=10
                )
                for friend in self.friends_list
            ]

        rebuild_friends_list()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Budget Collaboration", size=24, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Add a friend to collaborate", size=16, weight=ft.FontWeight.W_500),
                    ft.Row([
                        email_field,
                        ft.ElevatedButton(
                            "Send Invite",
                            icon=ft.Icons.PERSON_ADD,
                            on_click=add_friend,
                            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE)
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Text("Your Budget Partners", size=16, weight=ft.FontWeight.W_500),
                    friends_column,
                    ft.Container(
                        content=ft.Text(
                            "💡 Share your budgets and financial goals with trusted friends to stay motivated and accountable!",
                            size=12,
                            color=ft.Colors.GREY_600,
                            italic=True
                        ),
                        margin=ft.margin.only(top=20)
                    )
                ], scroll=ft.ScrollMode.AUTO),
                width=400,
                height=500,
                padding=20
            ),
            actions=[
                ft.TextButton("Close", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog.open = True
        self.page.update()

    async def handle_logout(self, e):
        """Handle logout"""
        await self.auth_service.sign_out()
        self.page.go("/")