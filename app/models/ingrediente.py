from config.db import db

class Ingrediente(db.Model):
    __tablename__ = "ingredientes"
    ingredienteID = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    vegetariano = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    inventario = db.Column(db.Integer, nullable=False)