from config.db import db

class Producto(db.Model):
    __tablename__ = "productos"

    productoID = db.Column(db.Integer, primary_key=True)
    tipo_producto = db.Column(db.String(45), nullable=False)
    ingrediente1 = db.Column(db.Integer, db.ForeignKey("ingredientes.ingredienteID"), nullable=False)
    ingrediente2 = db.Column(db.Integer, db.ForeignKey("ingredientes.ingredienteID"), nullable=False)
    ingrediente3 = db.Column(db.Integer, db.ForeignKey("ingredientes.ingredienteID"), nullable=False)


