"""Budget page - View spending by category"""

import flet as ft
from datetime import datetime
from collections import defaultdict
from ...services.api_client import APIClient


class BudgetsPage(ft.Container):
    """Budget breakdown by category"""
    
    def __init__(self, page: ft.Page, auth_service):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.api_client = APIClient()
        self.transactions = []
        self.category_totals = {}
        
        # Category colors and icons
        self.category_config = {
            'Food & Drinks': {'color': ft.Colors.ORANGE_400, 'icon': ft.Icons.RESTAURANT},
            'Food': {'color': ft.Colors.ORANGE_400, 'icon': ft.Icons.RESTAURANT},
            'Groceries': {'color': ft.Colors.ORANGE_600, 'icon': ft.Icons.SHOPPING_CART},
            'Car': {'color': ft.Colors.BLUE_400, 'icon': ft.Icons.DIRECTIONS_CAR},
            'Transportation': {'color': ft.Colors.BLUE_600, 'icon': ft.Icons.COMMUTE},
            'School': {'color': ft.Colors.PURPLE_400, 'icon': ft.Icons.SCHOOL},
            'Education': {'color': ft.Colors.PURPLE_600, 'icon': ft.Icons.MENU_BOOK},
            'House': {'color': ft.Colors.GREEN_400, 'icon': ft.Icons.HOME},
            'Housing': {'color': ft.Colors.GREEN_600, 'icon': ft.Icons.HOUSE},
            'Rent': {'color': ft.Colors.GREEN_700, 'icon': ft.Icons.HOME_WORK},
            'Shopping': {'color': ft.Colors.PINK_400, 'icon': ft.Icons.SHOPPING_BAG},
            'Entertainment': {'color': ft.Colors.INDIGO_400, 'icon': ft.Icons.MOVIE},
            'Healthcare': {'color': ft.Colors.RED_400, 'icon': ft.Icons.MEDICAL_SERVICES},
            'Health': {'color': ft.Colors.RED_600, 'icon': ft.Icons.FAVORITE},
            'Utilities': {'color': ft.Colors.CYAN_400, 'icon': ft.Icons.BOLT},
            'Bills': {'color': ft.Colors.CYAN_600, 'icon': ft.Icons.RECEIPT},
            'Travel': {'color': ft.Colors.TEAL_400, 'icon': ft.Icons.FLIGHT},
            'Fitness': {'color': ft.Colors.LIME_400, 'icon': ft.Icons.FITNESS_CENTER},
            'Personal': {'color': ft.Colors.AMBER_400, 'icon': ft.Icons.PERSON},
            'Other': {'color': ft.Colors.BROWN_400, 'icon': ft.Icons.MORE_HORIZ}
        }
        
        # Nice colors for auto-assignment
        self.color_palette = [
            ft.Colors.ORANGE_400,
            ft.Colors.BLUE_400,
            ft.Colors.PURPLE_400,
            ft.Colors.GREEN_400,
            ft.Colors.PINK_400,
            ft.Colors.INDIGO_400,
            ft.Colors.RED_400,
            ft.Colors.CYAN_400,
            ft.Colors.TEAL_400,
            ft.Colors.AMBER_400,
            ft.Colors.LIME_400,
            ft.Colors.DEEP_ORANGE_400,
            ft.Colors.LIGHT_BLUE_400,
            ft.Colors.DEEP_PURPLE_400,
            ft.Colors.LIGHT_GREEN_400
        ]
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        self.bgcolor = ft.Colors.WHITE
        self.padding = 30
        self.border_radius = 10
        
        # Load data
        self.load_budget_data()
    
    def build_ui(self):
        """Build the budget page UI"""
        self.budget_content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.ProgressRing()
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        return ft.Column(
            controls=[
                # Header
                ft.Row(
                    controls=[
                        ft.Text(
                            "Budget Breakdown",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Refresh",
                            on_click=lambda _: self.load_budget_data()
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Text(
                    "See how much you've spent in each category",
                    size=16,
                    color="#F8A5C2"  # Pink hex color #F8A5C2
  # Pink hex color #F8A5C2
                ),
                ft.Divider(),
                # Budget content
                ft.Container(
                    content=self.budget_content,
                    expand=True
                )
            ],
            spacing=10,
            expand=True
        )
    
    def load_budget_data(self):
        """Load transactions and calculate category totals"""
        async def fetch_data():
            user_id = 'demo'
            if self.auth_service.supabase and hasattr(self.auth_service, 'current_user'):
                if self.auth_service.current_user:
                    if hasattr(self.auth_service.current_user, 'id'):
                        user_id = self.auth_service.current_user.id
                    else:
                        user_id = str(self.auth_service.current_user)
            
            # Get all transactions
            self.transactions = await self.api_client.get_transactions(user_id, 1000)
            
            # Calculate totals by category (only expenses)
            category_totals = defaultdict(float)
            for txn in self.transactions:
                if txn['transaction_type'] == 'expense':
                    category = txn.get('category', 'Other')
                    category_totals[category] += txn['amount']
            
            self.category_totals = dict(category_totals)
            self.update_budget_display()
        
        self.page.run_task(fetch_data)
    
    def update_budget_display(self):
        """Update the budget display with category ovals"""
        if not self.category_totals:
            self.budget_content.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, size=100, color=ft.Colors.GREY_400),
                            ft.Text("No spending data yet", size=20, color=ft.Colors.GREY_600),
                            ft.Text("Import transactions to see your budget breakdown", size=14, color=ft.Colors.GREY_500)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                    padding=50,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        else:
            # Calculate total spending
            total_spending = sum(self.category_totals.values())
            
            # Create total spending card
            total_card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Total Spending", size=18, color=ft.Colors.GREY_700),
                        ft.Text(f"${total_spending:,.2f}", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                        ft.Text("Across all categories", size=14, color=ft.Colors.GREY_500)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                bgcolor=ft.Colors.BLUE_50,
                padding=30,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
                )
            )
            
            # Sort categories by spending (highest first)
            sorted_categories = sorted(self.category_totals.items(), key=lambda x: x[1], reverse=True)
            
            # Create oval cards for each category
            category_ovals = []
            for idx, (category, amount) in enumerate(sorted_categories):
                # Get category config or assign a nice color
                if category in self.category_config:
                    config = self.category_config[category]
                else:
                    # Assign a nice color from the palette based on index
                    color_idx = idx % len(self.color_palette)
                    config = {
                        'color': self.color_palette[color_idx],
                        'icon': ft.Icons.CATEGORY
                    }
                
                # Calculate percentage of total
                percentage = (amount / total_spending * 100) if total_spending > 0 else 0
                
                oval = self.create_category_oval(
                    category,
                    amount,
                    percentage,
                    config['color'],
                    config['icon']
                )
                category_ovals.append(oval)
            
            # Create grid layout for ovals
            oval_rows = []
            for i in range(0, len(category_ovals), 3):
                row_ovals = category_ovals[i:i+3]
                oval_rows.append(
                    ft.Row(
                        controls=row_ovals,
                        spacing=20,
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
            
            self.budget_content.controls = [
                ft.Container(
                    content=total_card,
                    alignment=ft.alignment.center
                ),
                ft.Container(height=20),
                ft.Container(
                    content=ft.Text(
                        "Spending by Category",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    alignment=ft.alignment.center
                ),
                *oval_rows
            ]
        
        self.budget_content.update()
    
    def create_category_oval(self, category: str, amount: float, percentage: float, color, icon):
        """Create an oval card for a category"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, size=50, color=color),
                    ft.Text(
                        category,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        f"${amount:,.2f}",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=color,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(
                        content=ft.Text(
                            f"{percentage:.1f}%",
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.WHITE
                        ),
                        bgcolor=color,
                        padding=ft.padding.symmetric(horizontal=15, vertical=5),
                        border_radius=20
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=100,  # Oval shape
            width=250,
            height=250,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                offset=ft.Offset(0, 5)
            ),
            border=ft.border.all(3, color),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )