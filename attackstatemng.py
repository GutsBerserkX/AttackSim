import json
import time
import os
from attacks import DDoSAttack, SQLInjectionAttack, PhishingAttack, Attack, AttackType
from users import User

def save_attack_state(attack: Attack, username: str) -> None:
    attack_data = {
        "user": username,
        "type": attack.get_attack_type().value,
        "status": "Stopped",  # Cambiado a "Stopped"
        "targets": attack.get_targets(),
        "params": {},
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": attack.duration,
        "result": attack.result
    }
    
    # Guardamos parámetros de cada ataque según su tipo
    if isinstance(attack, DDoSAttack):
        attack_data["params"] = {
            "dst_url": attack.get_target_url(),
            "n_ips": attack.n_ips,
            "n_msg": attack.n_msg,
            "threads": attack.threads
        }
    elif isinstance(attack, SQLInjectionAttack):
        attack_data["params"] = {
            "target_url": attack.get_target_url(),
            "payload": attack.payload
        }
    elif isinstance(attack, PhishingAttack):
        attack_data["params"] = {
            "target_emails": attack.get_target_url(),
            "template": attack.template
        }
    
    # Crear directorio si no existe
    os.makedirs("./ataques", exist_ok=True)

    # Generar archivo dependiendo del tipo de ataque
    attack_type = attack.get_attack_type().value
    filename = f"./ataques/{username}_{attack_type}_attack_state.json"
    
    with open(filename, "w") as file:
        json.dump(attack_data, file, indent=4)
    print(f"Estado del ataque guardado para {username} en {filename}: {attack_data}")