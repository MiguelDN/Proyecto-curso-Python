from flask import Blueprint, render_template, request, url_for, abort
from flask_login import login_required
from werkzeug.utils import redirect

from forms import FormCategoria, FormSINO

import db

catego = Blueprint("catego", __name__, static_folder="static", template_folder="templates")


@catego.route('/categorias')
@login_required
def categorias():
    from models import Categorias
    categorias = db.session.query(Categorias).order_by(Categorias.nombre).all()
    return render_template("categorias.html", categorias=categorias)


@catego.route('/nueva_categoria', methods=["get", "post"])
@login_required
def nueva_categoria():
    from models import Categorias
    # Control de permisos
    form = FormCategoria(request.form)
    if form.validate_on_submit():
        cat = Categorias(nombre=form.nombre.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for("catego.categorias"))
    else:
        return render_template("nueva_categoria.html", form=form)


@catego.route('/categorias/<id>/edit', methods=["get", "post"])
@login_required
def categorias_edit(id):
    from models import Categorias
    # Control de permisos
    cat = db.session.query(Categorias).get(id)
    if cat is None:
        abort(404)
    form = FormCategoria(request.form, obj=cat)
    if form.validate_on_submit():
        form.populate_obj(cat)
        db.session.commit()
        return redirect(url_for("catego.categorias"))
    return render_template("nueva_categoria.html", form=form)


@catego.route('/categorias/<id>/delete', methods=["get", "post"])
@login_required
def categorias_delete(id):
    from models import Categorias
    # Control de permisos
    cat = db.session.query(Categorias).get(id)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            db.session.delete(cat)
            db.session.commit()
        return redirect(url_for("catego.categorias"))
    return render_template("categorias_delete.html", form=form, cat=cat)