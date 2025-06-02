import React from 'react';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useSettings } from '@/contexts/SettingsContext';
import { getTranslation } from '@/utils/translations';
import { useTaskInfo } from '@/hooks/useTasks';
import ReportsTable from '@/components/reports/ReportsTable';
import GanttChart from '@/components/reports/GanttChart';
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';

// Инициализируем pdfMake с базовыми шрифтами
pdfMake.vfs = pdfFonts;

const Reports: React.FC = () => {
  const { language } = useSettings();
  const { data: tasks } = useTaskInfo();

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

  const generateAllTasksPDF = async () => {
    try {
      if (!tasks || tasks.length === 0) {
        alert('Нет данных для генерации отчета');
        return;
      }

      const content: pdfMake.Content[] = [
        { text: 'ОБЩИЙ ОТЧЕТ ПО ВСЕМ ЗАДАЧАМ', style: 'header' },
        { text: `Дата создания отчета: ${new Date().toLocaleString('ru-RU')}` },
        { text: `Общее количество задач: ${tasks.length}`, margin: [0, 0, 0, 10] }
      ];

      tasks.forEach((task, index) => {
        content.push(
          { text: `${index + 1}. ЗАДАЧА №${task.task_id}`, style: 'subheader' },
          {
            text: [
              `📋 ID задачи: ${task.task_id}\n`,
              `👤 Пользователь: ${task.user?.full_name || 'Не указан'}\n`,
              `⚙️ Станок: ${task.machine?.name || 'Не указан'}\n`,
              `📦 Упаковка: ${task.target_packaging?.name || 'Не указана'}\n`,
              `🎭 Рулон: ${task.base_material?.name || 'Не указан'}\n`,
              `⚡ Статус: ${getStatusText(task.status)}\n`,
              `🕐 Начало: ${task.start_time ? new Date(task.start_time).toLocaleString('ru-RU') : 'Не указано'}\n`,
              task.end_time ? `🕐 Завершение: ${new Date(task.end_time).toLocaleString('ru-RU')}\n` : '',
              task.material_used ? `✅ Использовано материала: ${task.material_used} м\n` : '',
              task.waste ? `❌ Отходы: ${task.waste} м\n` : '',
              task.value ? `📊 Количество упаковок: ${task.value} шт\n` : ''
            ]
          }
        );
      });

      const completedTasks = tasks.filter(task => task.status?.toLowerCase() === 'completed').length;
      const inProgressTasks = tasks.filter(task => task.status?.toLowerCase() === 'in_progress').length;
      const totalMaterialUsed = tasks.reduce((sum, task) => sum + (task.material_used || 0), 0);
      const totalWaste = tasks.reduce((sum, task) => sum + (task.waste || 0), 0);
      const totalProducts = tasks.reduce((sum, task) => sum + (task.value || 0), 0);
      const efficiency = totalMaterialUsed > 0
        ? ((totalMaterialUsed / (totalMaterialUsed + totalWaste)) * 100).toFixed(2)
        : '0';

      content.push({
        text: [
          '\n=== ОБЩАЯ СТАТИСТИКА ===\n',
          `Завершенных задач: ${completedTasks}\n`,
          `Задач в процессе: ${inProgressTasks}\n`,
          `Общий расход материала: ${totalMaterialUsed.toFixed(2)} м\n`,
          `Общие отходы: ${totalWaste.toFixed(2)} м\n`,
          `Общее количество изделий: ${totalProducts} шт.\n`,
          `Эффективность: ${efficiency}%\n`
        ],
        style: 'subheader'
      });

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

      pdfMake.createPdf(docDefinition).download(`all_tasks_report_${new Date().toISOString().split('T')[0]}.pdf`);
    } catch (error) {
      console.error('Ошибка при генерации PDF:', error);
      alert('Произошла ошибка при генерации PDF. Проверьте консоль для деталей.');
    }
  };

  return (
    <div className="p-6 bg-white dark:bg-gray-900 text-gray-900 dark:text-white min-h-full">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">{getTranslation(language, 'reports')}</h1>
        <Button
          onClick={generateAllTasksPDF}
          className="bg-green-600 hover:bg-green-700 text-white"
        >
          {getTranslation(language, 'generatePDF')} - Все задачи
        </Button>
      </div>

      <Tabs defaultValue="table" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="table">Таблица задач</TabsTrigger>
          <TabsTrigger value="gantt">Диаграмма Ганта</TabsTrigger>
        </TabsList>

        <TabsContent value="table" className="mt-6">
          <ReportsTable />
        </TabsContent>

        <TabsContent value="gantt" className="mt-6">
          <GanttChart />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Reports;
