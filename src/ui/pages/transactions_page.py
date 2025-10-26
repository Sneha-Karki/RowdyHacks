"""Transactions page - View all transactions"""

import flet as ft
from datetime import datetime
from ...services.api_client import APIClient


class TransactionsPage(ft.Container):
    """Full transactions view page"""
    
    def __init__(self, page: ft.Page, auth_service):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.api_client = APIClient()
        self.transactions = []
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        self.bgcolor = ft.Colors.WHITE
        self.padding = 20
        self.border_radius = 10
        
        # Load transactions
        self.load_transactions()
    
    def build_ui(self):
        """Build the transactions page UI"""
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
                            color=ft.Colors.BLACK
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Refresh",
                            on_click=lambda _: self.load_transactions()
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(),
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
            
            self.transactions = await self.api_client.get_transactions(user_id, 100)
            self.update_transactions_list()
        
        self.page.run_task(fetch_transactions)
    
    def update_transactions_list(self):
        """Update the transactions list UI"""
        if not self.transactions:
            self.transactions_column.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, size=100, color=ft.Colors.GREY_400),
                            ft.Text("No transactions yet", size=20, color=ft.Colors.GREY_600),
                            ft.Text("Import CSV or connect your bank to get started", size=14, color=ft.Colors.GREY_500)
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
                color = ft.Colors.GREEN if is_income else ft.Colors.RED
                
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
                                        ft.Text(txn['description'], weight=ft.FontWeight.BOLD, size=16),
                                        ft.Row(
                                            controls=[
                                                ft.Text(txn['category'], size=12, color=ft.Colors.GREY_600),
                                                ft.Text("•", size=12, color=ft.Colors.GREY_400),
                                                ft.Text(txn_date.strftime("%b %d, %Y"), size=12, color=ft.Colors.GREY_600)
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
                        border=ft.border.all(1, ft.Colors.GREY_200),
                        border_radius=8,
                        bgcolor=ft.Colors.WHITE,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=2,
                            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
                        )
                    )
                )
            
            self.transactions_column.controls = transaction_items
        
        self.transactions_column.update()
