from sqlalchemy import DateTime
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from budget import app, db, admin
# Imports for Flask Admin configuration
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user



class Vartotojas(db.Model, UserMixin):
    __tablename__ = "vartotojas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
    el_pastas = db.Column("El. pašto adresas", db.String(120), unique=True, nullable=False)
    nuotrauka = db.Column(db.String(20), nullable=False, default='default.jpg')
    slaptazodis = db.Column("Slaptažodis", db.String(60), unique=True, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Vartotojas.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Irasas(db.Model):
    __tablename__ = "irasas"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column("Data", DateTime, default=datetime.now())
    suma = db.Column("Vardas", db.Integer)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey("vartotojas.id"))
    vartotojas = db.relationship("Vartotojas", lazy=True)


# Flask Admin Class configuration
class ManoModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.el_pastas == "reda.tomonyte@gmail.com"


admin.add_view(ManoModelView(Vartotojas, db.session))
admin.add_view(ModelView(Irasas, db.session))
