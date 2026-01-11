# 앱 전체 테마 및 공통 스타일
theme = {
    'colors': {
        'primary': '#2196F3',
        'secondary': '#FF5722',
        'background': '#F5F5F5',
        'card_background': '#FFFFFF',
        'text': '#212121',
        'text_secondary': '#757575',
        'border': '#E0E0E0',
        'success': '#4CAF50',
        'warning': '#FFC107',
        'error': '#F44336',
    },
    'spacing': {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
    },
    'border_radius': {
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 24,
    },
    'font_size': {
        'xs': 12,
        'sm': 14,
        'md': 16,
        'lg': 20,
        'xl': 24,
        'xxl': 32,
    },
    'font_weight': {
        'normal': 'normal',
        'medium': 'medium',
        'bold': 'bold',
    },
}

# 색상 헥스코드를 RGB 튜플로 변환
def hex_to_rgb(hex_color: str) -> tuple:
    """#RRGGBB 형식을 (R, G, B) 튜플로 변환"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))