from flask import Flask, render_template, request, redirect, url_for, abort
import json

from werkzeug.utils import secure_filename

from forms import FormArticulo
from models import Categorias, Inventario, Proveedores
from flask_login import LoginManager, current_user, login_required
from getpass import getpass
import db
from config import SECRET_KEY
from catego import catego
from article import article
from providers import providers
from users import users
from compra import compra
from graphics import graphics

app = Flask(__name__)
app.register_blueprint(catego)
app.register_blueprint(article)
app.register_blueprint(providers)
app.register_blueprint(users)
app.register_blueprint(compra)
app.register_blueprint(graphics)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/")
def portada():
    categorias = db.session.query(Categorias).all()
    return render_template("portada.html", categorias=categorias)


@app.route("/index")
@app.route("/categorias/<id>")
def home(id="1"):
    categoria = db.session.query(Categorias).get(id)
    if id == "1":
        todos_los_articulos = db.session.query(Inventario).filter_by(activo=True).all()
    else:
        todos_los_articulos = db.session.query(Inventario).filter_by(CategoriaId=id, activo=True)
    categorias = db.session.query(Categorias).all()
    alarmas_stock = []
    stock = db.session.query(Inventario).all()
    for alrm in stock:
        if alrm.stock < 20:
            alarmas_stock.append(alrm.id)
    numero_alarmas = len(alarmas_stock)
    return render_template("index.html", todos_los_articulos=todos_los_articulos,
                           categorias=categorias, categoria=categoria, alarmas_stock=alarmas_stock,
                           numero_alarmas=numero_alarmas)


@login_manager.user_loader
def load_user(user_id):
    from models import Usuarios
    return db.session.query(Usuarios).get(int(user_id))


@app.route('/set_cookie')
def set_cookie():
    redirect_to_index = redirect('/')
    response = app.make_response(redirect_to_index)
    response.set_cookie('cookie_name', value='Tenemos una cookie')
    return response


@app.route('/get_cookie')
def get_cookie():
    datos = request.cookies.get('cookie_name')
    if datos != None:
        return datos
    else:
        return "No hay cookie"


@app.route('/del_cookie')
def del_cookie():
    redirect_to_index = redirect('/index')
    response = app.make_response(redirect_to_index)
    response.set_cookie('cookie_name', value='', expires=0)
    return response


@app.context_processor
def contar_carrito():
    if not current_user.is_authenticated:
        return {'num_articulos': 0}
    if request.cookies.get(str(current_user.id)) is None:
        return {'num_articulos': 0}
    else:
        datos = json.loads(request.cookies.get(str(current_user.id)))
        return {'num_articulos': len(datos)}


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404


def crear_admin():
    from models import Usuarios
    administrador = db.session.query(Usuarios).get(1)
    try:
        print(administrador.username)
        return
    except:
        print("INTRODUZCA LOS DATOS PARA ADMINISTRADOR")
        usuario = {"username": input("Usuario:"),
                   "password": getpass("Password:"),
                   "nombre": input("Nombre completo:"),
                   "email": input("Email:"),
                   "admin": True,
                   "proveedor": False}
        usu = Usuarios(**usuario)
        db.session.add(usu)
        db.session.commit()
        return


def crear_cat_todas():
    try:
        categoria = db.session.query(Categorias).get(1)
        return
    except:
        categoria = Categorias("Todas")
        db.session.add(categoria)
        db.session.commit()
        return


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    crear_admin()
    crear_cat_todas()
    app.run(debug=True)
