
import React from 'react';
import { Button } from '@/components/ui/button';

const mockPallets = [
  {
    id: 1,
    name: 'Палета №1',
    items: 150,
    weight: '45.2 кг',
    status: 'Готова к отправке'
  },
  {
    id: 2,
    name: 'Палета №2',
    items: 120,
    weight: '38.7 кг',
    status: 'В процессе'
  }
];

const Pallets: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Палеты</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockPallets.map((pallet) => (
          <div key={pallet.id} className="bg-white rounded-lg border p-6">
            <h3 className="text-lg font-semibold mb-4">{pallet.name}</h3>
            <div className="space-y-2">
              <p><span className="font-medium">Количество:</span> {pallet.items} шт</p>
              <p><span className="font-medium">Вес:</span> {pallet.weight}</p>
              <p><span className="font-medium">Статус:</span> 
                <span className={`ml-2 px-2 py-1 rounded text-sm ${
                  pallet.status === 'Готова к отправке' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {pallet.status}
                </span>
              </p>
            </div>
            <div className="flex space-x-2 mt-4">
              <Button variant="outline" size="sm">Изменить</Button>
              <Button variant="destructive" size="sm">Удалить</Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Pallets;
