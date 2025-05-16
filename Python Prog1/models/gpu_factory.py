import json
from models.gpu import GPU


class GPUFactory:
    @staticmethod
    def load_gpus_from_json(path):
        gpus = []
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            # Обработка изображений - поддерживаем как массив, так и одиночное изображение
            images = item['images'] if 'images' in item else [item['image']]

            gpu = GPU(
                id=str(item['id']),
                name=str(item['name']),
                price=float(item['price']),
                category=str(item.get('category', 'gpu')),
                memory=str(item['memory']),
                memory_type=str(item['memory_type']),
                clock_speed=str(item['clock_speed']),
                images=images
            )
            gpus.append(gpu)
        return gpus