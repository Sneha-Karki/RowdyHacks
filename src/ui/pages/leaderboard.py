"""Insights page - Brand leaderboard"""

import flet as ft
from datetime import datetime
from collections import defaultdict
from ...services.api_client import APIClient


class InsightsPage(ft.Container):
    """Brand leaderboard - Top brands by spending"""
    
    def __init__(self, page: ft.Page, auth_service):
        super().__init__()
        self.page = page
        self.auth_service = auth_service
        self.api_client = APIClient()
        self.transactions = []
        self.brand_totals = {}
        
        # Build UI
        self.content = self.build_ui()
        self.expand = True
        self.bgcolor = ft.Colors.WHITE
        self.padding = 30
        self.border_radius = 10
        
        # Load data
        self.load_brand_data()
    
    def build_ui(self):
        """Build the insights page UI"""
        self.leaderboard_content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.ProgressRing()
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=15,
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
                                    "🏆 Brand Leaderboard",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK
                                ),
                                ft.Text(
                                    "Most popular brands • Ranked by consistency",
                                    size=16,
                                    color=ft.Colors.GREY_600
                                )
                            ],
                            spacing=5
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Refresh",
                            on_click=lambda _: self.load_brand_data()
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(),
                # Leaderboard content
                ft.Container(
                    content=self.leaderboard_content,
                    expand=True
                )
            ],
            spacing=10,
            expand=True
        )
    
    def load_brand_data(self):
        """Load transactions and calculate brand totals"""
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
            
            # Calculate totals by brand (use description as brand name)
            brand_totals = defaultdict(lambda: {'total': 0, 'count': 0})
            for txn in self.transactions:
                if txn['transaction_type'] == 'expense':
                    brand = txn.get('description', 'Unknown')
                    brand_totals[brand]['total'] += txn['amount']
                    brand_totals[brand]['count'] += 1
            
            self.brand_totals = dict(brand_totals)
            self.update_leaderboard_display()
        
        self.page.run_task(fetch_data)
    
    def update_leaderboard_display(self):
        """Update the leaderboard display"""
        if not self.brand_totals:
            self.leaderboard_content.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.LEADERBOARD, size=100, color=ft.Colors.GREY_400),
                            ft.Text("No spending data yet", size=20, color=ft.Colors.GREY_600),
                            ft.Text("Import transactions to see your brand leaderboard", size=14, color=ft.Colors.GREY_500)
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
            # Sort brands by consistency (transaction count) instead of spending
            sorted_brands = sorted(
                self.brand_totals.items(), 
                key=lambda x: x[1]['count'], 
                reverse=True
            )
            
            # Calculate total transactions for percentage
            total_transactions = sum(data['count'] for data in self.brand_totals.values())
            
            # Create leaderboard entries
            leaderboard_items = []
            
            # Medal emojis for top 3
            medals = {0: "🥇", 1: "🥈", 2: "🥉"}
            
            for idx, (brand, data) in enumerate(sorted_brands[:20]):  # Top 20
                rank = idx + 1
                amount = data['total']
                count = data['count']
                percentage = (count / total_transactions * 100) if total_transactions > 0 else 0
                
                # Get medal or rank number
                rank_display = medals.get(idx, f"#{rank}")
                
                # Choose color based on rank
                if rank == 1:
                    rank_color = ft.Colors.AMBER_400
                    bg_color = ft.Colors.AMBER_50
                elif rank == 2:
                    rank_color = ft.Colors.GREY_400
                    bg_color = ft.Colors.GREY_50
                elif rank == 3:
                    rank_color = ft.Colors.ORANGE_400
                    bg_color = ft.Colors.ORANGE_50
                else:
                    rank_color = ft.Colors.BLUE_400
                    bg_color = ft.Colors.BLUE_50
                
                leaderboard_items.append(
                    self.create_leaderboard_item(
                        rank_display,
                        brand,
                        amount,
                        count,
                        percentage,
                        rank_color,
                        bg_color
                    )
                )
            
            # Promotional/News cards
            promo_cards = ft.Row(
                controls=[
                    self.create_promo_card(
                        "💰 Save 20% at Target",
                        "Use code SAVE20 at checkout",
                        ft.Colors.RED_400
                    ),
                    self.create_promo_card(
                        "🎉 Amazon Prime Day",
                        "Exclusive deals detected!",
                        ft.Colors.ORANGE_400
                    ),
                    self.create_promo_card(
                        "🔥 Flash Sale Alert",
                        "Walmart: 30% off groceries",
                        ft.Colors.BLUE_400
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
            )
            
            self.leaderboard_content.controls = [
                promo_cards,
                ft.Container(height=20),
                ft.Text(
                    "Most Consistent Brands",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
                ft.Text(
                    "Ranked by purchase frequency from 25 users",
                    size=14,
                    color=ft.Colors.GREY_500
                ),
                ft.Container(height=10),
                *leaderboard_items
            ]
        
        self.leaderboard_content.update()
    
    def create_promo_card(self, title: str, subtitle: str, color):
        """Create a promotional/news card"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        title,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        subtitle,
                        size=12,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            bgcolor=ft.Colors.with_opacity(0.1, color),
            padding=20,
            border_radius=10,
            width=250,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
            ),
            border=ft.border.all(2, color)
        )
    
    def create_leaderboard_item(self, rank_display: str, brand: str, amount: float, count: int, percentage: float, rank_color, bg_color):
        """Create a leaderboard item"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Rank
                    ft.Container(
                        content=ft.Text(
                            rank_display,
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=rank_color
                        ),
                        width=60,
                        alignment=ft.alignment.center
                    ),
                    # Brand info
                    ft.Column(
                        controls=[
                            ft.Text(
                                brand,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK
                            ),
                            ft.Text(
                                f"{count} transaction{'s' if count != 1 else ''}",
                                size=12,
                                color=ft.Colors.GREY_600
                            )
                        ],
                        spacing=2,
                        expand=True
                    ),
                    # Amount and percentage
                    ft.Column(
                        controls=[
                            ft.Text(
                                f"${amount:,.2f}",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=rank_color,
                                text_align=ft.TextAlign.RIGHT
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"{percentage:.1f}%",
                                    size=12,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=rank_color,
                                padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                border_radius=10
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=5
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=bg_color,
            padding=20,
            border_radius=12,
            width=700,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            ),
            border=ft.border.all(2, rank_color),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        )
