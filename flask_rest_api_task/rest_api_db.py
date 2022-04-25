from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'prekes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# DB objektas
class Preke(db.Model):
    __tablename__ = 'prekes'
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column("Pavadinimas", db.String)
    kaina = db.Column("Kaina", db.Float)
    kiekis = db.Column("Kiekis", db.Integer)


# Prekes schema
class PrekeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pavadinimas', 'kaina', 'kiekis')


preke_schema = PrekeSchema()
prekes_schema = PrekeSchema(many=True)


#CRUD
@app.route('/preke', methods=['POST'])
def prideti_preke():
    db.create_all()
    pavadinimas = request.json['pavadinimas']
    kaina = request.json['kaina']
    kiekis = request.json['kiekis']
    nauja_preke = Preke(pavadinimas=pavadinimas, kaina=kaina, kiekis=kiekis)
    db.session.add(nauja_preke)
    db.session.commit()
    return preke_schema.jsonify(nauja_preke)


@app.route('/preke', methods=['GET'])
def gauti_visas_prekes():
    visos_prekes = Preke.query.all()
    rezultatas = prekes_schema.dump(visos_prekes)
    return jsonify(rezultatas)


@app.route('/preke/<id>', methods=['GET'])
def gauti_preke(id):
    preke = Preke.query.get(id)
    return preke_schema.jsonify(preke)


@app.route('/preke/<id>', methods=['PUT'])
def pakeisti_preke(id):
    preke = Preke.query.get(id)
    preke.pavadinimas = request.json['pavadinimas']
    preke.kaina = request.json['kaina']
    preke.kiekis = request.json['kiekis']
    db.session.commit()
    return preke_schema.jsonify(preke)


@app.route('/preke/<id>', methods=['DELETE'])
def istrinti_preke(id):
    preke = Preke.query.get(id)
    if preke:
        db.session.delete(preke)
        db.session.commit()
        return preke_schema.jsonify(preke)
    else:
        {"error": "not found"}, 404


if __name__ == '__main__':
    app.run(host='10.250.0.47', port=5000, debug=True)
    db.create_all()
