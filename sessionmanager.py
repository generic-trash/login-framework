from datetime import datetime
import random
import string


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session_for_user(self, username):
        uuid = self.gen_random_id()
        self.sessions[uuid] = username
        return uuid

    @staticmethod
    def gen_random_id():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=128))

    def get_session(self, sessid):
        try:
            return self.sessions[sessid]
        except KeyError:
            return None

    def delete_session(self, sessid):
        try:
            del self.sessions[sessid]
            return True
        except KeyError:
            return False
