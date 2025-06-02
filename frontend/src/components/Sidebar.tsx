
import React from 'react';
import { Home, FileText, Wrench, BarChart3, Settings, Users, LogOut } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useSettings } from '@/contexts/SettingsContext';
import { getTranslation } from '@/utils/translations';

interface SidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
  username: string;
  onLogout: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeSection, onSectionChange, username, onLogout }) => {
  const { language } = useSettings();

  const menuItems = [
    { id: 'main', label: getTranslation(language, 'mainPage'), icon: Home },
    { id: 'cutting-maps', label: getTranslation(language, 'cuttingMaps'), icon: FileText },
    { id: 'resources', label: getTranslation(language, 'resources'), icon: Wrench },
    { id: 'reports', label: getTranslation(language, 'reports'), icon: BarChart3 },
    { id: 'settings', label: getTranslation(language, 'settings'), icon: Settings },
    { id: 'users', label: getTranslation(language, 'users'), icon: Users },
  ];

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return getTranslation(language, 'goodMorning');
    if (hour < 18) return getTranslation(language, 'goodAfternoon');
    return getTranslation(language, 'goodEvening');
  };

  return (
    <div className="w-64 bg-blue-600 dark:bg-blue-800 text-white min-h-screen flex flex-col">
      <div className="p-4 border-b border-blue-500 dark:border-blue-700">
        <div className="text-sm opacity-80">{getGreeting()}, {username}</div>
      </div>
      
      <nav className="mt-4 flex-1">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onSectionChange(item.id)}
            className={cn(
              "w-full flex items-center px-4 py-3 text-left hover:bg-blue-700 dark:hover:bg-blue-900 transition-colors",
              activeSection === item.id && "bg-blue-800 dark:bg-blue-900"
            )}
          >
            <item.icon className="w-5 h-5 mr-3" />
            {item.label}
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-blue-500 dark:border-blue-700">
        <button
          onClick={onLogout}
          className="w-full flex items-center px-4 py-3 text-left hover:bg-blue-700 dark:hover:bg-blue-900 transition-colors rounded"
        >
          <LogOut className="w-5 h-5 mr-3" />
          {getTranslation(language, 'logout')}
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
