from flask import session
from main import app


def login_user(Usuario):
    session["id"] = Usuario.id
    session["username"] = Usuario.username
    session["admin"] = Usuario.admin
    session["proveedor"] = Usuario.proveedor
    session["usuProveedorId"] = Usuario.usuProveedorId


def logout_user():
    session.pop("id", None)
    session.pop("username", None)
    session.pop("admin", None)
    session.pop("proveedor", None)


def is_login():
    if "id" in session:
        return True
    else:
        return False


def is_admin():
    return session.get("admin", False)


def is_proveedor():
    return session.get("proveedor", True)


@app.context_processor
def login():
    if "id" in session:
        return {'is_login': True}
    else:
        return {'is_login': False}


@app.context_processor
def admin():
    return {'is_admin': session.get("admin", False)}


@app.context_processor
def proveedor():
    return {'is_proveedor': session.get("proveedor", False)}
