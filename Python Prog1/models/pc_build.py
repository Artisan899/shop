from models.base_product import BaseProduct

class PCBuild(BaseProduct):
    def __init__(self, id, name, price, category, cpu, gpu, motherboard, ram, image, images=None):
        super().__init__(name, price, category)
        self.id = id
        self.cpu = cpu
        self.gpu = gpu
        self.motherboard = motherboard
        self.ram = ram
        self.image = image
        self.images = images or [image]

    def get_description(self):
        return (
            f"Сборка ПК: {self.name}\n"
            f"Процессор: {self.cpu}\n"
            f"Видеокарта: {self.gpu}\n"
            f"Материнская плата: {self.motherboard}\n"
            f"Оперативная память: {self.ram}"
        )