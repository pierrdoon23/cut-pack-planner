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
        'subtitle': "Оптимизация карт раскроя для минимизации отходов",
        'src_rolls': "Исходные рулоны",
        'target_rolls': "Целевые рулоны",
        'select': "Выбрать",
        'set': "Задать",
        'params': "Параметры",
        'new_map': "🞣 Новая карта",
        'export': "⎙ Экспорт",
        'optimize': "✂️ Оптимизировать",
        'result': "Результаты оптимизации\nЭффективность: 100%, Отходы: 0 мм",
        'theme': "Тема",
        'language': "Язык",
        'settings': "⚙️ Настройки",
        'api_url': "API URL",
        'port': "Порт",
        'report': "📊 Отчет",
        'report_text': "Здесь вы можете увидеть подробный отчет об операциях.",
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
        'subtitle': "Optimizing layouts to minimize waste",
        'src_rolls': "Source Rolls",
        'target_rolls': "Target Rolls",
        'select': "Select",
        'set': "Set",
        'params': "Parameters",
        'new_map': "🞣 New Map",
        'export': "⎙ Export",
        'optimize': "✂️ Optimize",
        'result': "Optimization Results\nEfficiency: 100%, Waste: 0 mm",
        'theme': "Theme",
        'language': "Language",
        'settings': "⚙️ Settings",
        'api_url': "API URL",
        'port': "Port",
        'report': "📊 Report",
        'report_text': "Here you can see a detailed report of operations."
    }
}

current_language = 'ru'

def tr(key):
    return translations[current_language].get(key, key)