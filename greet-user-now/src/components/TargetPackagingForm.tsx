import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PackagingType, SeamType, TargetPackagingCreate } from '@/types/creation';

interface TargetPackagingFormProps {
  onSubmit: (data: TargetPackagingCreate) => void;
  onCancel: () => void;
}

const TargetPackagingForm: React.FC<TargetPackagingFormProps> = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    purpose: '',
    length: '',
    width: '',
    package_type: '' as PackagingType,
    seam_type: '' as SeamType,
    is_two_streams: false
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      ...formData,
      length: parseFloat(formData.length),
      width: parseFloat(formData.width)
    });
    setFormData({
      name: '',
      purpose: '',
      length: '',
      width: '',
      package_type: '' as PackagingType,
      seam_type: '' as SeamType,
      is_two_streams: false
    });
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Добавить целевую упаковку</CardTitle>
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
              <Label htmlFor="purpose">Назначение</Label>
              <Input
                id="purpose"
                value={formData.purpose}
                onChange={(e) => setFormData(prev => ({ ...prev, purpose: e.target.value }))}
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
            <div>
              <Label htmlFor="seam_type">Тип шва</Label>
              <Select
                value={formData.seam_type}
                onValueChange={(value: SeamType) => setFormData(prev => ({ ...prev, seam_type: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Выберите тип шва" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="double_seam">Двойной шов</SelectItem>
                  <SelectItem value="single_seam">Одинарный шов</SelectItem>
                  <SelectItem value="ultrasonic">Ультразвуковой</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="md:col-span-2">
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="is_two_streams"
                  checked={formData.is_two_streams}
                  onChange={(e) => setFormData(prev => ({ ...prev, is_two_streams: e.target.checked }))}
                  className="h-4 w-4 rounded border-gray-300"
                />
                <Label htmlFor="is_two_streams">Двухпотоковая обработка</Label>
              </div>
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

export default TargetPackagingForm; 