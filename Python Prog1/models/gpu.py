# models/gpu.py
from models.base_product import BaseProduct

class GPU(BaseProduct):
    def __init__(self, id, name, price, category, memory, memory_type, clock_speed, image):
        self.id = id
        super().__init__(name, price, category)
        self.memory = memory  # Объем памяти (например, "8 GB")
        self.memory_type = memory_type  # Тип памяти (например, "GDDR6")
        self.clock_speed = clock_speed  # Тактовая частота
        self.image = image  # Путь к изображению

    def get_description(self):
        return f"Видеокарта {self.name} ({self.memory} {self.memory_type}, {self.clock_speed} MHz)"