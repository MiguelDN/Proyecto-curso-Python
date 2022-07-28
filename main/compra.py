from flask import Blueprint, request, make_response, redirect, render_template, url_for
from flask_login import login_required, current_user
from forms import FormCarrito
from models import Inventario, Ventas, Proveedores

import db
import json

compra = Blueprint("compra", __name__, static_folder="static", template_folder="templates")

inventario = db.session.query(Inventario)


@compra.route('/carrito/add/<id>', methods=["get", "post"])
@login_required
def carrito_add(id):
    art = db.session.query(Inventario).get(id)
    form = FormCarrito()
    form.id.data = id
    if form.validate_on_submit():
        if art.stock >= int(form.cantidad.data):
            try:
                datos = json.loads(request.cookies.get(str(current_user.id)))
            except:
                datos = []
            actualizar = False
            for dato in datos:
                if dato["id"] == id:
                    dato["cantidad"] = form.cantidad.data
                    actualizar = True
            if not actualizar:
                datos.append({"id": form.id.data,
                              "cantidad": form.cantidad.data})
            resp = make_response(redirect('/index'))
            resp.set_cookie(str(current_user.id), json.dumps(datos))
            return resp
        form.cantidad.errors.append("No hay artículos suficientes.")
    return render_template("carrito_add.html", form=form, art=art)


@compra.route('/carrito')
@login_required
def carrito():
    try:
        datos = json.loads(request.cookies.get(str(current_user.id)))
    except:
        datos = []
    articulos = []
    cantidades = []
    total = 0
    for articulo in datos:
        articulos.append(db.session.query(Inventario).get(articulo["id"]))
        cantidades.append(articulo["cantidad"])
        total = round(total + db.session.query(Inventario).get(articulo["id"]).precio_final() *
                      articulo["cantidad"], 2)
    articulos = zip(articulos, cantidades)
    return render_template("carrito.html", articulos=articulos, total=total)


@compra.route('/carrito_delete/<id>')
@login_required
def carrito_delete(id):
    try:
        datos = json.loads(request.cookies.get(str(current_user.id)))
    except:
        datos = []
    new_datos = []
    for dato in datos:
        if dato["id"] != id:
            new_datos.append(dato)
    resp = make_response(redirect(url_for('compra.carrito')))
    resp.set_cookie(str(current_user.id), json.dumps(new_datos))
    return resp


@compra.route('/pedido')
@login_required
def pedido():
    try:
        datos = json.loads(request.cookies.get(str(current_user.id)))
    except:
        datos = []
    total = 0
    articulos = []
    cantidades = []
    for articulo in datos:
        total = total + db.session.query(Inventario).get(articulo["id"]).precio_final() * \
                articulo["cantidad"]
        db.session.query(Inventario).get(articulo["id"]).stock -= articulo["cantidad"]
        articulos.append(db.session.query(Inventario).get(articulo["id"]))
        cantidades.append(articulo["cantidad"])
        db.session.commit()
    articulos = zip(articulos, cantidades)
    for art in articulos:
        idProducto = art[0].id
        cantidad = art[1]
        idUsuario = current_user.id
        idProveedor = art[0].proveedor.id
        venta = Ventas(idProducto=idProducto, cantidad=cantidad, idUsuario=idUsuario, idProveedor=idProveedor)
        db.session.add(venta)
        db.session.commit()
    resp = make_response(render_template("pedido.html", total=total))
    resp.set_cookie(str(current_user.id), "", expires=0)
    return resp


@compra.route("/historial", methods=["get", "post"])
@login_required
def historial():
    compras = db.session.query(Ventas).filter_by(idUsuario=current_user.id).all()
    proveedor = db.session.query(Proveedores)
    lista = []
    for c in compras:
        diccionario = {
            "id": c.id,
            "producto": inventario.filter_by(id=c.idProducto).first().nombre,
            "proveedor": proveedor.filter_by(id=c.idProveedor).first().nombre,
            "cantidad": c.cantidad,
            "total": get_total_compra(c.idProducto, c.cantidad)
        }
        lista.append(diccionario)
    return render_template("historial.html", lista=lista)


def get_total_compra(id_producto, cantidad):
    return round(inventario.filter_by(id=id_producto).first().precio_final() * cantidad, 2)
