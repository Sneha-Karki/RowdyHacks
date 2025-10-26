import flet as ft
from src.ui.theme import Theme

class RandyPet(ft.Container):
    def __init__(self, happiness=100, energy=100, budget_health=100, page=None):
        super().__init__()
        self.happiness = happiness
        self.energy = energy
        self.budget_health = budget_health
        self.page = page
        self.expressions = {
            'happy': '🤠🐍',
            'tired': '😴🐍',
            'worried': '😟🐍',
            'excited': '🤩🐍'
        }
        self.content = self.build()
        
    def get_expression(self):
        if self.happiness > 80:
            return self.expressions['happy']
        elif self.energy < 30:
            return self.expressions['tired']
        elif self.budget_health < 50:
            return self.expressions['worried']
        return self.expressions['happy']
    
    def feed(self, e):
        self.energy = min(100, self.energy + 20)
        self.happiness = min(100, self.happiness + 10)
        self.update_stats()
        
    def update_stats(self):
        self.stats_text.value = f"Happiness: {self.happiness}% | Energy: {self.energy}% | Budget Health: {self.budget_health}%"
        self.pet_expression.value = self.get_expression()
        self.update()
        
    def build(self):
        is_dark = self.page.is_dark_mode if self.page and hasattr(self.page, 'is_dark_mode') else False
        text_color = Theme.DARK_TEXT if is_dark else Theme.NOIR
        card_bg = Theme.DARK_SURFACE if is_dark else Theme.LIGHT_WASABI_BG
        accent_color = Theme.DARK_PRIMARY if is_dark else Theme.EMERALD
        
        self.pet_expression = ft.Text(
            value=self.get_expression(),
            size=50,
            text_align=ft.TextAlign.CENTER,
        )
        
        self.stats_text = ft.Text(
            value=f"Happiness: {self.happiness}% | Energy: {self.energy}% | Budget Health: {self.budget_health}%",
            size=16,
            color=text_color
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.pet_expression,
                        padding=20,
                        border_radius=10,
                        bgcolor=Theme.DARK_BG if is_dark else Theme.LIGHT_KHAKI_BG,
                    ),
                    self.stats_text,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Feed Randy 🍎",
                                on_click=self.feed,
                                color=ft.Colors.WHITE,
                                bgcolor=Theme.WASABI if is_dark else Theme.EMERALD
                            ),
                            ft.ElevatedButton(
                                "Talk to Randy 💬",
                                on_click=lambda _: print("Chat feature coming soon!"),
                                color=ft.Colors.WHITE,
                                bgcolor=Theme.DARK_PRIMARY if is_dark else Theme.EARTH
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            border=ft.border.all(1, Theme.DARK_PRIMARY if is_dark else Theme.LIGHT_EMERALD),
            border_radius=10,
            bgcolor=card_bg,
        )