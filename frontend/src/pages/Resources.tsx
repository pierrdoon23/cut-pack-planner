import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useSettings } from '@/contexts/SettingsContext';
import { getTranslation } from '@/utils/translations';
import { Plus, Trash2, Edit } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { useToast } from '@/hooks/use-toast';
import {
  useBaseMaterials,
  useCreateBaseMaterial,
  useDeleteBaseMaterial,
  useTargetPackaging,
  useCreateTargetPackaging,
  useDeleteTargetPackaging,
  useMachines,
  useCreateMachine,
  useDeleteMachine
} from '@/hooks/useCreation';
import { BaseMaterialCreate, TargetPackagingCreate, PackagingType, SeamType } from '@/types/creation';

const Resources: React.FC = () => {
  const { language } = useSettings();
  const { toast } = useToast();
  const [activeTab, setActiveTab] = useState<'rawRolls' | 'targetRolls' | 'machines'>('rawRolls');
  const [showForm, setShowForm] = useState(false);

  // API hooks
  const { data: baseMaterials = [], isLoading: baseMaterialsLoading } = useBaseMaterials();
  const { data: targetPackaging = [], isLoading: targetPackagingLoading } = useTargetPackaging();
  const { data: machines = [], isLoading: machinesLoading } = useMachines();

  const createBaseMaterial = useCreateBaseMaterial();
  const deleteBaseMaterial = useDeleteBaseMaterial();
  const createTargetPackaging = useCreateTargetPackaging();
  const deleteTargetPackaging = useDeleteTargetPackaging();
  const createMachine = useCreateMachine();
  const deleteMachine = useDeleteMachine();

  const [baseMaterialForm, setBaseMaterialForm] = useState({
    name: '',
    length: '',
    width: '',
    thickness: '',
    package_type: 'vacuum' as PackagingType
  });

  const [targetPackagingForm, setTargetPackagingForm] = useState({
    name: '',
    purpose: '',
    length: '',
    width: '',
    package_type: 'vacuum' as PackagingType,
    seam_type: 'double_seam' as SeamType,
    is_two_streams: false
  });

  const [machineForm, setMachineForm] = useState({
    name: '',
    cutting_speed: '',
    machine_width: ''
  });

  const handleCreateBaseMaterial = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!baseMaterialForm.name || !baseMaterialForm.length || !baseMaterialForm.width || 
        !baseMaterialForm.thickness || !baseMaterialForm.package_type) {
      toast({ 
        title: "Ошибка валидации", 
        description: "Все поля должны быть заполнены",
        variant: "destructive" 
      });
      return;
    }

    try {
      await createBaseMaterial.mutateAsync({
        name: baseMaterialForm.name.trim(),
        length: parseFloat(baseMaterialForm.length),
        width: parseFloat(baseMaterialForm.width),
        thickness: parseFloat(baseMaterialForm.thickness),
        package_type: baseMaterialForm.package_type
      });
      toast({ title: "Материал создан успешно" });
      setShowForm(false);
      setBaseMaterialForm({ name: '', length: '', width: '', thickness: '', package_type: 'vacuum' });
    } catch (error) {
      console.error('Error creating base material:', error);
      toast({ 
        title: "Ошибка создания материала", 
        description: "Проверьте правильность введенных данных",
        variant: "destructive" 
      });
    }
  };

  const handleCreateTargetPackaging = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!targetPackagingForm.name || !targetPackagingForm.purpose || !targetPackagingForm.length || 
        !targetPackagingForm.width || !targetPackagingForm.package_type || !targetPackagingForm.seam_type) {
      toast({ 
        title: "Ошибка валидации", 
        description: "Все поля должны быть заполнены",
        variant: "destructive" 
      });
      return;
    }

    try {
      await createTargetPackaging.mutateAsync({
        name: targetPackagingForm.name.trim(),
        purpose: targetPackagingForm.purpose.trim(),
        length: parseFloat(targetPackagingForm.length),
        width: parseFloat(targetPackagingForm.width),
        package_type: targetPackagingForm.package_type,
        seam_type: targetPackagingForm.seam_type,
        is_two_streams: targetPackagingForm.is_two_streams
      });
      toast({ title: "Упаковка создана успешно" });
      setShowForm(false);
      setTargetPackagingForm({ 
        name: '', 
        purpose: '', 
        length: '', 
        width: '', 
        package_type: 'vacuum', 
        seam_type: 'double_seam', 
        is_two_streams: false 
      });
    } catch (error) {
      console.error('Error creating target packaging:', error);
      toast({ 
        title: "Ошибка создания упаковки", 
        description: "Проверьте правильность введенных данных",
        variant: "destructive" 
      });
    }
  };

  const handleCreateMachine = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createMachine.mutateAsync({
        name: machineForm.name,
        cutting_speed: parseFloat(machineForm.cutting_speed),
        machine_width: parseFloat(machineForm.machine_width)
      });
      toast({ title: "Станок создан успешно" });
      setShowForm(false);
      setMachineForm({ name: '', cutting_speed: '', machine_width: '' });
    } catch (error) {
      toast({ title: "Ошибка создания станка", variant: "destructive" });
    }
  };

  const handleDelete = async (type: string, id: number) => {
    try {
      if (type === 'baseMaterial') {
        await deleteBaseMaterial.mutateAsync(id);
      } else if (type === 'targetPackaging') {
        await deleteTargetPackaging.mutateAsync(id);
      } else if (type === 'machine') {
        await deleteMachine.mutateAsync(id);
      }
      toast({ title: "Удалено успешно" });
    } catch (error) {
      toast({ title: "Ошибка удаления", variant: "destructive" });
    }
  };

  const renderForm = () => {
    if (!showForm) return null;

    switch (activeTab) {
      case 'rawRolls':
        return (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Создать базовый материал</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreateBaseMaterial} className="space-y-4">
                <div>
                  <Label htmlFor="name">Название</Label>
                  <Input
                    id="name"
                    value={baseMaterialForm.name}
                    onChange={(e) => setBaseMaterialForm(prev => ({ ...prev, name: e.target.value }))}
                    required
                  />
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="length">Длина (мм)</Label>
                    <Input
                      id="length"
                      type="number"
                      value={baseMaterialForm.length}
                      onChange={(e) => setBaseMaterialForm(prev => ({ ...prev, length: e.target.value }))}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="width">Ширина (мм)</Label>
                    <Input
                      id="width"
                      type="number"
                      value={baseMaterialForm.width}
                      onChange={(e) => setBaseMaterialForm(prev => ({ ...prev, width: e.target.value }))}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="thickness">Толщина (мм)</Label>
                    <Input
                      id="thickness"
                      type="number"
                      step="0.1"
                      value={baseMaterialForm.thickness}
                      onChange={(e) => setBaseMaterialForm(prev => ({ ...prev, thickness: e.target.value }))}
                      required
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="package_type">Тип упаковки</Label>
                  <Select onValueChange={(value) => {
                    setBaseMaterialForm(prev => ({
                      ...prev,
                      package_type: value as PackagingType
                    }));
                  }}>
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
                <div className="flex space-x-2">
                  <Button type="submit" disabled={createBaseMaterial.isPending}>
                    {createBaseMaterial.isPending ? 'Создание...' : 'Создать'}
                  </Button>
                  <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                    Отмена
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        );

      case 'targetRolls':
        return (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Создать целевую упаковку</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreateTargetPackaging} className="space-y-4">
                <div>
                  <Label htmlFor="target-name">Название</Label>
                  <Input
                    id="target-name"
                    value={targetPackagingForm.name}
                    onChange={(e) => setTargetPackagingForm(prev => ({ ...prev, name: e.target.value }))}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="purpose">Назначение</Label>
                  <Input
                    id="purpose"
                    value={targetPackagingForm.purpose}
                    onChange={(e) => setTargetPackagingForm(prev => ({ ...prev, purpose: e.target.value }))}
                    required
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="target-length">Длина (мм)</Label>
                    <Input
                      id="target-length"
                      type="number"
                      value={targetPackagingForm.length}
                      onChange={(e) => setTargetPackagingForm(prev => ({ ...prev, length: e.target.value }))}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="target-width">Ширина (мм)</Label>
                    <Input
                      id="target-width"
                      type="number"
                      value={targetPackagingForm.width}
                      onChange={(e) => setTargetPackagingForm(prev => ({ ...prev, width: e.target.value }))}
                      required
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="target-package-type">Тип упаковки</Label>
                  <Select onValueChange={(value) => {
                    setTargetPackagingForm(prev => ({
                      ...prev,
                      package_type: value as PackagingType
                    }));
                  }}>
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
                  <Label htmlFor="seam-type">Тип шва</Label>
                  <Select onValueChange={(value) => {
                    setTargetPackagingForm(prev => ({
                      ...prev,
                      seam_type: value as SeamType
                    }));
                  }}>
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
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="two-streams"
                    checked={targetPackagingForm.is_two_streams}
                    onCheckedChange={(checked) => 
                      setTargetPackagingForm(prev => ({ ...prev, is_two_streams: checked === true }))
                    }
                  />
                  <Label htmlFor="two-streams">Двухпоточный</Label>
                </div>
                <div className="flex space-x-2">
                  <Button type="submit" disabled={createTargetPackaging.isPending}>
                    {createTargetPackaging.isPending ? 'Создание...' : 'Создать'}
                  </Button>
                  <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                    Отмена
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        );

      case 'machines':
        return (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Создать станок</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreateMachine} className="space-y-4">
                <div>
                  <Label htmlFor="machine-name">Название</Label>
                  <Input
                    id="machine-name"
                    value={machineForm.name}
                    onChange={(e) => setMachineForm(prev => ({ ...prev, name: e.target.value }))}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="cutting-speed">Скорость резки</Label>
                  <Input
                    id="cutting-speed"
                    type="number"
                    step="0.1"
                    value={machineForm.cutting_speed}
                    onChange={(e) => setMachineForm(prev => ({ ...prev, cutting_speed: e.target.value }))}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="machine-width">Ширина станка (мм)</Label>
                  <Input
                    id="machine-width"
                    type="number"
                    value={machineForm.machine_width}
                    onChange={(e) => setMachineForm(prev => ({ ...prev, machine_width: e.target.value }))}
                    required
                  />
                </div>
                <div className="flex space-x-2">
                  <Button type="submit" disabled={createMachine.isPending}>
                    {createMachine.isPending ? 'Создание...' : 'Создать'}
                  </Button>
                  <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                    Отмена
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        );
    }
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'rawRolls':
        if (baseMaterialsLoading) return <div>Загрузка...</div>;
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {baseMaterials.map((material) => (
              <Card key={material.id}>
                <CardHeader>
                  <CardTitle className="text-lg">{material.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p><span className="font-medium">Длина:</span> {material.length} мм</p>
                    <p><span className="font-medium">Ширина:</span> {material.width} мм</p>
                    <p><span className="font-medium">Толщина:</span> {material.thickness} мм</p>
                    <p><span className="font-medium">Тип упаковки:</span> {material.package_type}</p>
                  </div>
                  <div className="flex space-x-2 mt-4">
                    <Button variant="outline" size="sm">
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button 
                      variant="destructive" 
                      size="sm"
                      onClick={() => handleDelete('baseMaterial', material.id)}
                      disabled={deleteBaseMaterial.isPending}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        );

      case 'targetRolls':
        if (targetPackagingLoading) return <div>Загрузка...</div>;
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {targetPackaging.map((packaging) => (
              <Card key={packaging.id}>
                <CardHeader>
                  <CardTitle className="text-lg">{packaging.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p><span className="font-medium">Назначение:</span> {packaging.purpose}</p>
                    <p><span className="font-medium">Длина:</span> {packaging.length} мм</p>
                    <p><span className="font-medium">Ширина:</span> {packaging.width} мм</p>
                    <p><span className="font-medium">Тип упаковки:</span> {packaging.package_type}</p>
                    <p><span className="font-medium">Тип шва:</span> {packaging.seam_type}</p>
                    <p><span className="font-medium">Двухпоточный:</span> {packaging.is_two_streams ? 'Да' : 'Нет'}</p>
                  </div>
                  <div className="flex space-x-2 mt-4">
                    <Button variant="outline" size="sm">
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button 
                      variant="destructive" 
                      size="sm"
                      onClick={() => handleDelete('targetPackaging', packaging.id)}
                      disabled={deleteTargetPackaging.isPending}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        );

      case 'machines':
        if (machinesLoading) return <div>Загрузка...</div>;
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {machines.map((machine) => (
              <Card key={machine.id}>
                <CardHeader>
                  <CardTitle className="text-lg">{machine.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p><span className="font-medium">Скорость резки:</span> {machine.cutting_speed}</p>
                    <p><span className="font-medium">Ширина станка:</span> {machine.machine_width} мм</p>
                  </div>
                  <div className="flex space-x-2 mt-4">
                    <Button variant="outline" size="sm">
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button 
                      variant="destructive" 
                      size="sm"
                      onClick={() => handleDelete('machine', machine.id)}
                      disabled={deleteMachine.isPending}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="p-6 bg-white dark:bg-gray-900 text-gray-900 dark:text-white min-h-full">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">{getTranslation(language, 'resources')}</h1>
        <Button onClick={() => setShowForm(true)} className="bg-blue-600 hover:bg-blue-700">
          <Plus className="w-4 h-4 mr-2" />
          {getTranslation(language, 'create')}
        </Button>
      </div>

      {/* Вкладки */}
      <div className="mb-6">
        <div className="border-b border-gray-200 dark:border-gray-700">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => {
                setActiveTab('rawRolls');
                setShowForm(false);
              }}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'rawRolls'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              }`}
            >
              Базовые материалы
            </button>
            <button
              onClick={() => {
                setActiveTab('targetRolls');
                setShowForm(false);
              }}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'targetRolls'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              }`}
            >
              Целевые упаковки
            </button>
            <button
              onClick={() => {
                setActiveTab('machines');
                setShowForm(false);
              }}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'machines'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              }`}
            >
              Станки
            </button>
          </nav>
        </div>
      </div>

      {/* Форма создания */}
      {renderForm()}

      {/* Содержимое вкладок */}
      {renderTabContent()}
    </div>
  );
};

export default Resources;
