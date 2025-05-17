import hashlib
import uuid
import bcrypt

class User:
    def __init__(self, username, email, password_plain):
        self.username = username
        self.email = email
        self.password = self.hash_password(password_plain)  # Теперь используем bcrypt
        # Создаем бонусную карту при инициализации пользователя
        self.bonus_card = {
            'id': str(uuid.uuid4()),  # Генерируем уникальный ID для карты
            'points': 1000  # Начальный бонус при создании
        }

    def hash_password(self, password):
        # Используем bcrypt вместо hashlib для совместимости
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'bonus_card': self.bonus_card
        }