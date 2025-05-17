from models.base_product import BaseProduct

class Motherboard(BaseProduct):
    def __init__(self, id, name, price, category, socket, memory_support, slots, images):
        super().__init__(name, price, category)
        self.id = id
        self.socket = socket  # Тип сокета (например, LGA1700, AM5)
        self.memory_support = memory_support  # Поддерживаемая память (например, "DDR5")
        self.slots = slots  # Слоты расширения (например, "2x PCIe 5.0 x16")
        self.images = images if isinstance(images, list) else [images]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'socket': self.socket,
            'memory_support': self.memory_support,
            'slots': self.slots,
            'images': self.images
        }