
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useBaseMaterials, useTargetPackaging, useMachines, useCreateTask } from '@/hooks/useTasks';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/hooks/useAuth';

const TaskCreationForm: React.FC = () => {
  const { toast } = useToast();
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    base_material_id: '',
    target_packaging_id: '',
    machine_id: ''
  });

  const { data: baseMaterials, isLoading: loadingMaterials } = useBaseMaterials();
  const { data: targetPackaging, isLoading: loadingPackaging } = useTargetPackaging();
  const { data: machines, isLoading: loadingMachines } = useMachines();
  const createTaskMutation = useCreateTask();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.base_material_id || !formData.target_packaging_id || !formData.machine_id) {
      toast({
        title: "Ошибка",
        description: "Пожалуйста, заполните все поля",
        variant: "destructive"
      });
      return;
    }

    if (!user?.id) {
      toast({
        title: "Ошибка",
        description: "Пользователь не авторизован",
        variant: "destructive"
      });
      return;
    }

    try {
      await createTaskMutation.mutateAsync({
        base_material_id: parseInt(formData.base_material_id),
        target_packaging_id: parseInt(formData.target_packaging_id),
        machine_id: parseInt(formData.machine_id),
        user_id: user.id,
        status: 'planned'
      });
      
      toast({
        title: "Успех",
        description: "Задача успешно создана"
      });
      
      setFormData({
        base_material_id: '',
        target_packaging_id: '',
        machine_id: ''
      });
    } catch (error) {
      console.error('Ошибка создания задачи:', error);
      toast({
        title: "Ошибка",
        description: "Не удалось создать задачу",
        variant: "destructive"
      });
    }
  };

  const isLoading = loadingMaterials || loadingPackaging || loadingMachines;

  if (isLoading) {
    return (
      <Card className="mb-6">
        <CardContent className="p-6 flex items-center justify-center">
          <Loader2 className="h-6 w-6 animate-spin mr-2" />
          <span>Загрузка данных...</span>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Создание новой задачи</CardTitle>
        {user && (
          <p className="text-sm text-gray-600">
            Пользователь: {user.full_name} ({user.role})
          </p>
        )}
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Сырьевой рулон</label>
              <Select
                value={formData.base_material_id}
                onValueChange={(value) => setFormData(prev => ({ ...prev, base_material_id: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Выберите материал" />
                </SelectTrigger>
                <SelectContent>
                  {baseMaterials?.map((material) => (
                    <SelectItem key={material.id} value={material.id.toString()}>
                      {material.name} ({material.length}x{material.width}x{material.thickness}мм)
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Целевой рулон</label>
              <Select
                value={formData.target_packaging_id}
                onValueChange={(value) => setFormData(prev => ({ ...prev, target_packaging_id: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Выберите упаковку" />
                </SelectTrigger>
                <SelectContent>
                  {targetPackaging?.map((packaging) => (
                    <SelectItem key={packaging.id} value={packaging.id.toString()}>
                      {packaging.name} ({packaging.length}x{packaging.width}мм)
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Станок</label>
              <Select
                value={formData.machine_id}
                onValueChange={(value) => setFormData(prev => ({ ...prev, machine_id: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Выберите станок" />
                </SelectTrigger>
                <SelectContent>
                  {machines?.map((machine) => (
                    <SelectItem key={machine.id} value={machine.id.toString()}>
                      {machine.name} (ширина: {machine.machine_width}мм)
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex justify-end">
            <Button 
              type="submit" 
              disabled={createTaskMutation.isPending}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {createTaskMutation.isPending ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  Создание...
                </>
              ) : (
                'Создать задачу'
              )}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default TaskCreationForm;
