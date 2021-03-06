from flask import Flask, render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/almacen.db'
db = SQLAlchemy(app)

#Creacion de las tablas de la base de datos 
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
    idUsuario = db.Column(db.Integer,db.ForeignKey("USUARIO.id"))
    nombre = db.Column(db.String(200))
    tlfn = db.Column(db.String(30))
    cif = db.Column(db.String(30))

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
    cantidadMax = db.Column(db.Integer)

class CompraCliente(db.Model):
    __tablename__ = "COMPRACLIENTE"
    id = db.Column(db.Integer,primary_key = True)
    idProducto = db.Column(db.Integer,db.ForeignKey("PRODUCTO.id"))
    idCliente = db.Column(db.Integer,db.ForeignKey("USUARIO.id"))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Integer)
    fecha = db.Column(db.Date)

class CompraProveedor(db.Model):
    __tablename__ = "COMPRAPROVEEDOR"
    id = db.Column(db.Integer,primary_key = True)
    idProducto = db.Column(db.Integer,db.ForeignKey("PRODUCTO.id"))
    idProveedor = db.Column(db.Integer,db.ForeignKey("PROVEEDOR.id"))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Integer)
    fecha = db.Column(db.Date)



#Ejecuta la cracion de datos en la base de datos 
db.create_all()
db.session.commit()


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/exit",methods=["Post"])
def exit():
    return render_template('index.html')

@app.route("/back/<id>",methods=['Post'])
def back(id):
    cliente = db.session.query(Usuario).filter_by(id=id).first()

    todosProductos = Producto.query.all()
    usuarios = Usuario.query.all()
    proveedores = Proveedor.query.all()
    return render_template("admin.html",listProveedores=proveedores,listUsuarios=usuarios, productos=todosProductos, usuario=cliente)
    
@app.route("/verProducto/<id>/<user>")
def verProducto(id,user):
    pro = db.session.query(Producto).filter_by(id=int(id)).first()
    cliente = db.session.query(Usuario).filter_by(id=user).first()

    return render_template("verProducto.html",produ=pro,usuario=cliente)

@app.route("/login",methods=['Post'])
#Funcion para logearte
def login():
    try:
        usuario = request.form["loginUsuario"]
        passw = request.form["loginPassword"]
        cliente = db.session.query(Usuario).filter_by(user=usuario).first()
        if (cliente.rol == 1 ) and cliente.password == passw:
            todosProductos = Producto.query.all()
            usuarios = Usuario.query.all()
            proveedores = Proveedor.query.all()
            return render_template("admin.html",listProveedores=proveedores,listUsuarios=usuarios, productos=todosProductos, usuario=cliente)
        elif(cliente.rol == 2) and cliente.password == passw:
            id = int(cliente.id)
            compras = db.session.query(CompraCliente).filter_by(idCliente=id).order_by(CompraCliente.fecha.desc()).all()            
            suma = db.session.query(CompraCliente,func.sum(CompraCliente.precio)).filter_by(idCliente=id).all()
            precioTotal = suma[0][1]
            if(precioTotal==None):
                precioTotal=0
            todosProductos = Producto.query.all()
            return render_template("cliente.html", productos=todosProductos, usuario=cliente,listacompras=compras,precio=precioTotal)
        elif(cliente.rol == 3) and cliente.password == passw:
            prove = db.session.query(Proveedor).filter_by(idUsuario=cliente.id).first()
            compras = db.session.query(CompraProveedor).filter_by(idProveedor=prove.id).order_by(CompraProveedor.fecha.desc()).all()            
            suma = db.session.query(CompraProveedor,func.sum(CompraProveedor.precio)).filter_by(idProveedor=prove.id).all()
            cant = db.session.query(CompraProveedor,func.sum(CompraProveedor.cantidad)).filter_by(idProveedor=prove.id).all()
            cantidad = cant[0][1]
            precioTotal = suma[0][1]
            if(precioTotal == None):
                precioTotal = 0
            if(cantidad == None):
                cantidad = 0
            todosProductos = db.session.query(Producto).filter_by(proveedor=prove.id)
            return render_template("proveedor.html", productos=todosProductos, usuario=cliente,provee=prove,listacompras=compras,precio=precioTotal,cantidad=cantidad)
        else:
            return redirect(url_for('home'))

    except AttributeError as e:
        print("error en los datos")
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
