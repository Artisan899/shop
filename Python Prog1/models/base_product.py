from abc import ABC, abstractmethod

class BaseProduct(ABC):
    def __init__(self, name: str, price: float, category: str):
        self.name = name
        self.price = price
        self.category = category

    @abstractmethod
    def get_description(self):
        pass
