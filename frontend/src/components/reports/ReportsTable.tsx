
import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { useReportTasks } from '@/hooks/useReports';
import { Loader2, FileText } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

const ReportsTable: React.FC = () => {
  const { data: tasks, isLoading, error } = useReportTasks();

  const generateTaskPDF = (task: any) => {
    console.log('Генерация PDF для задачи:', task.id);
    
    // Формируем содержимое PDF с подробной информацией о задаче
    const pdfContent = `
ОТЧЕТ ПО ЗАДАЧЕ №${task.id}

=== ОСНОВНАЯ ИНФОРМАЦИЯ ===
Название задачи: ${task.name}
Время начала: ${task.start_time ? new Date(task.start_time).toLocaleString('ru-RU') : 'Не указано'}
Время окончания: ${task.end_time ? new Date(task.end_time).toLocaleString('ru-RU') : 'В процессе'}
Статус: ${task.end_time ? 'Завершено' : 'В процессе'}

=== ДЕТАЛЬНАЯ ИНФОРМАЦИЯ ===
Базовый материал: ${task.base_material?.name || 'Не указан'}
Размеры материала: ${task.base_material?.length || 0} x ${task.base_material?.width || 0} мм
Толщина: ${task.base_material?.thickness || 0} мм
Тип упаковки материала: ${task.base_material?.package_type || 'Не указан'}

Целевая упаковка: ${task.target_packaging?.name || 'Не указана'}
Назначение: ${task.target_packaging?.purpose || 'Не указано'}
Размеры упаковки: ${task.target_packaging?.length || 0} x ${task.target_packaging?.width || 0} мм
Тип шва: ${task.target_packaging?.seam_type || 'Не указан'}
Два потока: ${task.target_packaging?.is_two_streams ? 'Да' : 'Нет'}

Станок: ${task.machine?.name || 'Не указан'}
Скорость резки: ${task.machine?.cutting_speed || 0} мм/мин
Ширина станка: ${task.machine?.machine_width || 0} мм

Пользователь: ${task.user?.full_name || 'Не указан'}
Роль: ${task.user?.role || 'Не указана'}

=== ПРОИЗВОДСТВЕННЫЕ ПОКАЗАТЕЛИ ===
Использованный материал: ${task.material_used || 0} мм
Отходы: ${task.waste || 0} мм
Количество изделий: ${task.value || 0} шт.

Дата создания отчета: ${new Date().toLocaleString('ru-RU')}
    `;

    // Имитация генерации PDF
    setTimeout(() => {
      const element = document.createElement('a');
      const file = new Blob([pdfContent], { type: 'application/pdf' });
      element.href = URL.createObjectURL(file);
      element.download = `task_${task.id}_report.pdf`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      
      console.log(`PDF отчет для задачи ${task.id} сгенерирован`);
    }, 500);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Загрузка данных...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert>
        <AlertDescription>
          Ошибка загрузки данных: {error.message}
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Название задачи</TableHead>
            <TableHead>Время начала</TableHead>
            <TableHead>Время окончания</TableHead>
            <TableHead>Статус</TableHead>
            <TableHead>Действия</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {tasks && tasks.length > 0 ? (
            tasks.map((task) => (
              <TableRow key={task.id}>
                <TableCell className="font-medium">{task.id}</TableCell>
                <TableCell>{task.name}</TableCell>
                <TableCell>
                  {task.start_time 
                    ? new Date(task.start_time).toLocaleString('ru-RU')
                    : 'Не указано'
                  }
                </TableCell>
                <TableCell>
                  {task.end_time 
                    ? new Date(task.end_time).toLocaleString('ru-RU')
                    : 'В процессе'
                  }
                </TableCell>
                <TableCell>
                  <span className={`px-2 py-1 rounded text-sm ${
                    task.end_time 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {task.end_time ? 'Завершено' : 'В процессе'}
                  </span>
                </TableCell>
                <TableCell>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => generateTaskPDF(task)}
                    className="flex items-center gap-2"
                  >
                    <FileText className="h-4 w-4" />
                    PDF отчет
                  </Button>
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={6} className="text-center text-gray-500 py-8">
                Нет данных для отображения
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
};

export default ReportsTable;
