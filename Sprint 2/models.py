from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from main import db_alchemy

class Users(db_alchemy.Model, UserMixin):
    
    __tablename__ = 'profesor'

    rut = db_alchemy.Column(db_alchemy.String(13), primary_key=True)
    nombre = db_alchemy.Column(db_alchemy.String(200), nullable=False)
    email = db_alchemy.Column(db_alchemy.String(256), unique=True, nullable=False)
    password = db_alchemy.Column(db_alchemy.String(512), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_id(self):
        return self.rut

    @staticmethod
    def get_by_id(id):
        return Users.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(email = email).first()

    def get_name(self):
        return self.nombre
