from basedb import *


class UserDB(BaseDB):
    def __init__(self, dbfile="dbs/users.jsdb"):
        super().__init__(dbfile)

    def check_pass(self, username, password):
        if username not in self.data:
            return False

        if self.data[username]["password"] == password:
            return True

        return False

    @staticmethod
    def serialize(func):
        def dummy_serialize(self, *args, **kwargs):
            val = func(self, *args, **kwargs)
            self._serialize()
            return val

        return dummy_serialize

    @staticmethod
    def ok(func):
        def ok_wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)
            if ret is None:
                return dict(status=200)
            if "status" not in ret:
                ret["status"] = 200

            return ret

        return ok_wrapper

    @staticmethod
    def if_user_exists(func):
        def validate_wrapper(self, username, *args, **kwargs):
            if username not in self.data:
                return dict(status=404, error="User Not Found")
            else:
                return func(self, username, *args, **kwargs)

        return validate_wrapper

    @serialize
    def add_user(self, username, email, password, confirm):
        if password != confirm:
            return dict(status=400, error="Passwords do not Match")
        if username in self.data:
            return dict(status=409, error="User already exists")
        self.data[username] = {
            "email": email,
            "password": password,
            "publicdata": {},
            "privatedata": {}
        }
        return dict(status=200)

    @serialize
    @if_user_exists
    @ok
    def del_user(self, username):
        del self.data[username]

    @serialize
    @if_user_exists
    @ok
    def update_public_data(self, username, data):
        self.data[username]["publicdata"].update(data)
        return dict(data=self.data[username]["publicdata"])

    @serialize
    @if_user_exists
    @ok
    def set_public_data(self, username, data):
        self.data[username]["publicdata"] = data

    @if_user_exists
    @ok
    def get_public_data(self, username):
        return dict(data=self.data[username]["publicdata"])

    @serialize
    @if_user_exists
    @ok
    def update_private_data(self, username, data):
        self.data[username]["privatedata"].update(data)
        return dict(data=self.data[username]["privatedata"])

    @serialize
    @if_user_exists
    @ok
    def set_private_data(self, username, data):
        self.data[username]["privatedata"] = data

    @if_user_exists
    @ok
    def get_private_data(self, username):
        return dict(data=self.data[username]["privatedata"])

    @if_user_exists
    @ok
    def get_email(self, username):
        return dict(data=self.data[username]["email"])

    @serialize
    @if_user_exists
    @ok
    def set_email(self, username, email):
        self.data[username]["email"] = email
