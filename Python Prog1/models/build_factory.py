import json
from models.pc_build import PCBuild


class BuildFactory:
    @staticmethod
    def load_builds_from_json(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        builds = []
        for item in data:
            builds.append({
                'id': item['id'],
                'name': item['name'],
                'price': item['price'],
                'images': item.get('images', [item.get('image')]),
                'cpu': item['cpu'],
                'gpu': item['gpu'],
                'motherboard': item['motherboard'],
                'ram': item['ram']
            })
        return builds