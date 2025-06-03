
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';

interface LoginFormProps {
  onLogin: (username: string, password: string) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [pdnConsent, setPdnConsent] = useState(false);
  const [cookieConsent, setCookieConsent] = useState(false);

  const canLogin = username.trim() && password.trim() && pdnConsent && cookieConsent;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (canLogin) {
      onLogin(username, password);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">Система раскроя</CardTitle>
          <p className="text-sm text-muted-foreground text-center">
            Введите данные для входа в систему
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="username" className="text-sm font-medium">
                Фамилия/логин
              </label>
              <Input
                id="username"
                type="text"
                placeholder="Введите логин"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">
                Пароль
              </label>
              <Input
                id="password"
                type="password"
                placeholder="Введите пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            
            <div className="space-y-3 pt-2">
              <div className="flex items-start space-x-3">
                <Checkbox
                  id="pdn-consent"
                  checked={pdnConsent}
                  onCheckedChange={(checked) => setPdnConsent(checked === true)}
                />
                <Label htmlFor="pdn-consent" className="text-sm leading-relaxed cursor-pointer">
                  Я согласен на хранение персональных данных
                </Label>
              </div>
              
              <div className="flex items-start space-x-3">
                <Checkbox
                  id="cookie-consent"
                  checked={cookieConsent}
                  onCheckedChange={(checked) => setCookieConsent(checked === true)}
                />
                <Label htmlFor="cookie-consent" className="text-sm leading-relaxed cursor-pointer">
                  Я согласен на использование cookie-файлов
                </Label>
              </div>
            </div>

            <Button 
              type="submit" 
              className="w-full" 
              disabled={!canLogin}
            >
              Войти
            </Button>
            
            {(!pdnConsent || !cookieConsent) && (username.trim() || password.trim()) && (
              <p className="text-sm text-red-500 text-center">
                Необходимо дать согласие на обработку данных для входа в систему
              </p>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginForm;
