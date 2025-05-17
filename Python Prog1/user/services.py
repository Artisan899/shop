import json
import bcrypt

from user.models import *

class UserService:
    def __init__(self, filepath):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        try:
            with open(self.filepath, 'r') as f:
                data = f.read().strip()
                if not data:
                    with open(self.filepath, 'w') as f:
                        json.dump([], f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def _load_users(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _save_users(self, users):
        with open(self.filepath, 'w') as f:
            json.dump(users, f, indent=4)

    def add_user(self, username, email, password):
        users = self._load_users()
        if any(user['email'] == email for user in users):
            raise ValueError("Пользователь с таким email уже существует.")

        new_user = User(username, email, password)
        users.append(new_user.to_dict())
        self._save_users(users)

    def get_user(self, username_or_email):
        users = self._load_users()
        for user in users:
            if user['username'] == username_or_email or user['email'] == username_or_email:
                return user
        return None

    def check_password(self, stored_password, provided_password):
        try:
            return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
        except Exception as e:
            print(f"Error checking password: {e}")
            return False

    def get_bonus_card(self, username_or_email):
        user = self.get_user(username_or_email)
        if user and 'bonus_card' in user:
            return user['bonus_card']
        return None

    def is_email_taken(self, email):
        users = self._load_users()
        return any(user['email'] == email for user in users)