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
