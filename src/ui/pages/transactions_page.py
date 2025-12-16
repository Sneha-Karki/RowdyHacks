"""Transactions page - View all transactions"""

import flet as ft
from datetime import datetime
from ...services.api_client import APIClient
from ..theme import Theme


class TransactionsPage(ft.Container):
    """Full transactions view page"""
    
    def __init__(self, page: ft.Page, auth_service, dashboard=None):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.api_client = APIClient()
        self.transactions = []
        self.dashboard = dashboard  # Reference to dashboard for refreshing overview
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        # Use theme-aware background
        is_dark = page.is_dark_mode if hasattr(page, 'is_dark_mode') else False
        self.bgcolor = Theme.DARK_SURFACE if is_dark else Theme.LIGHT_EMERALD_BG
        self.padding = 20
        self.border_radius = 10
        
        # Load transactions
        self.load_transactions()
    
    def build_ui(self):
        """Build the transactions page UI"""
        is_dark = self.page.is_dark_mode if hasattr(self.page, 'is_dark_mode') else False
        text_color = Theme.DARK_TEXT if is_dark else Theme.NOIR
        
        self.transactions_column = ft.Column(
            controls=[
                ft.ProgressRing()
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        return ft.Column(
            controls=[
                # Header
                ft.Row(
                    controls=[
                        ft.Text(
                            "All Transactions",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=text_color
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Add Transaction",
                            icon=ft.Icons.ADD,
                            on_click=lambda e: self.show_add_transaction_dialog(),
                            style=ft.ButtonStyle(
                                bgcolor=Theme.DARK_PRIMARY if is_dark else Theme.EMERALD,
                                color=ft.Colors.WHITE
                            )
                        ),
                        ft.Container(width=10),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Refresh",
                            on_click=lambda _: self.load_transactions(),
                            icon_color=text_color
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(color=Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
                # Transactions list
                ft.Container(
                    content=self.transactions_column,
                    expand=True
                )
            ],
            spacing=10,
            expand=True
        )
    
    def load_transactions(self):
        """Load all transactions from API"""
        async def fetch_transactions():
            user_id = 'demo'
            if self.auth_service.supabase and hasattr(self.auth_service, 'current_user'):
                if self.auth_service.current_user:
                    if hasattr(self.auth_service.current_user, 'id'):
                        user_id = self.auth_service.current_user.id
                    else:
                        user_id = str(self.auth_service.current_user)
            
            await self.reload_transactions_async(user_id)
        
        self.page.run_task(fetch_transactions)
    
    async def reload_transactions_async(self, user_id):
        """Async method to reload transactions"""
        self.transactions = await self.api_client.get_transactions(user_id, 100)
        self.update_transactions_list()
        self.page.update()
    
    def update_transactions_list(self):
        """Update the transactions list UI"""
        is_dark = self.page.is_dark_mode if hasattr(self.page, 'is_dark_mode') else False
        text_color = Theme.DARK_TEXT if is_dark else Theme.NOIR
        card_bg = Theme.DARK_SURFACE if is_dark else Theme.LIGHT_WASABI_BG
        
        if not self.transactions:
            self.transactions_column.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, size=100, color=Theme.DARK_TEXT if is_dark else ft.Colors.GREY_400),
                            ft.Text("No transactions yet", size=20, color=text_color),
                            ft.Text("Import CSV or connect your bank to get started", size=14, color=Theme.DARK_TEXT if is_dark else ft.Colors.GREY_500)
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
            transaction_items = []
            for txn in self.transactions:
                amount_str = f"+${txn['amount']:,.2f}" if txn['transaction_type'] == 'income' else f"-${txn['amount']:,.2f}"
                is_income = txn['transaction_type'] == 'income'
                color = Theme.WASABI if is_income else Theme.MAPLE
                
                txn_date = datetime.fromisoformat(txn['transaction_date']) if isinstance(txn['transaction_date'], str) else txn['transaction_date']
                
                transaction_items.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.ARROW_CIRCLE_UP if is_income else ft.Icons.ARROW_CIRCLE_DOWN,
                                    color=color,
                                    size=30
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(txn['description'], weight=ft.FontWeight.BOLD, size=16, color=text_color),
                                        ft.Row(
                                            controls=[
                                                ft.Text(txn['category'], size=12, color=Theme.DARK_TEXT if is_dark else ft.Colors.GREY_600),
                                                ft.Text("•", size=12, color=Theme.DARK_TEXT if is_dark else ft.Colors.GREY_400),
                                                ft.Text(txn_date.strftime("%b %d, %Y"), size=12, color=Theme.DARK_TEXT if is_dark else ft.Colors.GREY_600)
                                            ],
                                            spacing=5
                                        )
                                    ],
                                    spacing=2,
                                    expand=True
                                ),
                                ft.Text(amount_str, size=18, weight=ft.FontWeight.BOLD, color=color)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=15,
                        border=ft.border.all(1, Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
                        border_radius=8,
                        bgcolor=card_bg,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=2,
                            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
                        )
                    )
                )
            
            self.transactions_column.controls = transaction_items
        
        self.transactions_column.update()
    
    def show_add_transaction_dialog(self):
        """Show dialog to add a new transaction using BottomSheet for web compatibility"""
        
        # Form fields
        description_input = ft.TextField(
            label="Description *",
            hint_text="e.g., Grocery shopping",
            width=400
        )
        
        amount_input = ft.TextField(
            label="Amount *",
            hint_text="e.g., 50.00",
            prefix_text="$",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=400
        )
        
        category_dropdown = ft.Dropdown(
            label="Category *",
            hint_text="Select a category",
            width=400,
            options=[
                ft.dropdown.Option("Food"),
                ft.dropdown.Option("Groceries"),
                ft.dropdown.Option("Transportation"),
                ft.dropdown.Option("Car"),
                ft.dropdown.Option("Shopping"),
                ft.dropdown.Option("Entertainment"),
                ft.dropdown.Option("Healthcare"),
                ft.dropdown.Option("Utilities"),
                ft.dropdown.Option("Housing"),
                ft.dropdown.Option("Education"),
                ft.dropdown.Option("Travel"),
                ft.dropdown.Option("Personal"),
                ft.dropdown.Option("Other"),
            ]
        )
        
        transaction_type_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="expense", label="Expense"),
                ft.Radio(value="income", label="Income"),
            ]),
            value="expense"
        )
        
        date_input = ft.TextField(
            label="Date *",
            hint_text="YYYY-MM-DD",
            value=datetime.now().strftime("%Y-%m-%d"),
            width=400
        )
        
        def save_transaction(e):
            # Validate required fields
            if not description_input.value or not amount_input.value or not category_dropdown.value:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("❌ Please fill in all required fields"),
                    bgcolor=Theme.MAPLE
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            try:
                amount = float(amount_input.value)
                
                # Create transaction data
                async def add_transaction():
                    try:
                        user_id = 'demo'
                        if self.auth_service.supabase and hasattr(self.auth_service, 'current_user'):
                            if self.auth_service.current_user:
                                if hasattr(self.auth_service.current_user, 'id'):
                                    user_id = self.auth_service.current_user.id
                                else:
                                    user_id = str(self.auth_service.current_user)
                        
                        # Insert directly to Supabase
                        from src.database.transaction_service import TransactionService
                        transaction_service = TransactionService()
                        
                        # Parse the date string
                        transaction_date = datetime.strptime(date_input.value, "%Y-%m-%d")
                        
                        success = await transaction_service.add_transaction(
                            user_id=user_id,
                            description=description_input.value,
                            amount=amount,
                            category=category_dropdown.value,
                            transaction_type=transaction_type_radio.value,
                            date=transaction_date
                        )
                        
                        if success:
                            # Close bottom sheet first
                            bottom_sheet.open = False
                            self.page.update()
                            
                            # Show success message
                            self.page.snack_bar = ft.SnackBar(
                                content=ft.Text(f"✅ Transaction added: {description_input.value}"),
                                bgcolor=Theme.WASABI if self.page.is_dark_mode else Theme.EMERALD
                            )
                            self.page.snack_bar.open = True
                            self.page.update()
                            
                            # Reload transactions to show the new one
                            await self.reload_transactions_async(user_id)
                            
                            # Refresh the dashboard overview if we have a reference
                            if self.dashboard:
                                self.dashboard.load_dashboard_data()
                        else:
                            self.page.snack_bar = ft.SnackBar(
                                content=ft.Text("❌ Failed to add transaction"),
                                bgcolor=Theme.MAPLE
                            )
                            self.page.snack_bar.open = True
                            self.page.update()
                    
                    except Exception as ex:
                        self.page.snack_bar = ft.SnackBar(
                            content=ft.Text(f"❌ Error: {str(ex)}"),
                            bgcolor=Theme.MAPLE
                        )
                        self.page.snack_bar.open = True
                        self.page.update()
                
                self.page.run_task(add_transaction)
                
            except ValueError:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("❌ Please enter a valid amount"),
                    bgcolor=Theme.MAPLE
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
                                    "Add New Transaction",
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
                            "Fill in the form below to add a new transaction",
                            size=14,
                            color=Theme.DARK_TEXT if self.page.is_dark_mode else Theme.NOIR
                        ),
                        ft.Text(
                            "* Required fields",
                            size=12,
                            color=Theme.MAPLE,
                            italic=True
                        ),
                        ft.Container(height=10),
                        description_input,
                        amount_input,
                        category_dropdown,
                        ft.Container(height=5),
                        ft.Text("Transaction Type: *", size=14, weight=ft.FontWeight.BOLD),
                        transaction_type_radio,
                        ft.Container(height=5),
                        date_input,
                        ft.Container(height=20),
                        ft.Row(
                            controls=[
                                ft.TextButton(
                                    "Cancel",
                                    on_click=close_bottom_sheet,
                                    style=ft.ButtonStyle(color=Theme.DARK_TEXT if self.page.is_dark_mode else Theme.NOIR)
                                ),
                                ft.ElevatedButton(
                                    "Add Transaction",
                                    icon=ft.Icons.ADD,
                                    on_click=save_transaction,
                                    style=ft.ButtonStyle(
                                        bgcolor=Theme.DARK_PRIMARY if self.page.is_dark_mode else Theme.EMERALD,
                                        color=ft.Colors.WHITE
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    tight=True,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=30,
                width=700
            ),
            open=True,
            dismissible=True,
            on_dismiss=close_bottom_sheet
        )
        
        self.page.overlay.append(bottom_sheet)
        self.page.update()
