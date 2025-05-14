import json
from models.pc_build import PCBuild

class BuildFactory:
    @staticmethod
    def load_builds_from_json(path):
        builds = []
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            build = PCBuild(
                name=item['name'],
                price=item['price'],
                category=item['category'],
                cpu=item['cpu'],
                gpu=item['gpu'],
                motherboard=item['motherboard'],
                ram=item['ram'],
                image=item['image']
            )
            builds.append(build)
        return builds
