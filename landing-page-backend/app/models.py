from .extensions import db
from werkzeug.security import check_password_hash, generate_password_hash

class WaitingList(db.Model):
    __tablename__ = "waiting_list"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), index=True, nullable=True, unique=True)
    phone = db.Column(db.String(255), index=True, nullable=True, unique=True)

    def __repr__(self):
        return f"<ID: {self.id} | Name: {self.name}>"


class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="admin")
    email = db.Column(db.String(255), index=True, nullable=True, unique=True)
    phone = db.Column(db.String(255), index=True, nullable=True, unique=True)
    password_hash = db.Column(db.String(255), index=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)