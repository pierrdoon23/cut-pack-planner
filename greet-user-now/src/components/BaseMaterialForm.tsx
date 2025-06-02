import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PackagingType, BaseMaterialCreate } from '@/types/creation';

interface BaseMaterialFormProps {
  onSubmit: (data: BaseMaterialCreate) => void;
  onCancel: () => void;
}

const BaseMaterialForm: React.FC<BaseMaterialFormProps> = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    length: '',
    width: '',
    thickness: '',
    package_type: '' as PackagingType
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      ...formData,
      length: parseFloat(formData.length),
      width: parseFloat(formData.width),
      thickness: parseFloat(formData.thickness)
    });
    setFormData({ name: '', length: '', width: '', thickness: '', package_type: '' as PackagingType });
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Добавить базовый материал</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="name">Название</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                required
              />
            </div>
            <div>
              <Label htmlFor="length">Длина (м)</Label>
              <Input
                id="length"
                type="number"
                step="0.01"
                value={formData.length}
                onChange={(e) => setFormData(prev => ({ ...prev, length: e.target.value }))}
                required
              />
            </div>
            <div>
              <Label htmlFor="width">Ширина (м)</Label>
              <Input
                id="width"
                type="number"
                step="0.01"
                value={formData.width}
                onChange={(e) => setFormData(prev => ({ ...prev, width: e.target.value }))}
                required
              />
            </div>
            <div>
              <Label htmlFor="thickness">Толщина (мм)</Label>
              <Input
                id="thickness"
                type="number"
                step="0.01"
                value={formData.thickness}
                onChange={(e) => setFormData(prev => ({ ...prev, thickness: e.target.value }))}
                required
              />
            </div>
            <div className="md:col-span-2">
              <Label htmlFor="package_type">Тип упаковки</Label>
              <Select
                value={formData.package_type}
                onValueChange={(value: PackagingType) => setFormData(prev => ({ ...prev, package_type: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Выберите тип упаковки" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="vacuum">Вакуумная</SelectItem>
                  <SelectItem value="flow_pack">Флоу-пак</SelectItem>
                  <SelectItem value="shrink">Усадочная</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="flex space-x-2">
            <Button type="submit">Добавить</Button>
            <Button type="button" variant="outline" onClick={onCancel}>
              Отмена
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default BaseMaterialForm; 