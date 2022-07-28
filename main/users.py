from flask import Blueprint, redirect, render_template, abort, request
from flask_login import login_user, logout_user, login_required
import db
from forms import LoginForm, FormUsuario, FormUsuarioProveedor, FormChangePassword, FormSINO
from models import Usuarios, Proveedores

users = Blueprint("users", __name__, static_folder="static", template_folder="templates")


@users.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(Usuarios).filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data) and user.activo == True:
            login_user(user)
            return redirect('/index')
        form.username.errors.append("Usuario o contraseña incorrectas.")
    return render_template('login.html', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('index')


@users.route("/registro", methods=["get", "post"])
def registro():
    form = FormUsuario()
    if form.validate_on_submit():
        existe_usuario = db.session.query(Usuarios).filter_by(username=form.username.data).first()
        if existe_usuario is None:
            user = Usuarios()
            form.populate_obj(user)
            user.admin = False
            db.session.add(user)
            db.session.commit()
            return redirect("/index")
        form.username.errors.append("Nombre de usuario ya existe.")
    return render_template("usuarios_new.html", form=form)


@users.route("/registro_proveedor", methods=["get", "post"])
@login_required
def registro_proveedor():
    form = FormUsuarioProveedor()
    proveedores = [(c.id, c.nombre) for c in db.session.query(Proveedores).order_by(Proveedores.nombre).all()]
    form.usuProveedorId.choices = proveedores
    if form.validate_on_submit():
        existe_usuario = db.session.query(Usuarios).filter_by(username=form.username.data).first()
        if existe_usuario is None:
            user = Usuarios()
            form.populate_obj(user)
            user.admin = False
            user.proveedor = True
            db.session.add(user)
            db.session.commit()
            return redirect("/index")
        form.username.errors.append("Nombre de usuario ya existe.")
    return render_template("usuario_proveedor_new.html", form=form)


@users.route('/perfil/<username>', methods=["get", "post"])
@login_required
def perfil(username):
    user = db.session.query(Usuarios).filter_by(username=username).first()
    if user is None:
        abort(404)
    form = FormUsuario(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect("/index")
    return render_template("usuarios_new.html", form=form, perfil=True)


@users.route('/changepassword/<username>', methods=["get", "post"])
@login_required
def changepassword(username):
    user = db.session.query(Usuarios).filter_by(username=username).first()
    if user is None:
        abort(404)
    form = FormChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect("/index")
    return render_template("changepassword.html", form=form)


@users.route('/gestion_usuarios', methods=["get", "post"])
@users.route('/gestion_usuarios/<seleccion>', methods=["get", "post"])
@users.route('/gestion_usuarios/<seleccion>/<id>', methods=["get", "post"])
@login_required
def gestion_usuarios(seleccion=0, id=0):
    usuarios = db.session.query(Usuarios).filter_by(proveedor="0")
    proveedores = db.session.query(Usuarios).filter_by(proveedor="1")
    usuario = db.session.query(Usuarios).filter_by(id=id)
    return render_template("usuarios_gestion.html", seleccion=seleccion, usuarios=usuarios, proveedores=proveedores,
                           usuario=usuario, id=id)


@users.route('/usuarios/<id>/delete', methods=["get", "post"])
@login_required
def usuarios_delete(id):
    from models import Usuarios
    # Control de permisos
    usu = db.session.query(Usuarios).get(id)
    if usu is None:
        abort(404)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            usu.activo = False
            db.session.commit()
        return redirect("/gestion_usuarios")
    return render_template("Usuarios_delete.html", form=form, usu=usu)


@users.route('/usuarios/<id>/activar', methods=["get", "post"])
@login_required
def usuarios_activar(id):
    from models import Usuarios
    # Control de permisos
    usu = db.session.query(Usuarios).get(id)
    if usu is None:
        abort(404)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            usu.activo = True
            db.session.commit()
        return redirect("/gestion_usuarios")
    return render_template("Usuarios_delete.html", form=form, usu=usu)


