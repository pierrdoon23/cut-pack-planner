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
import { useTaskInfo } from '@/hooks/useTasks';
import { Loader2, FileText } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';
import { TaskInfo } from '@/types/tasks';

// Инициализируем pdfMake с базовыми шрифтами
pdfMake.vfs = pdfFonts;

const ReportsTable: React.FC = () => {
  const { data: tasks, isLoading, error } = useTaskInfo();

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

  const generateTaskPDF = (task: TaskInfo) => {
    try {
      const content: pdfMake.Content[] = [
        { text: `ОТЧЕТ ПО ЗАДАЧЕ №${task.task_id}`, style: 'header' },
        { text: `Дата создания отчета: ${new Date().toLocaleString('ru-RU')}`, margin: [0, 0, 0, 10] },
        
        { text: 'ОСНОВНАЯ ИНФОРМАЦИЯ', style: 'subheader' },
        {
          text: [
            `📋 ID задачи: ${task.task_id}\n`,
            `👤 Пользователь: ${task.user?.full_name || 'Не указан'}\n`,
            `⚙️ Станок: ${task.machine?.name || 'Не указан'}\n`,
            `📦 Упаковка: ${task.target_packaging?.name || 'Не указана'}\n`,
            `🎭 Рулон: ${task.base_material?.name || 'Не указан'}\n`,
            `⚡ Статус: ${getStatusText(task.status)}\n`,
            `🕐 Начало: ${task.start_time ? new Date(task.start_time).toLocaleString('ru-RU') : 'Не указано'}\n`,
            task.end_time ? `🕐 Завершение: ${new Date(task.end_time).toLocaleString('ru-RU')}\n` : ''
          ]
        },

        { text: 'ДЕТАЛЬНАЯ ИНФОРМАЦИЯ', style: 'subheader', margin: [0, 10, 0, 5] },
        {
          text: [
            '📦 Базовый материал:\n',
            `   • Название: ${task.base_material?.name || 'Не указан'}\n`,
            `   • Размеры: ${task.base_material?.length || 0} x ${task.base_material?.width || 0} мм\n`,
            `   • Толщина: ${task.base_material?.thickness || 0} мм\n`,
            `   • Тип упаковки: ${task.base_material?.package_type || 'Не указан'}\n\n`,
            
            '🎯 Целевая упаковка:\n',
            `   • Название: ${task.target_packaging?.name || 'Не указана'}\n`,
            `   • Назначение: ${task.target_packaging?.purpose || 'Не указано'}\n`,
            `   • Размеры: ${task.target_packaging?.length || 0} x ${task.target_packaging?.width || 0} мм\n`,
            `   • Тип шва: ${task.target_packaging?.seam_type || 'Не указан'}\n`,
            `   • Два потока: ${task.target_packaging?.is_two_streams ? 'Да' : 'Нет'}\n\n`,
            
            '⚙️ Станок:\n',
            `   • Название: ${task.machine?.name || 'Не указан'}\n`,
            `   • Скорость резки: ${task.machine?.cutting_speed || 0} мм/мин\n`,
            `   • Ширина станка: ${task.machine?.machine_width || 0} мм\n\n`,
            
            '👤 Пользователь:\n',
            `   • Имя: ${task.user?.full_name || 'Не указан'}\n`,
            `   • Роль: ${task.user?.role || 'Не указана'}\n`
          ]
        },

        { text: 'ПРОИЗВОДСТВЕННЫЕ ПОКАЗАТЕЛИ', style: 'subheader', margin: [0, 10, 0, 5] },
        {
          text: [
            `✅ Использовано материала: ${task.material_used || 0} м\n`,
            `❌ Отходы: ${task.waste || 0} м\n`,
            `📊 Количество изделий: ${task.value || 0} шт.\n`
          ]
        }
      ];

      const docDefinition = {
        content,
        defaultStyle: {
          fontSize: 10
        },
        styles: {
          header: {
            fontSize: 16,
            bold: true,
            alignment: 'center',
            margin: [0, 0, 0, 10]
          },
          subheader: {
            fontSize: 12,
            bold: true,
            margin: [0, 8, 0, 4]
          }
        }
      };

      pdfMake.createPdf(docDefinition).download(`task_${task.task_id}_report_${new Date().toISOString().split('T')[0]}.pdf`);
    } catch (error) {
      console.error('Ошибка при генерации PDF:', error);
      alert('Произошла ошибка при генерации PDF. Проверьте консоль для деталей.');
    }
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
              <TableRow key={task.task_id}>
                <TableCell className="font-medium">{task.task_id}</TableCell>
                <TableCell>{task.base_material?.name || 'Без названия'}</TableCell>
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
                    task.status?.toLowerCase() === 'completed'
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {getStatusText(task.status)}
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
              <TableCell colSpan={6} className="text-center py-4">
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
