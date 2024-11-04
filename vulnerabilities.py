# Clase que representa una vulnerabilidad en una máquina objetivo
class Vulnerability:
    def __init__(self, name: str, description: str):
        """Inicializa una vulnerabilidad con un nombre y descripción"""
        self.name = name
        self.description = description

    def exploit(self):
        """Simula la explotación de la vulnerabilidad"""
        print(f"Explotando la vulnerabilidad: {self.name}")
        print(f"Descripción: {self.description}")
