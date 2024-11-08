import json
import time
from attacks import DDoSAttack, SQLInjectionAttack, PhishingAttack
from users import User

def save_attack_state(attack: Attack, user: User) -> None:
    attack_data = {
        "user": user.username,
        "type": attack.get_attack_type().value,
        "status": attack.status,
        "targets": attack.get_targets(),
        "params": {},
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
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
    
    with open(f"./ataques/{user.username}_attack_state.json", "w") as file:
        json.dump(attack_data, file, indent=4)
    print(f"Estado del ataque guardado para {user.username}: {attack_data}")


def load_attack_state(user: User) -> Attack:
    try:
        with open(f"./ataques/{user.username}_attack_state.json", "r") as file:
            attack_data = json.load(file)
            attack_type = AttackType(attack_data["type"])
            targets = attack_data["targets"]

            if attack_type == AttackType.DDoS:
                return DDoSAttack(
                    dst_url=targets[0],
                    n_ips=attack_data["params"]["n_ips"],
                    n_msg=attack_data["params"]["n_msg"],
                    threads=attack_data["params"]["threads"]
                )
            elif attack_type == AttackType.SQL_INJECTION:
                return SQLInjectionAttack(
                    target_url=targets[0],
                    payload=attack_data["params"]["payload"]
                )
            elif attack_type == AttackType.PHISHING:
                return PhishingAttack(
                    target_emails=attack_data["params"]["target_emails"],
                    template=attack_data["params"]["template"]
                )
    except (FileNotFoundError, json.JSONDecodeError):
        print("No se encontró un estado guardado o hubo un error al cargarlo.")
        return None
