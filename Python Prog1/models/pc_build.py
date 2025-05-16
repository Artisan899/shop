from models.base_product import BaseProduct

class PCBuild(BaseProduct):
    def __init__(self, id, name, price, category, cpu, gpu, motherboard, ram, images):
        super().__init__(name, price, category)
        self.id = id
        self.cpu = cpu
        self.gpu = gpu
        self.motherboard = motherboard
        self.ram = ram
        self.images = images

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'cpu': self.cpu,
            'gpu': self.gpu,
            'motherboard': self.motherboard,
            'ram': self.ram,
            'images': self.images
        }