from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, TextAreaField, SelectField, FloatField, \
    PasswordField, EmailField, HiddenField
from flask_wtf.file import FileField
from wtforms.validators import data_required, NumberRange


class FormCategoria(FlaskForm):
    nombre = StringField("Nombre:",
                         validators=[data_required("Tienes que introducir el dato")]
                         )
    submit = SubmitField('Enviar')


class FormArticulo(FlaskForm):
    nombre = StringField("Nombre:",
                         validators=[data_required("Tienes que introducir el dato")]
                         )
    descripcion = TextAreaField("Descripción:")
    CategoriaId = SelectField("Categoría:", coerce=int)
    Proveedorid = SelectField("Proveedor:", coerce=int)
    stock = IntegerField("Stock:", default=1,
                         validators=[data_required("Tienes que introducir el dato")]
                         )
    precio = DecimalField("Precio:", default=0,
                          validators=[data_required("Tienes que introducir el dato")]
                          )
    capacidad_stock = IntegerField("Capacidad Stock:", default=1,
                                   validators=[data_required("Tienes que introducir el dato")]
                                   )
    ubicacion = StringField("Ubicación:",
                            validators=[data_required("Tienes que introducir el dato")]
                            )
    iva = IntegerField("IVA:", default=21,
                       validators=[data_required("Tienes que introducir el dato")])

    image = FileField('Selecciona imagen:')
    submit = SubmitField('Enviar')


class FormSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')


class FormStock(FlaskForm):
    stock = IntegerField("Stock:", default=1,
                         validators=[data_required("Tienes que introducir el dato")]
                         )
    submit = SubmitField('Enviar')


class FormProveedor(FlaskForm):
    nombre = StringField("Nombre:",
                         validators=[data_required("Tienes que introducir el dato")]
                         )
    cif = StringField("CIF:",
                      validators=[data_required("Tienes que introducir el dato")]
                      )
    descuento = FloatField("Descuento:", default=1,
                           validators=[data_required("Tienes que introducir el dato")]
                           )
    direccion = StringField("Dirección:", default=0,
                            validators=[data_required("Tienes que introducir el dato")]
                            )
    telefono = StringField("Teléfono:",
                           validators=[data_required("Tienes que introducir el dato")]
                           )
    submit = SubmitField('Enviar')


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[data_required()])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Entrar')


class FormUsuario(FlaskForm):
    username = StringField('Usuario', validators=[data_required()])
    password = PasswordField('Password', validators=[data_required()])
    nombre = StringField('Nombre completo')
    email = EmailField('Email')
    submit = SubmitField('Aceptar')


class FormUsuarioProveedor(FlaskForm):
    username = StringField('Usuario', validators=[data_required()])
    password = PasswordField('Password', validators=[data_required()])
    nombre = StringField('Nombre completo')
    email = EmailField('Email')
    usuProveedorId = SelectField("Proveedor ID:", coerce=int)
    submit = SubmitField('Aceptar')


class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Aceptar')


class FormCarrito(FlaskForm):
    id = HiddenField()
    cantidad = IntegerField('Cantidad', default=1,
                            validators=[NumberRange(min=1,
                                                    message="Debe ser un númer"
                                                            "o positivo"),
                                        data_required("Tienes que introducir el "
                                                      "dato")])
    submit = SubmitField('Aceptar')

