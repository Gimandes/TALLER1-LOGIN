from flask import Flask, render_template, request, redirect, url_for, flash, redirect, url_for
from config.config import Config
from config.db import db
from models.ingrediente import Ingrediente
from models.producto import Producto
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default = False)
    email = db.Column(db.String(120), nullable=False, default = False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/dashboard_admin")
@login_required
def dashboard_admin():
    return render_template("dashboard_admin.html")

@app.route("/auth/profile")
@login_required
def auth_profile():
    if current_user.is_admin:
        return f"datos: {current_user.username}- {current_user.password} - {current_user.email}"
    return f"datos: {current_user.username}- {current_user.password}"

@app.route("/logout")
def logout():
    logout_user()
    return render_template("login.html")

@app.route("/vender")
@login_required
def mostrar_vender():
    return render_template("vender.html") 

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/auth", methods=["GET"]) 
def auth():
    username = request.args.get("username")  
    password = request.args.get("password")

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        login_user(user)
        if user.is_admin: 
            return redirect(url_for("dashboard_admin"))
        return redirect(url_for("dashboard"))
    flash ("Las credenciales no estan registradas en nuestro sistema.", "error")
    return render_template("login.html", error="Usuario o contraseña incorrectos")






"""with app.app_context():
    db.create_all"""
     




@app.route("/ingredientes")
@login_required
def mostrar_ingredientes():
    ingredientes = Ingrediente.query.all()
    return render_template("ingredientes.html", ingredientes=ingredientes)

@app.route("/productos")
@login_required
def mostrar_productos():
    productos = Producto.query.all()
    return render_template("productos.html", productos=productos)

def vender(nombre_producto):
    producto = Producto.query.filter_by(nombre=nombre_producto).first()
    if not producto:
        return f"¡Oh no! No tenemos {nombre_producto}"

    ingredientes = [producto.ingrediente1_id, producto.ingrediente2_id, producto.ingrediente3_id]
    for ing_id in ingredientes:
        ingrediente = Ingrediente.query.get(ing_id)
        if ingrediente and ingrediente.inventario <= 0:
            raise ValueError(f"¡Oh no! Nos hemos quedado sin {ingrediente.nombre}")

    # Reducir inventario
    for ing_id in ingredientes:
        ingrediente = Ingrediente.query.get(ing_id)
        ingrediente.inventario -= 1

    return "¡Vendido!"

if __name__ == '__main__':
    app.run(debug=True)