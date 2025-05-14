import hashlib

class User:
    def __init__(self, username, email, password_plain):
        self.username = username
        self.email = email
        self.password = self.hash_password(password_plain)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
