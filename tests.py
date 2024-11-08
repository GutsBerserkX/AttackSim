import unittest
from attacks import DDoSAttack, SQLInjectionAttack, PhishingAttack, AttackType

class TestDDoSAttack(unittest.TestCase):

    def setUp(self):
        self.ddos_attack = DDoSAttack(dst_url="http://testphp.vulnweb.com", n_ips=10, n_msg=5, threads=2)

    def test_initialization(self):
        self.assertEqual(self.ddos_attack.dst_url, "http://testphp.vulnweb.com")
        self.assertEqual(self.ddos_attack.n_ips, 10)
        self.assertEqual(self.ddos_attack.n_msg, 5)
        self.assertEqual(self.ddos_attack.threads, 2)
        self.assertEqual(self.ddos_attack.get_attack_type(), AttackType.DDoS)
        self.assertEqual(self.ddos_attack.get_targets(), ["http://testphp.vulnweb.com"])
        self.assertEqual(self.ddos_attack.status, "pending")

    def test_start(self):
        self.ddos_attack.start()
        self.assertEqual(self.ddos_attack.status, "running")

    def test_pause(self):
        self.ddos_attack.pause()
        self.assertEqual(self.ddos_attack.status, "paused")

    def test_stop(self):
        self.ddos_attack.stop()
        self.assertEqual(self.ddos_attack.status, "stopped")


class TestSQLInjectionAttack(unittest.TestCase):

    def setUp(self):
        self.sql_injection_attack = SQLInjectionAttack(target_url="http:testphp.vulnweb.com/showimage.php?file=1", payload="OR 1=1")

    def test_initialization(self):
        self.assertEqual(self.sql_injection_attack.get_attack_type(), AttackType.SQL_INJECTION)
        self.assertEqual(self.sql_injection_attack.get_targets(), ["http:testphp.vulnweb.com/showimage.php?file=1"])
        self.assertEqual(self.sql_injection_attack.status, "pending")

    def test_start(self):
        self.sql_injection_attack.start()
        self.assertEqual(self.sql_injection_attack.status, "running")

    def test_pause(self):
        self.sql_injection_attack.pause()
        self.assertEqual(self.sql_injection_attack.status, "paused")

    def test_stop(self):
        self.sql_injection_attack.stop()
        self.assertEqual(self.sql_injection_attack.status, "stopped")


class TestPhishingAttack(unittest.TestCase):

    def setUp(self):
        self.phishing_attack = PhishingAttack(target_emails=["victim@example.com"], template="Phishing Template")

    def test_initialization(self):
        self.assertEqual(self.phishing_attack.get_attack_type(), AttackType.PHISHING)
        self.assertEqual(self.phishing_attack.get_targets(), ["victim@example.com"])
        self.assertEqual(self.phishing_attack.status, "pending")

    # def test_start(self):
    #     self.phishing_attack.start()
    #     self.assertEqual(self.phishing_attack.status, "running")

    # def test_pause(self):
    #     self.phishing_attack.pause()
    #     self.assertEqual(self.phishing_attack.status, "paused")

    # def test_stop(self):
    #     self.phishing_attack.stop()
    #     self.assertEqual(self.phishing_attack.status, "stopped")


if __name__ == '__main__':
    unittest.main()