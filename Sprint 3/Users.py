import modulo8 as bd
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

con = bd.connect()

class User(UserMixin):
    def __init__(self, id, name, email, password, active = True):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
        
    def login(self):
        self.ID_RUT = bd.get_rut_profesor(con, self.email)
        return self.ID_RUT

    @staticmethod
    def get_by_email(email):
        return bd.get_rut_profesor(con, email)
