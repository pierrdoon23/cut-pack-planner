import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useUsers, useCreateUser, useUpdateUser, useDeleteUser } from '@/hooks/useUsers';
import { useToast } from '@/hooks/use-toast';
import { User, UserCreate } from '@/types/users';

const Users: React.FC = () => {
  const { data: users = [], isLoading, error } = useUsers();
  const createUserMutation = useCreateUser();
  const updateUserMutation = useUpdateUser();
  const deleteUserMutation = useDeleteUser();
  const { toast } = useToast();

  const [newUser, setNewUser] = useState<UserCreate>({ 
    full_name: '', 
    role: 'operator', 
    password: '' 
  });
  const [editingUser, setEditingUser] = useState<User | null>(null);

  const handleAddUser = async () => {
    if (newUser.full_name && newUser.password) {
      try {
        await createUserMutation.mutateAsync(newUser);
        setNewUser({ full_name: '', role: 'operator', password: '' });
        toast({
          title: "Успех",
          description: "Пользователь успешно добавлен",
        });
      } catch (error) {
        toast({
          title: "Ошибка",
          description: "Не удалось добавить пользователя",
          variant: "destructive",
        });
      }
    }
  };

  const handleUpdateUser = async (userId: number, updatedData: Partial<User>) => {
    try {
      await updateUserMutation.mutateAsync({ userId, user: updatedData });
      setEditingUser(null);
      toast({
        title: "Успех",
        description: "Пользователь успешно обновлен",
      });
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось обновить пользователя",
        variant: "destructive",
      });
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этого пользователя?')) {
      deleteUserMutation.mutate(userId);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-6">Пользователи</h1>
        <p>Загрузка...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-6">Пользователи</h1>
        <p className="text-red-500">Ошибка загрузки данных</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Пользователи</h1>
      
      <div className="space-y-6">
        {users.map((user) => (
          <div key={user.id} className="bg-blue-600 text-white p-4 rounded">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-center">
              <div>
                <label className="block text-sm opacity-80">Логин:</label>
                {editingUser?.id === user.id ? (
                  <Input 
                    value={editingUser.full_name} 
                    onChange={(e) => setEditingUser({...editingUser, full_name: e.target.value})}
                    className="bg-white text-black" 
                  />
                ) : (
                  <Input 
                    value={user.full_name} 
                    className="bg-white text-black" 
                    readOnly 
                  />
                )}
              </div>
              <div>
                <label className="block text-sm opacity-80">Роль:</label>
                {editingUser?.id === user.id ? (
                  <Select 
                    value={editingUser.role} 
                    onValueChange={(value: 'admin' | 'operator') => setEditingUser({...editingUser, role: value})}
                  >
                    <SelectTrigger className="bg-white text-black">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="admin">Администратор</SelectItem>
                      <SelectItem value="operator">Оператор</SelectItem>
                    </SelectContent>
                  </Select>
                ) : (
                  <Select value={user.role}>
                    <SelectTrigger className="bg-white text-black">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="admin">Администратор</SelectItem>
                      <SelectItem value="operator">Оператор</SelectItem>
                    </SelectContent>
                  </Select>
                )}
              </div>
              <div>
                <label className="block text-sm opacity-80">Пароль:</label>
                <Input 
                  type="password" 
                  value="••••••" 
                  className="bg-white text-black" 
                  readOnly 
                />
              </div>
              <div className="flex space-x-2">
                {editingUser?.id === user.id ? (
                  <>
                    <Button 
                      variant="secondary" 
                      size="sm"
                      onClick={() => handleUpdateUser(user.id, editingUser)}
                      disabled={updateUserMutation.isPending}
                    >
                      Сохранить
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setEditingUser(null)}
                    >
                      Отмена
                    </Button>
                  </>
                ) : (
                  <>
                    <Button 
                      variant="secondary" 
                      size="sm"
                      onClick={() => setEditingUser(user)}
                    >
                      Изменить
                    </Button>
                    <Button 
                      variant="destructive" 
                      size="sm"
                      onClick={() => handleDeleteUser(user.id)}
                      disabled={deleteUserMutation.isPending}
                    >
                      Удалить
                    </Button>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}

        <div className="bg-gray-100 p-4 rounded">
          <h3 className="text-lg font-semibold mb-4">Добавить пользователя</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <div>
              <label className="block text-sm font-medium mb-1">Логин:</label>
              <Input 
                value={newUser.full_name}
                onChange={(e) => setNewUser({...newUser, full_name: e.target.value})}
                placeholder="Введите логин"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Роль:</label>
              <Select 
                value={newUser.role} 
                onValueChange={(value: 'admin' | 'operator') => setNewUser({...newUser, role: value})}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin">Администратор</SelectItem>
                  <SelectItem value="operator">Оператор</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Пароль:</label>
              <Input 
                type="password"
                value={newUser.password}
                onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                placeholder="Введите пароль"
              />
            </div>
            <Button 
              onClick={handleAddUser}
              disabled={createUserMutation.isPending}
            >
              Добавить
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Users;
