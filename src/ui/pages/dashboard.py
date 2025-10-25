"""Dashboard page - main app interface"""

import flet as ft
from datetime import datetime


class DashboardPage(ft.Container):
    """Main dashboard with navigation and content area"""
    
    def __init__(self, page: ft.Page, auth_service):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.current_view = "overview"
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        self.bgcolor = ft.Colors.GREY_50
    
    def build_ui(self):
        """Build the dashboard UI"""
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
                    icon=ft.Icons.RECEIPT_LONG_OUTLINED,
                    selected_icon=ft.Icons.RECEIPT_LONG,
                    label="Transactions"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CATEGORY_OUTLINED,
                    selected_icon=ft.Icons.CATEGORY,
                    label="Budgets"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INSIGHTS_OUTLINED,
                    selected_icon=ft.Icons.INSIGHTS,
                    label="Insights"
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
                            ft.PopupMenuItem(),  # Divider
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
            )
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
    
    def build_overview(self):
        """Build overview dashboard"""
        # Summary cards
        balance_card = self.create_stat_card(
            "Total Balance",
            "$5,432.00",
            ft.Icons.ACCOUNT_BALANCE_WALLET,
            ft.Colors.BLUE
        )
        
        income_card = self.create_stat_card(
            "Monthly Income",
            "$3,200.00",
            ft.Icons.TRENDING_UP,
            ft.Colors.GREEN
        )
        
        expenses_card = self.create_stat_card(
            "Monthly Expenses",
            "$2,150.00",
            ft.Icons.TRENDING_DOWN,
            ft.Colors.RED
        )
        
        savings_card = self.create_stat_card(
            "Savings Rate",
            "32.8%",
            ft.Icons.SAVINGS,
            ft.Colors.PURPLE
        )
        
        # Recent transactions
        transactions_list = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Recent Transactions", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    self.create_transaction_item("Grocery Store", "-$125.50", "Food", datetime.now()),
                    self.create_transaction_item("Salary", "+$3,200.00", "Income", datetime.now()),
                    self.create_transaction_item("Electric Bill", "-$89.00", "Utilities", datetime.now()),
                    self.create_transaction_item("Coffee Shop", "-$15.75", "Food", datetime.now()),
                    ft.Container(height=10),
                    ft.TextButton(
                        "View All Transactions →",
                        on_click=lambda _: self.switch_view(1)
                    )
                ],
                spacing=10
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        # Quick actions
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
                        "AI Insights",
                        icon=ft.Icons.AUTO_AWESOME,
                        width=200,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE, color=ft.Colors.WHITE)
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
                # Summary cards row
                ft.Row(
                    controls=[balance_card, income_card, expenses_card, savings_card],
                    spacing=20,
                    wrap=True
                ),
                ft.Container(height=20),
                # Content row
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
            1: "transactions",
            2: "budgets",
            3: "insights"
        }
        
        self.current_view = views.get(index, "overview")
        
        if self.current_view == "overview":
            self.content_area.content = self.build_overview()
        else:
            # Placeholder for other views
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
    
    def handle_csv_import(self, e):
        """Handle CSV import"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("CSV import feature coming soon!"),
            bgcolor=ft.Colors.BLUE
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    async def handle_logout(self, e):
        """Handle logout"""
        await self.auth_service.sign_out()
        self.page.go("/")
