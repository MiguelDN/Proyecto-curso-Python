from flask import Blueprint, render_template
import matplotlib.pyplot as plt
from flask_login import login_required

import db
from models import Inventario, Proveedores, Ventas, Usuarios

graphics = Blueprint("graphics", __name__, static_folder="static", template_folder="templates")


@graphics.route("/graficas", methods=["get", "post"])
def graficas():
    return render_template("graficas.html")


@graphics.route("/grafica_ventas_totales", methods=["get", "post"])
@login_required
def grafica_ventas_totales():
    plt.switch_backend('agg')
    from models import Ventas
    ventas = db.session.query(Ventas)
    proveedores = []
    valores = []
    for v in ventas:
        producto = db.session.query(Inventario).filter_by(id=v.idProducto).first()
        proveedor = db.session.query(Proveedores).filter_by(id=v.idProveedor).first()
        if proveedor.nombre not in proveedores:
            proveedores.append(proveedor.nombre)
        else:
            pass
        i = proveedores.index(proveedor.nombre)
        try:
            valores[i] += (producto.precio * v.cantidad)
        except:
            valores.append(producto.precio * v.cantidad)
    plt.pie(x=valores, labels=proveedores, autopct='%1.2f%%')
    plt.title("Porcentaje de ventas")
    plt.savefig("static/upload/graficos/grafica_ventas_totales.png")
    ventas = db.session.query(Ventas)
    ventas_totales = 0
    beneficios_totales = 0
    for v in ventas:
        producto = db.session.query(Inventario).filter_by(id=v.idProducto).first()
        proveedor = db.session.query(Proveedores).filter_by(id=v.idProveedor).first()
        compra = producto.precio * v.cantidad
        ventas_totales += compra
        beneficio = producto.precio * v.cantidad * (proveedor.descuento / 100)
        beneficios_totales += beneficio
    beneficios_totales = round(beneficios_totales, 2)
    ventas_totales = round(ventas_totales, 2)
    porcentaje = round(beneficios_totales * 100 / ventas_totales, 2)
    descuentos_proveedores = db.session.query(Proveedores).all()
    return render_template("grafica_ventas_totales.html", ventas_totales=ventas_totales,
                           beneficios_totales=beneficios_totales,
                           porcentaje=porcentaje, proveedores=proveedores, valores=valores,
                           descuentos_proveedores=descuentos_proveedores)


@graphics.route("/grafica_por_proveedor", methods=["get", "post"])
@graphics.route("/grafica_por_proveedor/<id>", methods=["get", "post"])
@login_required
def grafica_por_proveedor(id=0):
    plt.switch_backend('agg')
    proveedores = db.session.query(Proveedores).all()
    proveedor= db.session.query(Proveedores).get(id)
    ventas = db.session.query(Ventas).filter_by(idProveedor=id)
    if id == 0:
        seleccion = 0
        return render_template("grafica_por_proveedor.html", proveedores=proveedores, seleccion=seleccion,
                               proveedor=proveedor)
    else:
        seleccion = 1
        ventas_totales = 0
        beneficios_totales = 0
        productos = []
        valores = []
        for v in ventas:
            producto = db.session.query(Inventario).filter_by(id=v.idProducto).first()
            proveedor = db.session.query(Proveedores).filter_by(id=v.idProveedor).first()
            if producto.nombre not in productos:
                productos.append(producto.nombre)
            else:
                pass
            i = productos.index(producto.nombre)
            try:
                valores[i] += (producto.precio * v.cantidad)
            except:
                valores.append(producto.precio * v.cantidad)
        plt.pie(x=valores, labels=productos, autopct='%1.2f%%')
        plt.title("Porcentaje productos proveedor")
        plt.savefig("static/upload/graficos/grafica_proveedor.png")
        return render_template("grafica_por_proveedor.html", proveedores=proveedores, seleccion=seleccion,
                               proveedor=proveedor, id=id)


@graphics.route("/grafica_cliente", methods=["get", "post"])
@login_required
def grafica_ventas_clientes():
    plt.switch_backend('agg')
    from models import Ventas
    ventas = db.session.query(Ventas)
    clientes = []
    valores = []
    for v in ventas:
        producto = db.session.query(Inventario).filter_by(id=v.idProducto).first()
        proveedor = db.session.query(Proveedores).filter_by(id=v.idProveedor).first()
        if v.idUsuario not in clientes:
            clientes.append(v.idUsuario)
        else:
            pass
        i = clientes.index(v.idUsuario)
        try:
            valores[i] += (producto.precio * v.cantidad)
        except:
            valores.append(producto.precio * v.cantidad)
    plt.pie(x=valores, labels=clientes, autopct='%1.2f%%')
    plt.title("Ventas Clientes")
    plt.savefig("static/upload/graficos/grafica_venta_clientes.png")
    usuario = db.session.query(Usuarios)
    lista = []
    for valor, cliente in sorted(zip(valores, clientes), reverse=True):
        diccionario = {
            'id': cliente,
            'nombre': usuario.filter_by(id=cliente).first().nombre,
            'valor': valor
        }
        lista.append(diccionario)
    return render_template("grafica_cliente.html", lista=lista)
