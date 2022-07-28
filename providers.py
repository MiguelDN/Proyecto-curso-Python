from flask import Blueprint, render_template, redirect, abort, request, url_for
from flask_login import login_required

import db
from forms import FormProveedor, FormSINO
from models import Proveedores, Inventario

providers = Blueprint("providers", __name__, static_folder="static", template_folder="templates")


@providers.route('/proveedores')
@login_required
def proveedores():
    from models import Proveedores
    proveedores = db.session.query(Proveedores).order_by(Proveedores.nombre).all()
    return render_template("proveedores.html", proveedores=proveedores)


@providers.route('/proveedor_nuevo', methods=["get", "post"])
@login_required
def proveedor_nuevo():
    from models import Inventario, Categorias, Proveedores
    # Control de permisos
    form = FormProveedor()
    proveedores = [(c.id, c.nombre) for c in db.session.query(Proveedores).all()]
    if form.validate_on_submit():
        pro = Proveedores(nombre=form.nombre.data, cif=form.cif.data, descuento=form.descuento.data,
                          direccion=form.direccion.data, telefono=form.telefono.data)
        form.populate_obj(pro)
        db.session.add(pro)
        db.session.commit()
        return redirect("/proveedores")
    else:
        return render_template("proveedor_nuevo.html", form=form)


@providers.route("/proveedores_productos/<id>")
@login_required
def proveedores_productos(id):
    from models import Inventario, Categorias, Proveedores
    proveedores = db.session.query(Proveedores).order_by(Proveedores.nombre).all()
    articulos = db.session.query(Inventario).filter_by(Proveedorid=id).all()
    return render_template("proveedores_productos.html", articulos=articulos)


@providers.route('/proveedores/<id>/edit', methods=["get", "post"])
@login_required
def proveedores_edit(id):
    # Control de permisos
    pro = db.session.query(Proveedores).get(id)
    if pro is None:
        abort(404)
    form = FormProveedor(request.form, obj=pro)
    if form.validate_on_submit():
        form.populate_obj(pro)
        db.session.commit()
        return redirect(url_for("proveedores"))
    return render_template("proveedor_nuevo.html", form=form)


@providers.route('/proveedores/<id>/delete', methods=["get", "post"])
@login_required
def proveedores_delete(id):
    # Control de permisos
    pro = db.session.query(Proveedores).get(id)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            pro.activo = False
            db.session.commit()
        return redirect(url_for("providers.proveedores"))
    return render_template("proveedores_delete.html", form=form, pro=pro)


@providers.route('/proveedores/<id>/activar', methods=["get", "post"])
@login_required
def proveedores_activar(id):
    # Control de permisos
    pro = db.session.query(Proveedores).get(id)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            pro.activo = True
            db.session.commit()
        return redirect(url_for("providers.proveedores"))
    return render_template("proveedores_delete.html", form=form, pro=pro)


@providers.route('/alarmas_stock')
@login_required
def alarmas_stock():
    alarmas_stock = []
    stock = db.session.query(Inventario).all()
    for alrm in stock:
        if alrm.stock < 20:
            alarmas_stock.append(alrm)

    return render_template("alarmas_stock.html", alarmas_stock=alarmas_stock)


@providers.route('/datos_proveedor/<id>')
@login_required
def datos_proveedor(id):
    proveedor = db.session.query(Proveedores).get(id)
    return render_template('datos_proveedor.html', proveedor=proveedor)

