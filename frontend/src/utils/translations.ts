export const translations = {
  ru: {
    // Навигация
    mainPage: 'Главная страница',
    cuttingMaps: 'Задачи',
    resources: 'Создание ресурсов',
    reports: 'Отчеты',
    settings: 'Настройки',
    users: 'Пользователи',
    logout: 'Выйти',
    
    // Приветствие
    goodMorning: 'Доброе утро',
    goodAfternoon: 'Добрый день',
    goodEvening: 'Добрый вечер',
    
    // Настройки
    theme: 'Тема',
    themeSettings: 'Тема оформления:',
    light: 'Светлая',
    dark: 'Темная',
    languageSettings: 'Язык интерфейса:',
    language: 'Язык',
    fontSizeSettings: 'Размер шрифта:',
    fontSize: 'Размер шрифта',
    small: 'Маленький',
    medium: 'Средний',
    large: 'Большой',
    xlarge: 'Очень большой',
    applySettings: 'Применить настройки',
    resetSettings: 'Сбросить настройки',
    settingsSaved: 'Настройки сохранены!',
    settingsReset: 'Настройки сброшены!',
    
    // Ресурсы
    quantity: 'Количество',
    weight: 'Вес',
    status: 'Статус',
    readyToUse: 'Готов к использованию',
    inProgress: 'В процессе',
    edit: 'Редактировать',
    delete: 'Удалить',
    rawRolls: 'Сырьевые рулоны',
    targetRolls: 'Целевые рулоны',
    machines: 'Станки',
    addRawRoll: 'Добавить сырьевой рулон',
    addTargetRoll: 'Добавить целевой рулон',
    addMachine: 'Добавить станок',
    name: 'Название',
    width: 'Ширина',
    thickness: 'Толщина',
    material: 'Материал',
    targetWidth: 'Целевая ширина',
    targetThickness: 'Целевая толщина',
    priority: 'Приоритет',
    low: 'Низкий',
    high: 'Высокий',
    machineType: 'Тип станка',
    maxWidth: 'Максимальная ширина',
    efficiency: 'Эффективность',
    active: 'Активен',
    maintenance: 'Техобслуживание',
    inactive: 'Неактивен',
    add: 'Добавить',
    cancel: 'Отмена',
    create: 'Создать',
    
    // Отчеты
    generatePDF: 'Генерировать PDF',
    pdfGenerated: 'PDF отчет создан и сохранен!',
    generatingPDF: 'Генерация PDF отчета...'
  },
  en: {
    // Navigation
    mainPage: 'Main Page',
    cuttingMaps: 'Tasks',
    resources: 'Resource Creation',
    reports: 'Reports',
    settings: 'Settings',
    users: 'Users',
    logout: 'Logout',
    
    // Greeting
    goodMorning: 'Good morning',
    goodAfternoon: 'Good afternoon',
    goodEvening: 'Good evening',
    
    // Settings
    theme: 'Theme',
    themeSettings: 'Theme Settings:',
    light: 'Light',
    dark: 'Dark',
    languageSettings: 'Interface Language:',
    language: 'Language',
    fontSizeSettings: 'Font Size:',
    fontSize: 'Font Size',
    small: 'Small',
    medium: 'Medium',
    large: 'Large',
    xlarge: 'Extra Large',
    applySettings: 'Apply Settings',
    resetSettings: 'Reset Settings',
    settingsSaved: 'Settings saved!',
    settingsReset: 'Settings reset!',
    
    // Resources
    quantity: 'Quantity',
    weight: 'Weight',
    status: 'Status',
    readyToUse: 'Ready to use',
    inProgress: 'In progress',
    edit: 'Edit',
    delete: 'Delete',
    rawRolls: 'Raw Rolls',
    targetRolls: 'Target Rolls',
    machines: 'Machines',
    addRawRoll: 'Add Raw Roll',
    addTargetRoll: 'Add Target Roll',
    addMachine: 'Add Machine',
    name: 'Name',
    width: 'Width',
    thickness: 'Thickness',
    material: 'Material',
    targetWidth: 'Target Width',
    targetThickness: 'Target Thickness',
    priority: 'Priority',
    low: 'Low',
    high: 'High',
    machineType: 'Machine Type',
    maxWidth: 'Max Width',
    efficiency: 'Efficiency',
    active: 'Active',
    maintenance: 'Maintenance',
    inactive: 'Inactive',
    add: 'Add',
    cancel: 'Cancel',
    create: 'Create'
  }
};

export const getTranslation = (language: 'ru' | 'en', key: string): string => {
  const keys = key.split('.');
  let value: any = translations[language];
  
  for (const k of keys) {
    value = value?.[k];
  }
  
  return value || key;
};
