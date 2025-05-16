# cpu_factory.py
from models.cpu import CPU
import json


class CPUFactory:
    @staticmethod
    def load_cpus_from_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        cpus = []
        for item in data:
            cpus.append(CPU(
                id=item['id'],
                name=item['name'],
                price=item['price'],
                category='CPU',
                frequency=item['frequency'],
                socket=item['socket'],
                cores=item['cores'],
                cpu_type=item.get('type', ''),
                images=item['images']
            ))
        return cpus