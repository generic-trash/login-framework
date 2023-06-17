import unittest
from userdb import *


class UserDBTests(unittest.TestCase):
    baseEmail = "potato@potato.com"

    @classmethod
    def setUpClass(cls) -> None:
        with open("dbs/users_test.jsdb", "w") as users:
            users.write("{}")
        cls.userdb = UserDB("dbs/users_test.jsdb")

    def setUp(self):
        self.userdb.add_user("baseUser", self.baseEmail, "fried", "fried")

    def test_add_user(self):
        status = self.userdb.add_user("hello", self.baseEmail, "fried")
        assert status['status'] == 200
        status = self.userdb.add_user("hello", self.baseEmail, "baked")
        assert status['status'] == 409

    def test_del_user(self):
        status = self.userdb.del_user("baseUser")
        assert status['status'] == 200
        status = self.userdb.del_user("nonExistentUser")
        assert status['status'] == 404
        status = self.userdb.del_user("baseUser")
        assert status['status'] == 404

    def test_get_email(self):
        status = self.userdb.get_email("nonExistentUser")
        assert status['status'] == 404
        status = self.userdb.get_email("baseUser")
        assert status['status'] == 200 and status["data"] == self.baseEmail

    def test_update_email(self):
        status = self.userdb.set_email("nonExistentUser", "fried@potato.com")
        assert status['status'] == 404
        status = self.userdb.set_email("baseUser", "fried@notato.com")
        assert status['status'] == 200
        assert self.userdb.get_email("baseUser")["data"] == "fried@notato.com"

    def test_get_set_public_data(self):
        dataset = {
            "whoami": "root",
            "privilege": "NTAUTHORITY/SYSTEM"
        }
        dataset_updated = {
            "whoami": "root",
            "privilege": "NTAUTHORITY/SYSTEM",
            "swag": "ohio"
        }
        status = self.userdb.get_public_data("baseUser")
        assert status['status'] == 200
        assert status['data'] == {}
        status = self.userdb.set_public_data("baseUser", dataset)
        assert status['status'] == 200
        status = self.userdb.get_public_data("baseUser")
        assert status['status'] == 200
        assert status['data'] == dataset
        status = self.userdb.update_public_data("baseUser", {"swag": "ohio"})
        assert status['status'] == 200
        assert status['data'] == dataset_updated

    def test_get_set_private_data(self):
        dataset = {
            "whoami": "root",
            "privilege": "NTAUTHORITY/SYSTEM"
        }
        dataset_updated = {
            "whoami": "root",
            "privilege": "NTAUTHORITY/SYSTEM",
            "swag": "ohio"
        }
        status = self.userdb.get_private_data("baseUser")
        assert status['status'] == 200
        assert status['data'] == {}
        status = self.userdb.set_private_data("baseUser", dataset)
        assert status['status'] == 200
        status = self.userdb.get_private_data("baseUser")
        assert status['status'] == 200
        assert status['data'] == dataset
        status = self.userdb.update_private_data("baseUser", {"swag": "ohio"})
        assert status['status'] == 200
        assert status['data'] == dataset_updated

    def test_check_pass(self):
        assert self.userdb.check_pass("baseUser", "fried")
        assert not self.userdb.check_pass("baseUser", "baked")
        assert not self.userdb.check_pass("nonExistentUser", "fried")


if __name__ == '__main__':
    unittest.main()
