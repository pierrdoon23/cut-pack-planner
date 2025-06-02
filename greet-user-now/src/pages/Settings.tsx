
import React from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { useSettings } from '@/contexts/SettingsContext';
import { getTranslation } from '@/utils/translations';

const Settings: React.FC = () => {
  const { theme, language, fontSize, setTheme, setLanguage, setFontSize } = useSettings();

  const applySettings = () => {
    console.log('Применение настроек:', { theme, language, fontSize });
    alert(getTranslation(language, 'settingsSaved'));
  };

  const resetSettings = () => {
    setTheme('light');
    setLanguage('ru');
    setFontSize('medium');
    alert(getTranslation(language, 'settingsReset'));
  };

  return (
    <div className="p-6 bg-white dark:bg-gray-900 text-gray-900 dark:text-white min-h-full">
      <h1 className="text-2xl font-bold mb-6">{getTranslation(language, 'settings')}</h1>
      
      <div className="max-w-md space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2">{getTranslation(language, 'themeSettings')}</label>
          <div className="flex items-center space-x-2">
            <span className="text-sm">{getTranslation(language, 'light')}</span>
            <Switch 
              checked={theme === 'dark'} 
              onCheckedChange={(checked) => setTheme(checked ? 'dark' : 'light')}
            />
            <span className="text-sm">{getTranslation(language, 'dark')}</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">{getTranslation(language, 'languageSettings')}</label>
          <Select value={language} onValueChange={setLanguage}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ru">Русский</SelectItem>
              <SelectItem value="en">English</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">{getTranslation(language, 'fontSizeSettings')}</label>
          <Select value={fontSize} onValueChange={setFontSize}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="small">{getTranslation(language, 'small')}</SelectItem>
              <SelectItem value="medium">{getTranslation(language, 'medium')}</SelectItem>
              <SelectItem value="large">{getTranslation(language, 'large')}</SelectItem>
              <SelectItem value="xlarge">{getTranslation(language, 'xlarge')}</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2 pt-4">
          <Button onClick={applySettings} className="w-full bg-blue-600 hover:bg-blue-700">
            {getTranslation(language, 'applySettings')}
          </Button>
          <Button onClick={resetSettings} variant="destructive" className="w-full">
            {getTranslation(language, 'resetSettings')}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
