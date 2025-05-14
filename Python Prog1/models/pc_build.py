from models.base_product import BaseProduct

class PCBuild(BaseProduct):
    def __init__(self, name, price, category, cpu, gpu, motherboard, ram, image):
        super().__init__(name, price, category)
        self.cpu = cpu
        self.gpu = gpu
        self.motherboard = motherboard
        self.ram = ram
        self.image = image

    def get_description(self):
        return f"CPU: {self.cpu}, GPU: {self.gpu}, RAM: {self.ram}, Motherboard: {self.motherboard}"
