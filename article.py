from flask import Blueprint, redirect, render_template, abort, url_for, request
from flask_login import login_required
from werkzeug.utils import secure_filename

import db
from forms import FormArticulo, FormSINO
from models import Inventario, Categorias, Proveedores

article = Blueprint("article", __name__, static_folder="static", template_folder="templates")


@article.route('/articulos_nuevos/<id>', methods=["get", "post"])
@login_required
def articulos_nuevos(id):
    from models import Inventario, Categorias, Proveedores
    # Control de permisos
    form = FormArticulo()
    categorias = [(c.id, c.nombre) for c in db.session.query(Categorias).order_by(Categorias.nombre).all()]
    form.CategoriaId.choices = categorias
    proveedores = [(p.id, p.nombre) for p in db.session.query(Proveedores).filter_by(id=id)]
    form.Proveedorid.choices = proveedores
    if form.validate_on_submit():
        try:
            f = form.image.data
            nombre_fichero = secure_filename(f.filename)
            f.save(article.root_path + "/static/upload/" + nombre_fichero)
        except:
            nombre_fichero = ""
        art = Inventario()
        form.populate_obj(art)
        art.image = nombre_fichero
        db.session.add(art)
        db.session.commit()
        return redirect("/proveedores")
    else:
        return render_template("articulos_nuevos.html", form=form)


@article.route('/articulos/<id>/delete', methods=["get", "post"])
@login_required
def articulos_delete(id):
    from models import Inventario
    # Control de permisos
    art = db.session.query(Inventario).get(id)
    if art is None:
        abort(404)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            art.activo = False
            db.session.commit()
        return redirect(url_for('providers.proveedores_productos', id=art.Proveedorid))
    return render_template("articulos_delete.html", form=form, art=art)


@article.route('/articulos/<id>/activar', methods=["get", "post"])
@login_required
def articulos_activar(id):
    from models import Inventario
    # Control de permisos
    art = db.session.query(Inventario).get(id)
    if art is None:
        abort(404)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            art.activo = True
            db.session.commit()
        return redirect(url_for('providers.proveedores_productos', id=art.Proveedorid))
    return render_template("articulos_delete.html", form=form, art=art)


@article.route('/articulos/<id>/edit', methods=["GET", "POST"])
@login_required
def articulos_edit(id):
    # Control de permisos
    art = db.session.query(Inventario).get(id)
    if art is None:
        abort(404)
    form = FormArticulo(obj=art)
    categorias = [(c.id, c.nombre) for c in db.session.query(Categorias).order_by(Categorias.nombre).all()[0:]]
    form.CategoriaId.choices = categorias
    proveedores = [(p.id, p.nombre) for p in db.session.query(Proveedores).order_by(Proveedores.nombre).all()[0:]]
    form.Proveedorid.choices = proveedores
    print("nombre imagen antes primer if", form.image.data)
    if form.validate_on_submit():
        print("primer if")
        # Borramos la imagen anterior si hemos subido una nueva
        if form.image.data:
            print("segundo if")

            try:
                print("try")
                f = form.image.data
                print("f en try", f.filename)
                nombre_fichero = secure_filename(f.filename)
                print("primer nombre del fichero try", nombre_fichero)
                f.save(article.root_path + "/static/upload/" + nombre_fichero)
                print("nombre del fichero try", nombre_fichero)
            except:
                print("except")
                nombre_fichero = ""
                print("nombre del fichero except", nombre_fichero)
        else:
            print("else")
            nombre_fichero = art.image
        form.populate_obj(art)
        art.image = nombre_fichero
        db.session.commit()
        print("nombre del ficher final", nombre_fichero)
        return redirect(url_for('providers.proveedores_productos', id=art.Proveedorid))
    return render_template("articulos_nuevos.html", form=form)

