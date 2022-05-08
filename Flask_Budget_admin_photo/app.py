import os
from flask import Flask, render_template, redirect, url_for, flash, request, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, logout_user, login_user, UserMixin, login_required
import forms
import secrets
from PIL import Image


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '4654f5dfadsrfasdr54e6rae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'new_budget.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'prisijungti'
login_manager.login_message_category = 'info'


class Vartotojas(db.Model, UserMixin):
    __tablename__ = "vartotojas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
    el_pastas = db.Column("El. pašto adresas", db.String(120), unique=True, nullable=False)
    nuotrauka = db.Column(db.String(20), nullable=False, default='default.jpg')
    slaptazodis = db.Column("Slaptažodis", db.String(60), unique=True, nullable=False)


class Irasas(db.Model):
    __tablename__ = "irasas"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column("Data", DateTime, default=datetime.now())
    suma = db.Column("Vardas", db.Integer)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey("vartotojas.id"))
    vartotojas = db.relationship("Vartotojas", lazy=True)


class ManoModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.el_pastas == "reda.tomonyte@gmail.com"


admin = Admin(app)
admin.add_view(ManoModelView(Vartotojas, db.session))
admin.add_view(ModelView(Irasas, db.session))


@login_manager.user_loader
def load_user(vartotojo_id):
    db.create_all()
    return Vartotojas.query.get(int(vartotojo_id))


@app.route("/registruotis", methods=['GET', 'POST'])
def registruotis():
    # db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegistracijosForma()
    if form.validate_on_submit():
        koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        vartotojas = Vartotojas(vardas=form.vardas.data, el_pastas=form.el_pastas.data, slaptazodis=koduotas_slaptazodis)
        db.session.add(vartotojas)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
        return redirect(url_for('index'))
    return render_template('registruotis.html', title='Register', form=form)


@app.route("/prisijungti", methods=['GET', 'POST'])
def prisijungti():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        is_matched = bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data)
        if user and is_matched:
            login_user(user, remember=form.prisiminti.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį', 'danger')
    return render_template('prisijungti.html', title='Prisijungti', form=form)


@app.route("/atsijungti")
def atsijungti():
    logout_user()
    return redirect(url_for('index'))


@app.route("/admin")
@login_required
def admin():
    return redirect(url_for(admin))


@app.route("/irasai")
@login_required
def records():
    db.create_all()
    page = request.args.get('page', 1, type=int)
    visi_irasai = Irasas.query.filter_by(vartotojas_id=current_user.id).order_by(Irasas.data.desc()).paginate(page=page,per_page=5)
    return render_template("irasai.html", visi_irasai=visi_irasai, datetime=datetime)


@app.route("/naujas_irasas", methods=["GET", "POST"])
def new_record():
    # db.create_all()
    forma = forms.IrasasForm()
    if forma.validate_on_submit():
        naujas_irasas = Irasas(suma=forma.suma.data, vartotojas_id=current_user.id)
        db.session.add(naujas_irasas)
        db.session.commit()
        flash(f"Įrašas sukurtas", 'success')
        return redirect(url_for('records'))
    return render_template("prideti_irasa.html", form=forma)


@app.route("/balansas")
def balance():
    try:
        visi_irasai = Irasas.query.filter_by(vartotojas_id=current_user.id)
    except:
        visi_irasai = []
    balansas = 0
    for irasas in visi_irasai:
        balansas += irasas.suma
    return render_template("balansas.html", balansas=balansas)


@app.route("/timetable")
@login_required
def timetable():
    return render_template('timetable.html', title='Timetable')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilio_nuotraukos', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/paskyra", methods=['GET', 'POST'])
@login_required
def paskyra():
    form = forms.PaskyrosAtnaujinimoForma()
    if form.validate_on_submit():
        if form.nuotrauka.data:
            nuotrauka = save_picture(form.nuotrauka.data)
            current_user.nuotrauka = nuotrauka
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        db.session.commit()
        flash('Tavo paskyra atnaujinta!', 'success')
        return redirect(url_for('paskyra'))
    elif request.method == 'GET':
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas
    nuotrauka = url_for('static', filename='profilio_nuotraukos/' + current_user.nuotrauka)
    return render_template('paskyra.html', title='Account', form=form, nuotrauka=nuotrauka)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
    db.create_all()
