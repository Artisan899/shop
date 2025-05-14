import json
import bcrypt  # Импортируем библиотеку для хэширования паролей

class UserService:
    def __init__(self, filepath):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        """Проверка на наличие файла, создание при необходимости, и его правильное форматирование."""
        try:
            with open(self.filepath, 'r') as f:
                # Пробуем загрузить содержимое файла
                data = f.read().strip()
                if not data:  # Если файл пустой, записываем пустой список
                    with open(self.filepath, 'w') as f:
                        json.dump([], f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файла нет или он повреждён, создаём пустой файл
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def _load_users(self):
        """Загрузка всех пользователей из файла."""
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _save_users(self, users):
        """Сохранение списка пользователей в файл."""
        with open(self.filepath, 'w') as f:
            json.dump(users, f)

    def add_user(self, username, email, password):
        """Добавление нового пользователя с хэшированием пароля."""
        users = self._load_users()
        if any(user['email'] == email for user in users):
            raise ValueError("Пользователь с таким email уже существует.")
        # Хэшируем пароль перед сохранением
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.append({"username": username, "email": email, "password": hashed_password.decode('utf-8')})
        self._save_users(users)

    def get_user(self, username_or_email):
        """Поиск пользователя по имени или email."""
        users = self._load_users()
        for user in users:
            if user['username'] == username_or_email or user['email'] == username_or_email:
                return user
        return None

    def check_password(self, stored_password, provided_password):
        """Проверка пароля с хэшированием."""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
