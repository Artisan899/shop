from models.base_product import BaseProduct

class GPU(BaseProduct):
    def __init__(self, id, name, price, category, memory, memory_type, clock_speed, images):
        super().__init__(name, price, category)
        self.id = id
        self.memory = memory
        self.memory_type = memory_type
        self.clock_speed = clock_speed
        self.images = images if isinstance(images, list) else [images]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'memory': self.memory,
            'memory_type': self.memory_type,
            'clock_speed': self.clock_speed,
            'images': self.images
        }