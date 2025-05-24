# Localization
translations = {
    'ru': {
        'statistics': "\U0001F4CA Главная Страница",
        'plan_completion': "Выполнение плана по дням недели",
        'rolls': "Рулоны",
        'cutting_maps': "Карты раскроя",
        'packages': "Пакеты",
        'cutting_types': "Типы нарезки",
        'usage_and_waste': "Отходы и использование",
        'visualization': "Карты раскроя",
        'src_rolls': "Исходные рулоны",
        'target_rolls': "Целевые рулоны",
        'machine': "Станок",
        'select': "Выбрать",
        'set': "Задать",
        'params': "Параметры",
        'new_map': "🞣 Новая карта",
        'export': "⎙ Экспорт",
        'optimize': "✂️ Оптимизировать",
        'theme': "Тема",
        'language': "Язык",
        'settings': "⚙️ Настройки",
        'api_url': "API URL",
        'port': "Порт",
        'report': "📊 Отчет",
        'report_text': "Здесь вы можете увидеть подробный отчет об операциях.",
        'load_maps': 'Загрузить карты',
        'create': 'Создать'
    },
    'en': {
        'statistics': "\U0001F4CA Main Page",
        'plan_completion': "Plan Completion by Weekday",
        'rolls': "Rolls",
        'cutting_maps': "Cutting Maps",
        'packages': "Packages",
        'cutting_types': "Cutting Types",
        'usage_and_waste': "Usage and Waste",
        'visualization': "Cutting Layout",
        'src_rolls': "Source Rolls",
        'target_rolls': "Target Rolls",
        'machine': "Machine",
        'select': "Select",
        'set': "Set",
        'params': "Parameters",
        'new_map': "🞣 New Map",
        'export': "⎙ Export",
        'optimize': "✂️ Optimize",
        'theme': "Theme",
        'language': "Language",
        'settings': "⚙️ Settings",
        'api_url': "API URL",
        'port': "Port",
        'report': "📊 Report",
        'report_text': "Here you can see a detailed report of operations.",
        'load_maps': 'Load Cards',
        'create': 'Create'
    }
}

current_language = 'ru'

def tr(key):
    return translations[current_language].get(key, key)