import React from 'react';
import DashboardCard from '@/components/DashboardCard';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { useMainPageData } from '@/hooks/useMainPageData';
import { Loader2 } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

const MainPage: React.FC = () => {
  const { data, isLoading, error, refetch } = useMainPageData();

  if (isLoading) {
    return (
      <div className="p-6 flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Загрузка данных...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <Alert variant="destructive">
          <AlertDescription>
            Ошибка загрузки данных: {error instanceof Error ? error.message : 'Неизвестная ошибка'}
            <button 
              onClick={() => refetch()} 
              className="ml-2 underline hover:no-underline"
            >
              Попробовать снова
            </button>
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  console.log('Raw Weekly Chart Data:', data?.weeklyChart);

  const weeklyChartData = data?.weeklyChart.labels.map((label, index) => {
    const value = data.weeklyChart.values[index] || 0;
    console.log(`Day ${label}: ${value} tasks`);
    return {
      day: label,
      value: value
    };
  }) || [];

  console.log('Processed Weekly Chart Data:', weeklyChartData);

  const cuttingTypesData = data?.cuttingTypes.map((item, index) => ({
    name: item.type,
    value: item.percent,
    color: index === 0 ? '#3B82F6' : '#60A5FA'
  })) || [];

  const wasteData = data?.materialUsage ? [
    { name: 'Отходы', value: data.materialUsage.wasted_percent, color: '#F97316' },
    { name: 'Использование', value: data.materialUsage.used_percent, color: '#22C55E' }
  ] : [];

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Главная Страница</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <DashboardCard 
          title="Рулоны" 
          value={data?.rollsCount.total || 0} 
          subtitle={`${data?.rollsCount.last_24h || 0} за 24 часа`} 
        />
        <DashboardCard 
          title="Карты раскроя" 
          value={data?.cuttingMapsCount.total || 0} 
          subtitle={`${data?.cuttingMapsCount.last_24h || 0} за 24 часа`} 
        />
        <DashboardCard 
          title="Палеты" 
          value={data?.packagesCount.total || 0} 
          subtitle={`${data?.packagesCount.last_24h || 0} за 24 часа`} 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Выполнение планов по дням недели</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weeklyChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis allowDecimals={false} domain={[0, 'auto']} />
              <Tooltip 
                formatter={(value) => [`${value} задач`, 'Количество']}
                labelFormatter={(label) => `День: ${label}`}
              />
              <Bar 
                dataKey="value" 
                fill="#3B82F6" 
                name="Выполненные задачи"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-4">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-4">Типы нарезки</h3>
            <ResponsiveContainer width="100%" height={150}>
              <PieChart>
                <Pie
                  data={cuttingTypesData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={60}
                  dataKey="value"
                >
                  {cuttingTypesData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value, name) => [`${value}%`, `${name}`]} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-4">Отходы и использование</h3>
            <ResponsiveContainer width="100%" height={150}>
              <PieChart>
                <Pie
                  data={wasteData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={60}
                  dataKey="value"
                >
                  {wasteData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value, name) => [`${value}%`, `${name}`]} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
