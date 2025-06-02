
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface SettingsContextType {
  theme: 'light' | 'dark';
  language: 'ru' | 'en';
  fontSize: 'small' | 'medium' | 'large' | 'xlarge';
  setTheme: (theme: 'light' | 'dark') => void;
  setLanguage: (language: 'ru' | 'en') => void;
  setFontSize: (fontSize: 'small' | 'medium' | 'large' | 'xlarge') => void;
}

const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

export const useSettings = () => {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettings must be used within a SettingsProvider');
  }
  return context;
};

interface SettingsProviderProps {
  children: ReactNode;
}

const SETTINGS_COOKIE_NAME = 'app_settings';
const COOKIE_EXPIRY_DAYS = 14;

const setCookie = (name: string, value: string, days: number) => {
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Strict`;
};

const getCookie = (name: string): string | null => {
  const nameEQ = name + '=';
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
};

export const SettingsProvider: React.FC<SettingsProviderProps> = ({ children }) => {
  const [theme, setThemeState] = useState<'light' | 'dark'>('light');
  const [language, setLanguageState] = useState<'ru' | 'en'>('ru');
  const [fontSize, setFontSizeState] = useState<'small' | 'medium' | 'large' | 'xlarge'>('medium');

  // Загружаем настройки из куков при инициализации
  useEffect(() => {
    const savedSettings = getCookie(SETTINGS_COOKIE_NAME);
    if (savedSettings) {
      try {
        const settings = JSON.parse(decodeURIComponent(savedSettings));
        setThemeState(settings.theme || 'light');
        setLanguageState(settings.language || 'ru');
        setFontSizeState(settings.fontSize || 'medium');
      } catch (error) {
        console.error('Error parsing saved settings:', error);
      }
    }
  }, []);

  // Сохраняем настройки в куки при изменении
  const saveSettings = (newTheme: string, newLanguage: string, newFontSize: string) => {
    const settings = {
      theme: newTheme,
      language: newLanguage,
      fontSize: newFontSize,
    };
    setCookie(SETTINGS_COOKIE_NAME, encodeURIComponent(JSON.stringify(settings)), COOKIE_EXPIRY_DAYS);
  };

  const setTheme = (newTheme: 'light' | 'dark') => {
    setThemeState(newTheme);
    saveSettings(newTheme, language, fontSize);
  };

  const setLanguage = (newLanguage: 'ru' | 'en') => {
    setLanguageState(newLanguage);
    saveSettings(theme, newLanguage, fontSize);
  };

  const setFontSize = (newFontSize: 'small' | 'medium' | 'large' | 'xlarge') => {
    setFontSizeState(newFontSize);
    saveSettings(theme, language, newFontSize);
  };

  useEffect(() => {
    // Применяем тему к документу
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  useEffect(() => {
    // Применяем размер шрифта к документу
    const root = document.documentElement;
    root.classList.remove('text-small', 'text-medium', 'text-large', 'text-xlarge');
    
    switch (fontSize) {
      case 'small':
        root.style.fontSize = '14px';
        break;
      case 'medium':
        root.style.fontSize = '16px';
        break;
      case 'large':
        root.style.fontSize = '18px';
        break;
      case 'xlarge':
        root.style.fontSize = '20px';
        break;
    }
  }, [fontSize]);

  return (
    <SettingsContext.Provider value={{
      theme,
      language,
      fontSize,
      setTheme,
      setLanguage,
      setFontSize
    }}>
      {children}
    </SettingsContext.Provider>
  );
};
