import logging
from typing import List
from attacks import Attack
from reports import Report
from target_machine import VirtualMachineManager  # Asegúrate de que la ruta sea correcta

class AttackSim:
    def __init__(self, target_machines: List[TargetMachine]):
        """Inicializa la simulación con una lista de máquinas objetivo"""
        self.target_machines = target_machines
        # Configuramos el logging para registrar las actividades
        logging.basicConfig(filename='attacksim.log', level=logging.INFO)

    def configure_attack(self, attack: Attack, target_machine: TargetMachine):
        """Configura el ataque en la máquina objetivo seleccionada"""
        # Validamos si la máquina está en la lista de máquinas objetivo
        if target_machine not in self.target_machines:
            logging.warning(f"La máquina {target_machine.get_operating_system()} no está disponible.")
            print(f"La máquina objetivo {target_machine.get_operating_system()} no está disponible.")
            return
        # Si la máquina es válida, configuramos el ataque
        logging.info(f"Configurando {attack.__class__.__name__} en {target_machine.get_operating_system()}")
        print(f"Configurando {attack.__class__.__name__} en {target_machine.get_operating_system()}")
        target_machine.simulate_response()  # Método a definir en TargetMachine

    def execute_attack(self, attack: Attack, target_machine: TargetMachine):
        """Ejecuta el ataque configurado en la máquina objetivo"""
        # Validamos si la máquina está en la lista de máquinas objetivo antes de ejecutar el ataque
        if target_machine not in self.target_machines:
            logging.warning(f"No se puede ejecutar el ataque en {target_machine.get_operating_system()}, la máquina no está en la lista.")
            print(f"No se puede ejecutar el ataque en {target_machine.get_operating_system()}, la máquina no está en la lista.")
            return
        # Si la máquina es válida, ejecutamos el ataque
        logging.info(f"Ejecutando {attack.__class__.__name__} en {target_machine.get_operating_system()}")
        print(f"Ejecutando {attack.__class__.__name__} en {target_machine.get_operating_system()}")
        attack.start()

    def generate_report(self, attack: Attack, report: Report):
        """Genera un reporte después de ejecutar el ataque"""
        logging.info(f"Generando reporte para {attack.__class__.__name__}")
        print(f"Generando reporte para {attack.__class__.__name__}")
        report.generate_pdf()
