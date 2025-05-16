# build_factory.py
from models.pc_build import PCBuild
import json


class BuildFactory:
    @staticmethod
    def load_builds_from_json(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        builds = []
        for item in data:
            builds.append(PCBuild(
                id=item['id'],
                name=item['name'],
                price=item['price'],
                category='PC',
                cpu=item['cpu'],
                gpu=item['gpu'],
                motherboard=item['motherboard'],
                ram=item['ram'],
                images=item.get('images', [item.get('image')])
            ))
        return builds