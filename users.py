from enum import Enum
from attacks import Attack, AttackType
import json

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class User():
    def __init__(self, username: str, role: Role):
        self.username = username
        self.role = role
        self.attacks = []

    def can_access_attack(self, attack_type: AttackType) -> bool:
        if self.role == Role.ADMIN:
            return True
        if self.role == Role.USER and attack_type in [AttackType.PHISHING, AttackType.SQL_INJECTION]:
            return True
        return False

    def add_attack(self, attack: Attack) -> None:
        self.attacks.append(attack)

    def history_attacks(self):
        return self.attacks

class UserManager:
    def __init__(self):
        self.users = [Pepe]

    def add_user(self, username: str, role: Role, ) -> None:
        self.users.append(User(username, role))

    def get_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def remove_user(self, username: str) -> bool:
        user = self.get_user(username)
        if user:
            self.users.remove(user)
            return True
        return False
    
    def save_users(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            for user in self.users:
                file.write(f"{user.username},{user.role.value}\n")

    def load_users(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                self.users = []
                for line in file:
                    username, role = line.strip().split(',')
                    self.users.append(User(username, Role(role)))
        except FileNotFoundError:
            self.users = []



Pepe = User("Pepe", Role.USER)
