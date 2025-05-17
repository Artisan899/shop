# user/models.py
import hashlib
import uuid
import bcrypt
from typing import Dict, List

class User:
    def __init__(self, username: str, email: str, password_plain: str):
        self.username = username
        self.email = email
        self.password = self.hash_password(password_plain)
        self.bonus_card = {
            'id': str(uuid.uuid4()),
            'points': 1000
        }
        self.cart: Dict[str, int] = {}  # Словарь для хранения корзины: {"product_type_id": quantity}

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def add_to_cart(self, product_type: str, product_id: str, quantity: int = 1):
        key = f"{product_type}_{product_id}"
        self.cart[key] = self.cart.get(key, 0) + quantity

    def remove_from_cart(self, product_type: str, product_id: str):
        key = f"{product_type}_{product_id}"
        if key in self.cart:
            del self.cart[key]

    def update_cart_item(self, product_type: str, product_id: str, quantity: int):
        key = f"{product_type}_{product_id}"
        if quantity <= 0:
            self.remove_from_cart(product_type, product_id)
        else:
            self.cart[key] = quantity

    def clear_cart(self):
        self.cart = {}

    def get_cart_count(self) -> int:
        return sum(self.cart.values())

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'bonus_card': self.bonus_card,
            'cart': self.cart
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        user = cls(data['username'], data['email'], 'temp_password')
        user.password = data['password']
        user.bonus_card = data.get('bonus_card', {'id': str(uuid.uuid4()), 'points': 1000})
        user.cart = data.get('cart', {})
        return user