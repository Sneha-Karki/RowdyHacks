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
        self.category_budgets = {}  # Store budget goals for each category
        
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
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Monthly Budget Breakdown",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK
                                ),
                                ft.Text(
                                    f"{datetime.now().strftime('%B %Y')}",
                                    size=14,
                                    color=ft.Colors.GREY_600
                                )
                            ],
                            spacing=5
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
            
            # Get current month/year for filtering
            now = datetime.now()
            current_month = now.month
            current_year = now.year
            
            # Calculate totals by category (only expenses from current month)
            category_totals = defaultdict(float)
            for txn in self.transactions:
                if txn['transaction_type'] == 'expense':
                    # Parse transaction date
                    txn_date = datetime.fromisoformat(txn['transaction_date']) if isinstance(txn['transaction_date'], str) else txn['transaction_date']
                    
                    # Only include current month transactions
                    if txn_date.month == current_month and txn_date.year == current_year:
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
        # Get budget goal for this category
        budget_goal = self.category_budgets.get(category, 0)
        
        # Determine if over budget
        is_over_budget = budget_goal > 0 and amount > budget_goal
        is_within_budget = budget_goal > 0 and amount <= budget_goal
        
        # Budget indicator arrow
        budget_indicator = None
        if is_over_budget:
            budget_indicator = ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ARROW_UPWARD, size=20, color=ft.Colors.RED),
                    ft.Text(
                        f"${amount - budget_goal:,.2f} over",
                        size=12,
                        color=ft.Colors.RED,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            )
        elif is_within_budget:
            budget_indicator = ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ARROW_DOWNWARD, size=20, color=ft.Colors.GREEN),
                    ft.Text(
                        f"${budget_goal - amount:,.2f} under",
                        size=12,
                        color=ft.Colors.GREEN,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            )
        
        controls = [
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
        ]
        
        # Add budget goal if set
        if budget_goal > 0:
            controls.append(
                ft.Text(
                    f"Goal: ${budget_goal:,.2f}",
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                )
            )
        
        # Add budget indicator
        if budget_indicator:
            controls.append(budget_indicator)
        else:
            controls.append(
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
            )
        
        # Add "Set Limit" button
        controls.append(
            ft.Container(height=5)
        )
        controls.append(
            ft.ElevatedButton(
                "Set Limit",
                icon=ft.Icons.EDIT,
                on_click=lambda _: self.show_budget_dialog(category, amount, budget_goal, color),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    color=color
                ),
                height=30
            )
        )
        
        return ft.Container(
            content=ft.Column(
                controls=controls,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=100,  # Oval shape
            width=250,
            height=320,  # Increased height for budget button
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                offset=ft.Offset(0, 5)
            ),
            border=ft.border.all(3, color),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )
    
    def show_budget_dialog(self, category: str, current_amount: float, current_budget: float, color):
        """Show dialog to set budget limit for category using BottomSheet for web compatibility"""
        
        budget_input = ft.TextField(
            label=f"Monthly Limit for {category}",
            hint_text="Enter amount (e.g., 500)",
            value=str(int(current_budget)) if current_budget > 0 else "",
            prefix_text="$",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=400
        )
        
        def save_budget(e):
            try:
                new_budget = float(budget_input.value) if budget_input.value else 0
                self.category_budgets[category] = new_budget
                
                # Show success message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"✅ Limit set for {category}: ${new_budget:,.2f}"),
                    bgcolor=ft.Colors.GREEN
                )
                self.page.snack_bar.open = True
                
                # Close bottom sheet and refresh
                bottom_sheet.open = False
                self.page.update()
                self.update_budget_display()
                
            except ValueError:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("❌ Please enter a valid number"),
                    bgcolor=ft.Colors.RED
                )
                self.page.snack_bar.open = True
                self.page.update()
        
        def close_bottom_sheet(e):
            bottom_sheet.open = False
            if self.page:
                self.page.update()
        
        bottom_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"Set Monthly Limit for {category}",
                                    size=24,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    on_click=close_bottom_sheet,
                                    tooltip="Close"
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Divider(),
                        ft.Text(
                            f"Current spending this month: ${current_amount:,.2f}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Container(height=15),
                        ft.Text(
                            "Enter your monthly spending limit:",
                            size=14,
                            color=ft.Colors.GREY_700
                        ),
                        ft.Container(height=5),
                        budget_input,
                        ft.Container(height=15),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.INFO_OUTLINED, size=16, color=ft.Colors.BLUE_400),
                                    ft.Container(width=5),
                                    ft.Text(
                                        "Set a realistic monthly limit to track your spending",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                        italic=True
                                    )
                                ]
                            ),
                            bgcolor=ft.Colors.BLUE_50,
                            padding=10,
                            border_radius=8
                        ),
                        ft.Container(height=10),
                        ft.Text(
                            "• Green arrow ↓ = Under budget\n• Red arrow ↑ = Over budget",
                            size=11,
                            color=ft.Colors.GREY_600
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            controls=[
                                ft.TextButton(
                                    "Cancel",
                                    on_click=close_bottom_sheet,
                                    style=ft.ButtonStyle(color=ft.Colors.GREY_700)
                                ),
                                ft.ElevatedButton(
                                    "Set Limit",
                                    icon=ft.Icons.CHECK,
                                    on_click=save_budget,
                                    style=ft.ButtonStyle(bgcolor=color, color=ft.Colors.WHITE)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    tight=True,
                    spacing=5
                ),
                padding=30,
                width=600
            ),
            open=True,
            dismissible=True,
            on_dismiss=close_bottom_sheet
        )
        
        self.page.overlay.append(bottom_sheet)
        self.page.update()
