from flask import Flask, render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/almacen.db'
db = SQLAlchemy(app)

class Rol(db.Model):
    __tablename__ = "ROL"
    id = db.Column(db.Integer,primary_key = True)
    rol = db.Column(db.String(200),unique = True)

class Usuario(db.Model):
    __tablename__ = "USUARIO"
    id = db.Column(db.Integer,primary_key = True)
    user = db.Column(db.String(200))
    password = db.Column(db.String(100))
    rol = db.Column(db.Integer,db.ForeignKey("ROL.id"))

class Proveedor(db.Model):
    __tablename__ = "PROVEEDOR"
    id = db.Column(db.Integer,primary_key = True)
    id_usario = db.Column(db.Integer,db.ForeignKey("USUARIO.id"))
    nombre = db.Column(db.String(200))
    tlfn = db.Column(db.String(30))
    cif = db.Column(db.String(30))
    facturacion = db.Column(db.Integer)

class Producto(db.Model):
    __tablename__ = "PRODUCTO"
    id = db.Column(db.Integer,primary_key = True)
    producto = db.Column(db.String(200))
    color = db.Column(db.String(200))
    cantidad = db.Column(db.Integer)
    descripcion = db.Column(db.String(300))
    precio = db.Column(db.Integer)
    lugar = db.Column(db.String(200))
    proveedor = db.Column(db.Integer,db.ForeignKey("PROVEEDOR.id"))





db.create_all()
db.session.commit()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=['Post'])
def login():

    try:
        usuario = request.form["loginUsuario"]
        passw = request.form["loginPassword"]
        print(usuario,passw)
        cliente = db.session.query(Usuario).filter_by(user=usuario).first()
        print(cliente.rol)
        if cliente.rol == 1:
           return render_template("admin.html",usu = cliente)
        if cliente.rol == 2:
           return render_template("cliente.html",usu = cliente)
        if cliente.rol == 3:
           return render_template("proveedor.html",usu = cliente)

    except AttributeError as e:
        print("error en los datos")
        return redirect(url_for('home'))
    except Exception as e:
        print(type(e))
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
