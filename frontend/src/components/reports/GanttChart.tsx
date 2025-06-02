
import React from 'react';
import { useGanttData } from '@/hooks/useReports';
import { Loader2 } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

const GanttChart: React.FC = () => {
  const { data: ganttTasks, isLoading, error } = useGanttData();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Загрузка диаграммы...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert>
        <AlertDescription>
          Ошибка загрузки данных для диаграммы: {error.message}
        </AlertDescription>
      </Alert>
    );
  }

  // Вычисляем временные рамки
  const allDates = ganttTasks?.flatMap(task => [task.start, task.end]) || [];
  const minDate = allDates.length > 0 ? new Date(Math.min(...allDates.map(d => d.getTime()))) : new Date();
  const maxDate = allDates.length > 0 ? new Date(Math.max(...allDates.map(d => d.getTime()))) : new Date();
  
  const totalDuration = maxDate.getTime() - minDate.getTime();
  const dayInMs = 24 * 60 * 60 * 1000;
  const totalDays = Math.ceil(totalDuration / dayInMs);

  // Генерируем сетку дней
  const timeLabels = [];
  for (let i = 0; i <= totalDays; i++) {
    const date = new Date(minDate.getTime() + i * dayInMs);
    timeLabels.push(date.toLocaleDateString('ru-RU', { 
      day: '2-digit', 
      month: '2-digit' 
    }));
  }

  const getTaskPosition = (start: Date, end: Date) => {
    const startOffset = (start.getTime() - minDate.getTime()) / totalDuration * 100;
    const duration = (end.getTime() - start.getTime()) / totalDuration * 100;
    return { left: `${startOffset}%`, width: `${Math.max(duration, 2)}%` };
  };

  return (
    <div className="bg-white rounded-lg border p-4">
      <h3 className="text-lg font-semibold mb-4">Диаграмма Ганта</h3>
      
      {ganttTasks && ganttTasks.length > 0 ? (
        <div className="overflow-x-auto">
          {/* Временная шкала */}
          <div className="flex mb-2 border-b">
            <div className="w-48 flex-shrink-0 p-2 font-medium">Задачи</div>
            <div className="flex-1 relative">
              <div className="flex">
                {timeLabels.map((label, index) => (
                  <div key={index} className="flex-1 text-xs text-center p-1 border-l">
                    {label}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Задачи */}
          <div className="space-y-1">
            {ganttTasks.map((task) => {
              const position = getTaskPosition(task.start, task.end);
              return (
                <div key={task.id} className="flex items-center h-8">
                  <div className="w-48 flex-shrink-0 p-2 text-sm truncate">
                    {task.name}
                  </div>
                  <div className="flex-1 relative h-6 bg-gray-50">
                    <div
                      className={`absolute h-full rounded ${
                        task.progress === 100 
                          ? 'bg-green-500' 
                          : 'bg-blue-500'
                      } opacity-80`}
                      style={position}
                      title={`${task.name}: ${task.start.toLocaleDateString()} - ${task.end.toLocaleDateString()}`}
                    >
                      <div className="text-xs text-white p-1 truncate">
                        {task.progress}%
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="text-center text-gray-500 py-8">
          Нет данных для отображения диаграммы
        </div>
      )}
    </div>
  );
};

export default GanttChart;
