import json
from models.motherboard import Motherboard

class MotherboardFactory:
    @staticmethod
    def load_motherboards_from_json(path):
        motherboards = []
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            # Обработка изображений - поддерживаем как массив, так и одиночное изображение
            images = item['images'] if 'images' in item else [item['image']]

            motherboard = Motherboard(
                id=str(item['id']),
                name=str(item['name']),
                price=float(item['price']),
                category=str(item.get('category', 'motherboard')),
                socket=str(item['socket']),
                memory_support=str(item['memory_support']),
                slots=str(item['slots']),
                images=images
            )
            motherboards.append(motherboard)
        return motherboards