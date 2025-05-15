# models/gpu_factory.py
import json
from models.gpu import GPU

class GPUFactory:
    @staticmethod
    def load_gpus_from_json(path):
        gpus = []
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            gpu = GPU(
                id=item['id'],
                name=item['name'],
                price=item['price'],
                category=item['category'],
                memory=item['memory'],
                memory_type=item['memory_type'],
                clock_speed=item['clock_speed'],
                image=item['image']
            )
            gpus.append(gpu)
        return gpus