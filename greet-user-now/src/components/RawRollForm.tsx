
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useSettings } from '@/contexts/SettingsContext';
import { getTranslation } from '@/utils/translations';

interface RawRollFormProps {
  onSubmit: (data: any) => void;
  onCancel: () => void;
}

const RawRollForm: React.FC<RawRollFormProps> = ({ onSubmit, onCancel }) => {
  const { language } = useSettings();
  const [formData, setFormData] = useState({
    name: '',
    width: '',
    thickness: '',
    weight: '',
    material: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({ name: '', width: '', thickness: '', weight: '', material: '' });
  };

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>{getTranslation(language, 'addRawRoll')}</CardTitle>
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
              <Label htmlFor="width">{getTranslation(language, 'width')} (мм)</Label>
              <Input
                id="width"
                type="number"
                value={formData.width}
                onChange={(e) => handleChange('width', e.target.value)}
                required
              />
            </div>
            <div>
              <Label htmlFor="thickness">{getTranslation(language, 'thickness')} (мм)</Label>
              <Input
                id="thickness"
                type="number"
                step="0.1"
                value={formData.thickness}
                onChange={(e) => handleChange('thickness', e.target.value)}
                required
              />
            </div>
            <div>
              <Label htmlFor="weight">{getTranslation(language, 'weight')} (кг)</Label>
              <Input
                id="weight"
                type="number"
                step="0.1"
                value={formData.weight}
                onChange={(e) => handleChange('weight', e.target.value)}
                required
              />
            </div>
            <div className="md:col-span-2">
              <Label htmlFor="material">{getTranslation(language, 'material')}</Label>
              <Input
                id="material"
                value={formData.material}
                onChange={(e) => handleChange('material', e.target.value)}
                required
              />
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

export default RawRollForm;
