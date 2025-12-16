"""Theme configuration - Color palettes for light and dark modes"""

import flet as ft


class Theme:
    """Theme configuration with color palettes"""
    
    # Base Colors (from your palette)
    EMERALD = "#284139"        # Emerald Green
    WASABI = "#8D9D76"         # Wasabi
    KHAKI = "#F8D794"          # Creased Khaki
    EARTH = "#BE8830"          # Egyptian Earth
    NOIR = "#111A19"           # Noir de Vigne
    MAPLE = "#692721"          # Maple Spice
    
    # Light Mode Colors - Lighter variations
    LIGHT_EMERALD = "#3A5A4F"     # Lighter emerald
    LIGHT_EMERALD_BG = "#E8F0ED"  # Very light emerald for backgrounds
    LIGHT_WASABI = "#A8B899"      # Lighter wasabi
    LIGHT_WASABI_BG = "#F2F5EF"   # Very light wasabi for backgrounds
    LIGHT_KHAKI = "#FBE9C0"       # Lighter khaki
    LIGHT_KHAKI_BG = "#FEF9F0"    # Very light khaki for backgrounds
    LIGHT_EARTH = "#D4A054"       # Lighter earth
    LIGHT_EARTH_BG = "#F8F0E5"    # Very light earth for backgrounds
    LIGHT_MAPLE = "#8B4035"       # Lighter maple
    
    # Dark Mode Colors
    DARK_BG = "#111A19"           # Dark background (Noir)
    DARK_SURFACE = "#1F2D2B"      # Slightly lighter for cards
    DARK_PRIMARY = "#8D9D76"      # Wasabi as primary
    DARK_SECONDARY = "#F8D794"    # Khaki as secondary
    DARK_ACCENT = "#BE8830"       # Earth as accent
    DARK_TEXT = "#F8D794"         # Light text
    
    @staticmethod
    def get_light_theme():
        """Get light theme configuration with lighter color variations"""
        return {
            "primary": Theme.LIGHT_EMERALD,
            "primary_light": Theme.LIGHT_EMERALD_BG,
            "secondary": Theme.LIGHT_WASABI,
            "secondary_light": Theme.LIGHT_WASABI_BG,
            "accent": Theme.LIGHT_EARTH,
            "accent_light": Theme.LIGHT_EARTH_BG,
            "khaki": Theme.LIGHT_KHAKI,
            "khaki_light": Theme.LIGHT_KHAKI_BG,
            "background": "#FFFFFF",
            "surface": "#FAFAFA",
            "card_bg": "#FFFFFF",
            "text": Theme.NOIR,
            "text_secondary": "#666666",
            "text_light": "#999999",
            "border": "#E0E0E0",
            "button_primary": Theme.LIGHT_EMERALD,
            "button_primary_hover": Theme.EMERALD,
            "button_secondary": Theme.LIGHT_WASABI,
            "button_accent": Theme.LIGHT_EARTH,
            "success": "#4CAF50",
            "warning": Theme.LIGHT_MAPLE,
            "error": "#D32F2F",
            "info": Theme.LIGHT_WASABI
        }
    
    @staticmethod
    def get_dark_theme():
        """Get dark theme configuration"""
        return {
            "primary": Theme.DARK_PRIMARY,
            "primary_light": Theme.DARK_SURFACE,
            "secondary": Theme.DARK_SECONDARY,
            "secondary_light": "#2A3532",
            "accent": Theme.DARK_ACCENT,
            "accent_light": "#3A3A2A",
            "khaki": Theme.DARK_SECONDARY,
            "khaki_light": "#3A3A2A",
            "background": Theme.DARK_BG,
            "surface": Theme.DARK_SURFACE,
            "card_bg": Theme.DARK_SURFACE,
            "text": Theme.DARK_TEXT,
            "text_secondary": "#AAAAAA",
            "text_light": "#777777",
            "border": "#2A3A37",
            "button_primary": Theme.DARK_PRIMARY,
            "button_primary_hover": "#9DB089",
            "button_secondary": Theme.DARK_SECONDARY,
            "button_accent": Theme.DARK_ACCENT,
            "success": "#66BB6A",
            "warning": "#FFA726",
            "error": "#EF5350",
            "info": Theme.DARK_PRIMARY
        }
    
    @staticmethod
    def apply_theme(page: ft.Page, is_dark_mode: bool):
        """Apply theme to the page"""
        if is_dark_mode:
            theme = Theme.get_dark_theme()
            page.theme_mode = ft.ThemeMode.DARK
        else:
            theme = Theme.get_light_theme()
            page.theme_mode = ft.ThemeMode.LIGHT
        
        # Store theme in page data for access across components
        page.theme_colors = theme
        page.update()
        
        return theme
