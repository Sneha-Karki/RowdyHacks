import flet as ft

class RandyPet(ft.Container):
    def __init__(self, happiness=100, energy=100, budget_health=100):
        super().__init__()
        self.happiness = happiness
        self.energy = energy
        self.budget_health = budget_health
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
        self.pet_expression = ft.Text(
            value=self.get_expression(),
            size=50,
            text_align=ft.TextAlign.CENTER,
        )
        
        self.stats_text = ft.Text(
            value=f"Happiness: {self.happiness}% | Energy: {self.energy}% | Budget Health: {self.budget_health}%",
            size=16,
            color=ft.Colors.BLUE_GREY_400
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.pet_expression,
                        padding=20,
                        border_radius=10,
                        bgcolor=ft.Colors.BLUE_50,
                    ),
                    self.stats_text,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Feed Randy 🍎",
                                on_click=self.feed,
                                color=ft.Colors.GREEN
                            ),
                            ft.ElevatedButton(
                                "Talk to Randy 💬",
                                on_click=lambda _: print("Chat feature coming soon!"),
                                color=ft.Colors.BLUE
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            border=ft.border.all(1, ft.Colors.BLUE_200),
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
        )