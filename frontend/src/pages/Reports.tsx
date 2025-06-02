
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useSettings } from '@/contexts/SettingsContext';
import { getTranslation } from '@/utils/translations';
import { useReportTasks } from '@/hooks/useReports';
import ReportsTable from '@/components/reports/ReportsTable';
import GanttChart from '@/components/reports/GanttChart';

const Reports: React.FC = () => {
  const { language } = useSettings();
  const { data: tasks } = useReportTasks();

  const generateAllTasksPDF = () => {
    console.log('Генерация общего PDF отчета');
    
    if (!tasks || tasks.length === 0) {
      alert('Нет данных для генерации отчета');
      return;
    }

    // Формируем полный отчет по всем задачам
    let pdfContent = `
ОБЩИЙ ОТЧЕТ ПО ВСЕМ ЗАДАЧАМ

Дата создания отчета: ${new Date().toLocaleString('ru-RU')}
Общее количество задач: ${tasks.length}

====================================================

`;

    tasks.forEach((task, index) => {
      pdfContent += `
${index + 1}. ЗАДАЧА №${task.id}

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

====================================================

`;
    });

    // Добавляем статистику
    const completedTasks = tasks.filter(task => task.end_time).length;
    const inProgressTasks = tasks.length - completedTasks;
    const totalMaterialUsed = tasks.reduce((sum, task) => sum + (task.material_used || 0), 0);
    const totalWaste = tasks.reduce((sum, task) => sum + (task.waste || 0), 0);
    const totalProducts = tasks.reduce((sum, task) => sum + (task.value || 0), 0);

    pdfContent += `
=== ОБЩАЯ СТАТИСТИКА ===
Завершенных задач: ${completedTasks}
Задач в процессе: ${inProgressTasks}
Общий расход материала: ${totalMaterialUsed.toFixed(2)} мм
Общие отходы: ${totalWaste.toFixed(2)} мм
Общее количество произведенных изделий: ${totalProducts} шт.
Эффективность использования материала: ${totalMaterialUsed > 0 ? ((totalMaterialUsed / (totalMaterialUsed + totalWaste)) * 100).toFixed(2) : 0}%
    `;
    
    // Имитация генерации PDF
    setTimeout(() => {
      const element = document.createElement('a');
      const file = new Blob([pdfContent], { type: 'application/pdf' });
      element.href = URL.createObjectURL(file);
      element.download = `all_tasks_report_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      
      alert('Общий PDF отчет сгенерирован');
    }, 1000);
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
