
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface DashboardCardProps {
  title: string;
  value: number;
  subtitle?: string;
}

const DashboardCard: React.FC<DashboardCardProps> = ({ title, value, subtitle }) => {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-medium">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold">{value}</div>
        {subtitle && <p className="text-sm text-muted-foreground mt-1">{subtitle}</p>}
      </CardContent>
    </Card>
  );
};

export default DashboardCard;
