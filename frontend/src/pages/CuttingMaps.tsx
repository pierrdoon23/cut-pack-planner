import React from 'react';
import { Button } from '@/components/ui/button';
import { useTaskInfo, useDeleteTask, useUpdateTaskStatus } from '@/hooks/useTasks';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';
import TaskCreationForm from '@/components/TaskCreationForm';
import { TaskStatus } from '@/types/tasks';

const CuttingMaps: React.FC = () => {
  const { data: taskInfo, isLoading, error } = useTaskInfo();
  const deleteTaskMutation = useDeleteTask();
  const updateStatusMutation = useUpdateTaskStatus();

  const handleDeleteTask = async (taskId: number) => {
    try {
      await deleteTaskMutation.mutateAsync(taskId);
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleUpdateStatus = async (taskId: number, status: TaskStatus) => {
    try {
      await updateStatusMutation.mutateAsync({ taskId, status });
    } catch (error) {
      console.error('Error updating task status:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
      case 'in-progress':
        return 'bg-yellow-100 text-yellow-800';
      case 'planned':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'completed':
        return 'Завершено';
      case 'in_progress':
      case 'in-progress':
        return 'В процессе';
      case 'planned':
        return 'Запланировано';
      default:
        return status || 'Неизвестно';
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Загрузка карт раскроя...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <Alert>
          <AlertDescription>
            Ошибка загрузки данных: {error.message}
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Задачи</h1>
      
      <TaskCreationForm />

      <div className="mb-4">
        <h2 className="text-lg font-semibold">
          Всего задач: {taskInfo?.length || 0}
        </h2>
      </div>

      <div className="space-y-4">
        {taskInfo && taskInfo.length > 0 ? (
          taskInfo.map((task) => (
            <div key={task.task_id} className="bg-white rounded-lg border p-4">
              <div className="grid grid-cols-1 gap-3">
                <div className="flex items-center">
                  <span className="font-semibold text-blue-600 mr-2">📋 Задача ID:</span>
                  <span>{task.task_id}</span>
                </div>
                
                <div className="flex items-center">
                  <span className="font-semibold mr-2">👤 Пользователь:</span>
                  <span>{task.user?.full_name || 'Не указан'}</span>
                </div>
                
                <div className="flex items-center">
                  <span className="font-semibold mr-2">⚙️ Станок:</span>
                  <span>{task.machine?.name || 'Не указан'}</span>
                </div>
                
                <div className="flex items-center">
                  <span className="font-semibold mr-2">📦 Упаковка:</span>
                  <span>{task.target_packaging?.name || 'Не указана'}</span>
                </div>
                
                <div className="flex items-center">
                  <span className="font-semibold mr-2">🎭 Рулон:</span>
                  <span>{task.base_material?.name || 'Не указан'}</span>
                </div>
                
                <div className="flex items-center">
                  <span className="font-semibold mr-2">⚡ Статус:</span>
                  <span className={`px-2 py-1 rounded text-sm ${getStatusColor(task.status)}`}>
                    {getStatusText(task.status)}
                  </span>
                </div>
                
                <div className="flex items-center">
                  <span className="font-semibold mr-2">🕐 Начало:</span>
                  <span>
                    {task.start_time 
                      ? new Date(task.start_time).toLocaleString('ru-RU')
                      : 'Не указано'
                    }
                  </span>
                </div>
                
                {task.end_time && (
                  <div className="flex items-center">
                    <span className="font-semibold mr-2">🕐 Завершение:</span>
                    <span>{new Date(task.end_time).toLocaleString('ru-RU')}</span>
                  </div>
                )}
                
                {task.material_used && (
                  <div className="flex items-center">
                    <span className="font-semibold mr-2">✅ Использовано материала:</span>
                    <span>{task.material_used} м</span>
                  </div>
                )}
                
                {task.waste && (
                  <div className="flex items-center">
                    <span className="font-semibold mr-2">❌ Отходы:</span>
                    <span>{task.waste} м</span>
                  </div>
                )}
                
                {task.value && (
                  <div className="flex items-center">
                    <span className="font-semibold mr-2">📊 Количество упаковок:</span>
                    <span>{task.value} шт</span>
                  </div>
                )}
              </div>
              
              <div className="flex justify-end space-x-2 mt-4">
                <Button 
                  variant="destructive" 
                  size="sm"
                  onClick={() => handleDeleteTask(task.task_id)}
                  disabled={deleteTaskMutation.isPending}
                >
                  {deleteTaskMutation.isPending ? 'Удаление...' : 'Удалить'}
                </Button>
                {task.status === 'planned' && (
                  <Button 
                    variant="default" 
                    size="sm"
                    onClick={() => handleUpdateStatus(task.task_id, 'in_progress' as TaskStatus)}
                    disabled={updateStatusMutation.isPending}
                  >
                    Начать работу
                  </Button>
                )}
                {task.status === 'in_progress' && (
                  <Button 
                    variant="default" 
                    size="sm"
                    onClick={() => handleUpdateStatus(task.task_id, 'completed' as TaskStatus)}
                    disabled={updateStatusMutation.isPending}
                    className="bg-green-500 hover:bg-green-600 text-white"
                  >
                    Завершить
                  </Button>
                )}
                {task.status === 'completed' && (
                  <Button 
                    variant="default" 
                    size="sm"
                    onClick={() => handleUpdateStatus(task.task_id, 'planned' as TaskStatus)}
                    disabled={updateStatusMutation.isPending}
                  >
                    Вернуть в планирование
                  </Button>
                )}
                {(task.status === 'planned' || task.status === 'in_progress') && (
                  <Button 
                    variant="destructive" 
                    size="sm"
                    onClick={() => handleUpdateStatus(task.task_id, 'cancelled' as TaskStatus)}
                    disabled={updateStatusMutation.isPending}
                  >
                    Отменить
                  </Button>
                )}
              </div>
            </div>
          ))
        ) : (
          <div className="text-center text-gray-500 py-8">
            Нет данных для отображения
          </div>
        )}
      </div>
    </div>
  );
};

export default CuttingMaps;
