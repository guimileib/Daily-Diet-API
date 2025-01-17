from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, unique=False)
    refeicoes = db.relationship('Refeicao', backref='user', lazy=True)
    
class Refeicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
    data_hora = db.Column(db.DateTime, nullable=False)
    dieta = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    