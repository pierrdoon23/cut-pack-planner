
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useSettings } from '@/contexts/SettingsContext';
import { getTranslation } from '@/utils/translations';

interface MachineFormProps {
  onSubmit: (data: any) => void;
  onCancel: () => void;
}

const MachineForm: React.FC<MachineFormProps> = ({ onSubmit, onCancel }) => {
  const { language } = useSettings();
  const [formData, setFormData] = useState({
    name: '',
    type: '',
    maxWidth: '',
    efficiency: '',
    status: 'active'
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({ name: '', type: '', maxWidth: '', efficiency: '', status: 'active' });
  };

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>{getTranslation(language, 'addMachine')}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="name">{getTranslation(language, 'name')}</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleChange('name', e.target.value)}
                required
              />
            </div>
            <div>
              <Label htmlFor="type">{getTranslation(language, 'machineType')}</Label>
              <Input
                id="type"
                value={formData.type}
                onChange={(e) => handleChange('type', e.target.value)}
                required
              />
            </div>
            <div>
              <Label htmlFor="maxWidth">{getTranslation(language, 'maxWidth')} (мм)</Label>
              <Input
                id="maxWidth"
                type="number"
                value={formData.maxWidth}
                onChange={(e) => handleChange('maxWidth', e.target.value)}
                required
              />
            </div>
            <div>
              <Label htmlFor="efficiency">{getTranslation(language, 'efficiency')} (%)</Label>
              <Input
                id="efficiency"
                type="number"
                min="0"
                max="100"
                value={formData.efficiency}
                onChange={(e) => handleChange('efficiency', e.target.value)}
                required
              />
            </div>
            <div className="md:col-span-2">
              <Label htmlFor="status">{getTranslation(language, 'status')}</Label>
              <select
                id="status"
                value={formData.status}
                onChange={(e) => handleChange('status', e.target.value)}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="active">{getTranslation(language, 'active')}</option>
                <option value="maintenance">{getTranslation(language, 'maintenance')}</option>
                <option value="inactive">{getTranslation(language, 'inactive')}</option>
              </select>
            </div>
          </div>
          <div className="flex space-x-2">
            <Button type="submit">{getTranslation(language, 'add')}</Button>
            <Button type="button" variant="outline" onClick={onCancel}>
              {getTranslation(language, 'cancel')}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default MachineForm;
