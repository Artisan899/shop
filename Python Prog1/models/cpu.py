from models.base_product import BaseProduct

class CPU(BaseProduct):
    def __init__(self, id, name, price, category, frequency, socket, cores, cpu_type, images=None):
        super().__init__(name, price, category)
        self.id = id
        self.frequency = frequency
        self.socket = socket
        self.cores = cores
        self.type = cpu_type
        self.images = images or []

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'frequency': self.frequency,
            'socket': self.socket,
            'cores': self.cores,
            'type': self.type,
            'images': self.images
        }