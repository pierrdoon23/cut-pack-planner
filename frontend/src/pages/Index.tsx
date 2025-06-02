
import React, { useState } from 'react';
import LoginForm from '@/components/LoginForm';
import Sidebar from '@/components/Sidebar';
import MainPage from './MainPage';
import CuttingMaps from './CuttingMaps';
import Resources from './Resources';
import Reports from './Reports';
import Settings from './Settings';
import Users from './Users';
import { SettingsProvider } from '@/contexts/SettingsContext';
import { useAuth } from '@/hooks/useAuth';

const Index = () => {
  const { isAuthenticated, user, login, logout } = useAuth();
  const [activeSection, setActiveSection] = useState('main');

  const handleLogin = (username: string, password: string) => {
    login(username, password);
  };

  const handleLogout = () => {
    logout();
    setActiveSection('main');
  };

  const renderContent = () => {
    switch (activeSection) {
      case 'main':
        return <MainPage />;
      case 'cutting-maps':
        return <CuttingMaps />;
      case 'resources':
        return <Resources />;
      case 'reports':
        return <Reports />;
      case 'settings':
        return <Settings />;
      case 'users':
        return <Users />;
      default:
        return <MainPage />;
    }
  };

  if (!isAuthenticated) {
    return (
      <SettingsProvider>
        <LoginForm onLogin={handleLogin} />
      </SettingsProvider>
    );
  }

  return (
    <SettingsProvider>
      <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
        <Sidebar 
          activeSection={activeSection}
          onSectionChange={setActiveSection}
          username={user?.full_name || ''}
          onLogout={handleLogout}
        />
        <main className="flex-1 overflow-auto">
          {renderContent()}
        </main>
      </div>
    </SettingsProvider>
  );
};

export default Index;
