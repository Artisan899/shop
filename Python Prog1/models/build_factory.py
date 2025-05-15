import json
from models.pc_build import PCBuild


class BuildFactory:
    @staticmethod
    def load_builds_from_json(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        builds = []
        for item in data:
            # Обработка изображений (поддержка старого и нового формата)
            image = item.get('image', item.get('images', ['default.jpg'])[0])
            images = item.get('images', [image])

            builds.append(PCBuild(
                id=str(item['id']),
                name=item['name'],
                price=float(item['price']),
                category=item.get('category', 'PC'),
                cpu=item['cpu'],
                gpu=item['gpu'],
                motherboard=item['motherboard'],
                ram=item['ram'],
                image=image,
                images=images
            ))
        return builds