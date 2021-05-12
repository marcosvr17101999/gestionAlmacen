# gestionAlmacen
Proyecto Final
Proyecto Final del curso de Programacion Python en el cual se trabajara con Flask y SQLAlchemy
La aplicacion consiste en crear una aplicacion web que ayude a una empresa de suministros informaticos.
La aplicacion servira como base de datos y como gestion de datos de la empresa como para los proveedores.

Requerimientos:
    Inventario de todos los productos y cantidades del almacen, de tal forma que cuando el stock este al 90% nos avise(zona ADMIN)
    Tres tipos de acceso para los clientes, los proveedores y el admin
    Cliente vera todos los productos y una grafica de gastos datos puestos en la base de datos a mano debido a que no esta implementado la opcion de compras en la app
    Proveedor vera todos los productos suyos y una grafica de cuantos productos se han vendido a la empresa
    Admin vera todos los clientes,proveedores y productos donde avise el stock que haya
    
    Aniadir paginas cuando todas las funcionalidades esten de ver detalles del producto y detalles de clientes



    (COSAS QUE TENGO QUE MODIFICAR EN LA BASE DE DATOS)
    ANIADIR TABLA DE COMPRAS DE CLIENTES Y COMPRAS DE PRODUCTOS
    TABLAS ACTUALES:
        ROL-->id,rol 
        USUARIO-->id,user,password,rol 
        Proveedor-->id,id_usario,nombre,tlfn,cif
        Producto-->id,producto,color,cantidad,descripcion,precio,lugar,proveedor,cantidadmax
        comprasClientes-->id,idproducto,idcliente,cantidad,precio,fecha
        comprasProveedor-->id,idproducto,idproveedor,cantidad,precio,fecha



CODIGO QUE USARE 
  <th
                                class="{% if (producto.cantidad/producto.cantidadmax < 0.90) %} stock {% else %} stock2 {% endif %}">
                                {{producto.id}}</th>