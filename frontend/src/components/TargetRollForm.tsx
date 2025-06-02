
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useSettings } from '@/contexts/SettingsContext';
import { getTranslation } from '@/utils/translations';

interface TargetRollFormProps {
  onSubmit: (data: any) => void;
  onCancel: () => void;
}

const TargetRollForm: React.FC<TargetRollFormProps> = ({ onSubmit, onCancel }) => {
  const { language } = useSettings();
  const [formData, setFormData] = useState({
    name: '',
    targetWidth: '',
    targetThickness: '',
    quantity: '',
    priority: 'medium'
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({ name: '', targetWidth: '', targetThickness: '', quantity: '', priority: 'medium' });
  };

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>{getTranslation(language, 'addTargetRoll')}</CardTitle>
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
              <Label htmlFor="targetWidth">{getTranslation(language, 'targetWidth')} (мм)</Label>
              <Input
                id="targetWidth"
                type="number"
                value={formData.targetWidth}
                onChange={(e) => handleChange('targetWidth', e.target.value)}
                required
              />
            </div>
            <div>
              <Label htmlFor="targetThickness">{getTranslation(language, 'targetThickness')} (мм)</Label>
              <Input
                id="targetThickness"
                type="number"
                step="0.1"
                value={formData.targetThickness}
                onChange={(e) => handleChange('targetThickness', e.target.value)}
                required
              />
            </div>
            <div>
              <Label htmlFor="quantity">{getTranslation(language, 'quantity')}</Label>
              <Input
                id="quantity"
                type="number"
                value={formData.quantity}
                onChange={(e) => handleChange('quantity', e.target.value)}
                required
              />
            </div>
            <div className="md:col-span-2">
              <Label htmlFor="priority">{getTranslation(language, 'priority')}</Label>
              <select
                id="priority"
                value={formData.priority}
                onChange={(e) => handleChange('priority', e.target.value)}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="low">{getTranslation(language, 'low')}</option>
                <option value="medium">{getTranslation(language, 'medium')}</option>
                <option value="high">{getTranslation(language, 'high')}</option>
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

export default TargetRollForm;
