from typing import List
import pyvbox 

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
