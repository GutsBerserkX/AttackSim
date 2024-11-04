from typing import List
import pyvbox  # Asegúrate de que pyvbox esté instalado

class TargetMachine:
    def __init__(self, operating_system: str, vulnerabilities: List[str]):
        """Inicializa la máquina objetivo"""
        self.__operating_system = operating_system  # Encapsulamos el sistema operativo
        self.__vulnerabilities = vulnerabilities  # Encapsulamos las vulnerabilidades

    # Getter para obtener el sistema operativo
    def get_operating_system(self):
        return self.__operating_system

    # Setter para modificar el sistema operativo (opcional)
    def set_operating_system(self, operating_system: str):
        if isinstance(operating_system, str):
            self.__operating_system = operating_system

    # Getter para obtener las vulnerabilidades
    def get_vulnerabilities(self):
        return self.__vulnerabilities

    # Setter para modificar las vulnerabilidades
    def set_vulnerabilities(self, vulnerabilities: List[str]):
        if isinstance(vulnerabilities, list):
            self.__vulnerabilities = vulnerabilities


class Vulnerability:
    def __init__(self, name: str, description: str):
        self.__name = name  # Atributo privado
        self.__description = description  # Atributo privado

    # Getter para obtener el nombre
    def get_name(self):
        return self.__name

    # Setter para modificar el nombre (opcional)
    def set_name(self, name: str):
        if isinstance(name, str):
            self.__name = name

    # Getter para obtener la descripción
    def get_description(self):
        return self.__description

    # Setter para modificar la descripción (opcional)
    def set_description(self, description: str):
        if isinstance(description, str):
            self.__description = description


class VirtualMachineManager:
    def __init__(self):
        self.virtualbox = pyvbox.VirtualBox()  # Crear una instancia de VirtualBox
        self.virtual_machines = []  # Lista para almacenar las máquinas virtuales creadas

    def create_vm(self, name: str, os_type: str):
        """Crea una máquina virtual y la añade a la lista"""
        try:
            vm = self.virtualbox.create_machine(name=name, os_type_id=os_type, 
                                                settings_file="", 
                                                description="", 
                                                groups=[], 
                                                flags="")
            self.virtualbox.register_machine(vm)
            self.virtual_machines.append(vm)  # Añadir a la lista de máquinas virtuales
            print(f"Máquina virtual '{name}' creada con éxito.")
            return vm
        except Exception as e:
            print(f"Error al crear la máquina virtual: {e}")
            return None

    def start_vm(self, vm: pyvbox.Machine):
        """Inicia la máquina virtual"""
        session = pyvbox.Session()
        try:
            progress = vm.launch_vm_process(session, "headless", [])
            progress.wait_for_completion(-1)  # Esperar hasta que se complete
            print(f"Máquina virtual '{vm.name}' iniciada.")
        except Exception as e:
            print(f"Error al iniciar la máquina virtual: {e}")

    def stop_vm(self, vm: pyvbox.Machine):
        """Detiene la máquina virtual"""
        session = pyvbox.Session()
        try:
            vm.lock_machine(session, pyvbox.LockType.shared)
            session.console.power_down()  # Apagar la máquina
            print(f"Máquina virtual '{vm.name}' detenida.")
        except Exception as e:
            print(f"Error al detener la máquina virtual: {e}")

    def list_vms(self):
        """Lista todas las máquinas virtuales creadas"""
        if not self.virtual_machines:
            print("No hay máquinas virtuales creadas.")
            return
        print("Máquinas virtuales creadas:")
        for vm in self.virtual_machines:
            print(f" - {vm.name}")


# Ejemplo de uso de las clases (descomentar si se desea ejecutar)
# if __name__ == "__main__":
#     manager = VirtualMachineManager()
#     new_vm = manager.create_vm("TestVM", "Ubuntu_64")
#     if new_vm:
#         manager.start_vm(new_vm)
#         # manager.stop_vm(new_vm)
#     manager.list_vms()  # Mostrar la lista de máquinas virtuales creadas
