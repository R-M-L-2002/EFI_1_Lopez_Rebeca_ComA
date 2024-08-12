from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tiendaCelulares'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'efi1'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from modelos import Marca,Fabricante,Modelo,Categoria,Caracteristica,Stock, Proveedor,Accesorio,Equipo,Inventario,Cliente,Venta

@app.route('/')
def index():
    return render_template('index.html')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/marcas')
def listar_marcas():
    marcas = Marca.query.all()
    return render_template('marcas.html', marcas=marcas)

@app.route('/marcas/crear', methods=['GET', 'POST'])
def crear_marca():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            if not nombre:
                flash('El nombre es requerido', 'error')
            else:
                nueva_marca = Marca(nombre=nombre)
                db.session.add(nueva_marca)
                db.session.commit()
                flash('Marca creada con éxito', 'success')
                return redirect(url_for('marcas'))
        except Exception as e:
            db.session.rollback()  
            flash(f'Error al crear la marca: {e}', 'error')
    return render_template('crear_marca.html')

@app.route('/marcas/editar/<int:id>', methods=['GET', 'POST'])
def editar_marca(id):
    marca = Marca.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if nombre:
            marca.nombre = nombre
            db.session.commit()
            flash('Marca actualizada con éxito', 'success')
            return redirect(url_for('marcas'))
        flash('El nombre es requerido', 'error')
    return render_template('editar_marca.html', marca=marca)

@app.route('/marcas/eliminar/<int:id>', methods=['POST'])
def eliminar_marca(id):
    marca = Marca.query.get_or_404(id)
    db.session.delete(marca)
    db.session.commit()
    flash('Marca eliminada con éxito', 'success')
    return redirect(url_for('marcas'))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/fabricantes')
def listar_fabricantes():
    fabricantes = Fabricante.query.all()
    return render_template('listar_fabricantes.html', fabricantes=fabricantes)

@app.route('/fabricante/crear', methods=['GET', 'POST'])
def crear_fabricante():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        pais_origen = request.form.get('pais_origen')
        if not nombre or not pais_origen:
            flash('Todos los campos son requeridos', 'error')
        else:
            nuevo_fabricante = Fabricante(
                nombre=nombre,
                pais_origen=pais_origen
            )
            db.session.add(nuevo_fabricante)
            db.session.commit()
            flash('Fabricante creado con éxito', 'success')
            return redirect(url_for('listar_fabricantes'))
    return render_template('crear_fabricante.html')

@app.route('/fabricante/editar/<int:id>', methods=['GET', 'POST'])
def editar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        pais_origen = request.form.get('pais_origen')
        if not nombre or not pais_origen:
            flash('Todos los campos son requeridos', 'error')
        else:
            fabricante.nombre = nombre
            fabricante.pais_origen = pais_origen
            db.session.commit()
            flash('Fabricante actualizado con éxito', 'success')
            return redirect(url_for('listar_fabricantes'))
    return render_template('editar_fabricante.html', fabricante=fabricante)

@app.route('/fabricante/eliminar/<int:id>', methods=['POST'])
def eliminar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    db.session.delete(fabricante)
    db.session.commit()
    flash('Fabricante eliminado con éxito', 'success')
    return redirect(url_for('listar_fabricantes'))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/modelos')
def listar_modelos():
    modelos = Modelo.query.all()
    return render_template('listar_modelos.html', modelos=modelos)

@app.route('/modelo/crear', methods=['GET', 'POST'])
def crear_modelo():
    fabricantes = Fabricante.query.all() 
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fabricante_id = request.form.get('fabricante_id')
        if not nombre or not fabricante_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            nuevo_modelo = Modelo(
                nombre=nombre,
                fabricante_id=fabricante_id
            )
            db.session.add(nuevo_modelo)
            db.session.commit()
            flash('Modelo creado con éxito', 'success')
            return redirect(url_for('listar_modelos'))
    return render_template('crear_modelo.html', fabricantes=fabricantes)

@app.route('/modelo/editar/<int:id>', methods=['GET', 'POST'])
def editar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    fabricantes = Fabricante.query.all()  # Obtener la lista de fabricantes
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fabricante_id = request.form.get('fabricante_id')
        if not nombre or not fabricante_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            modelo.nombre = nombre
            modelo.fabricante_id = fabricante_id
            db.session.commit()
            flash('Modelo actualizado con éxito', 'success')
            return redirect(url_for('listar_modelos'))
    return render_template('editar_modelo.html', modelo=modelo, fabricantes=fabricantes)

@app.route('/modelo/eliminar/<int:id>', methods=['POST'])
def eliminar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    db.session.delete(modelo)
    db.session.commit()
    flash('Modelo eliminado con éxito', 'success')
    return redirect(url_for('listar_modelos'))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------    
@app.route('/categorias')
def categorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

@app.route('/categoria/nueva', methods=['GET', 'POST'])
def nueva_categoria():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es requerido', 'error')
        else:
            categoria = Categoria(nombre=nombre)
            db.session.add(categoria)
            db.session.commit()
            flash('Categoría creada con éxito', 'success')
            return redirect(url_for('categorias'))
    return render_template('categoria_form.html')

@app.route('/categoria/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es requerido', 'error')
        else:
            categoria.nombre = nombre
            db.session.commit()
            flash('Categoría actualizada con éxito', 'success')
            return redirect(url_for('categorias'))
    return render_template('categoria_form.html', categoria=categoria)

@app.route('/categoria/borrar/<int:id>', methods=['POST'])
def borrar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada con éxito', 'success')
    return redirect(url_for('categorias'))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/caracteristicas')
def caracteristicas():
    caracteristicas = Caracteristica.query.all()
    return render_template('caracteristicas.html', caracteristicas=caracteristicas)

@app.route('/caracteristica/nueva', methods=['GET', 'POST'])
def nueva_caracteristica():
    modelos = Modelo.query.all()
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion')
        modelo_id = request.form.get('modelo_id')
        if not tipo or not descripcion or not modelo_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            caracteristica = Caracteristica(
                tipo=tipo,
                descripcion=descripcion,
                modelo_id=modelo_id
            )
            db.session.add(caracteristica)
            db.session.commit()
            flash('Característica creada con éxito', 'success')
            return redirect(url_for('caracteristicas'))
    return render_template('caracteristica_form.html', modelos=modelos)

@app.route('/caracteristica/editar/<int:id>', methods=['GET', 'POST'])
def editar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    modelos = Modelo.query.all()
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion')
        modelo_id = request.form.get('modelo_id')
        if not tipo or not descripcion or not modelo_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            caracteristica.tipo = tipo
            caracteristica.descripcion = descripcion
            caracteristica.modelo_id = modelo_id
            db.session.commit()
            flash('Característica actualizada con éxito', 'success')
            return redirect(url_for('caracteristicas'))
    return render_template('caracteristica_form.html', caracteristica=caracteristica, modelos=modelos)

@app.route('/caracteristica/borrar/<int:id>', methods=['POST'])
def borrar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    db.session.delete(caracteristica)
    db.session.commit()
    flash('Característica eliminada con éxito', 'success')
    return redirect(url_for('caracteristicas'))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/stocks')
def stocks():
    stocks = Stock.query.all()
    return render_template('stocks.html', stocks=stocks)

@app.route('/stock/nuevo', methods=['GET', 'POST'])
def nuevo_stock():
    equipos = Equipo.query.all()
    if request.method == 'POST':
        cantidad = request.form.get('cantidad')
        ubicacion = request.form.get('ubicacion')
        equipo_id = request.form.get('equipo_id')
        if not cantidad or not ubicacion or not equipo_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            stock = Stock(
                cantidad=cantidad,
                ubicacion=ubicacion,
                equipo_id=equipo_id
            )
            db.session.add(stock)
            db.session.commit()
            flash('Stock creado con éxito', 'success')
            return redirect(url_for('stocks'))
    return render_template('stock_form.html', equipos=equipos)

@app.route('/stock/editar/<int:id>', methods=['GET', 'POST'])
def editar_stock(id):
    stock = Stock.query.get_or_404(id)
    equipos = Equipo.query.all()
    if request.method == 'POST':
        cantidad = request.form.get('cantidad')
        ubicacion = request.form.get('ubicacion')
        equipo_id = request.form.get('equipo_id')
        if not cantidad or not ubicacion or not equipo_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            stock.cantidad = cantidad
            stock.ubicacion = ubicacion
            stock.equipo_id = equipo_id
            db.session.commit()
            flash('Stock actualizado con éxito', 'success')
            return redirect(url_for('stocks'))
    return render_template('stock_form.html', stock=stock, equipos=equipos)

@app.route('/stock/borrar/<int:id>', methods=['POST'])
def borrar_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    flash('Stock eliminado con éxito', 'success')
    return redirect(url_for('stocks'))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/proveedores')
def proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/proveedor/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        contacto = request.form.get('contacto')
        if not nombre or not contacto:
            flash('Todos los campos son requeridos', 'error')
        else:
            proveedor = Proveedor(
                nombre=nombre,
                contacto=contacto
            )
            db.session.add(proveedor)
            db.session.commit()
            flash('Proveedor creado con éxito', 'success')
            return redirect(url_for('proveedores'))
    return render_template('proveedor_form.html')

@app.route('/proveedor/editar/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        contacto = request.form.get('contacto')
        if not nombre or not contacto:
            flash('Todos los campos son requeridos', 'error')
        else:
            proveedor.nombre = nombre
            proveedor.contacto = contacto
            db.session.commit()
            flash('Proveedor actualizado con éxito', 'success')
            return redirect(url_for('proveedores'))
    return render_template('proveedor_form.html', proveedor=proveedor)

@app.route('/proveedor/borrar/<int:id>', methods=['POST'])
def borrar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado con éxito', 'success')
    return redirect(url_for('proveedores'))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/accesorios')
def accesorios():
    accesorios = Accesorio.query.all()
    return render_template('accesorios.html', accesorios=accesorios)

@app.route('/accesorio/nuevo', methods=['GET', 'POST'])
def nuevo_accesorio():
    modelos = Modelo.query.all()  
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        modelo_id = request.form.get('modelo_id')
        if not tipo or not modelo_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            accesorio = Accesorio(tipo=tipo, modelo_id=modelo_id)
            db.session.add(accesorio)
            db.session.commit()
            flash('Accesorio creado con éxito', 'success')
            return redirect(url_for('accesorios'))
    return render_template('accesorio_form.html', modelos=modelos)

@app.route('/accesorio/editar/<int:id>', methods=['GET', 'POST'])
def editar_accesorio(id):
    accesorio = Accesorio.query.get_or_404(id)
    modelos = Modelo.query.all() 
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        modelo_id = request.form.get('modelo_id')
        if not tipo or not modelo_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            accesorio.tipo = tipo
            accesorio.modelo_id = modelo_id
            db.session.commit()
            flash('Accesorio actualizado con éxito', 'success')
            return redirect(url_for('accesorios'))
    return render_template('accesorio_form.html', accesorio=accesorio, modelos=modelos)

@app.route('/accesorio/borrar/<int:id>', methods=['POST'])
def borrar_accesorio(id):
    accesorio = Accesorio.query.get_or_404(id)
    db.session.delete(accesorio)
    db.session.commit()
    return redirect(url_for('accesorios'))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/equipos')
def equipos():
    equipos = Equipo.query.all()
    return render_template('equipos.html', equipos=equipos)

@app.route('/equipo/nuevo', methods=['GET', 'POST'])
def crear_equipo():
    categorias = Categoria.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()
    caracteristicas = Caracteristica.query.all()
    accesorios = Accesorio.query.all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        categoria_id = request.form.get('categoria_id')
        marca_id = request.form.get('marca_id')
        modelo_id = request.form.get('modelo_id')
        caracteristica_id = request.form.get('caracteristica_id')
        accesorio_id = request.form.get('accesorio_id')
        
        if not nombre or not precio or not categoria_id or not marca_id or not modelo_id or not caracteristica_id or not accesorio_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            equipo = Equipo(
                nombre=nombre,
                precio=precio,
                categoria_id=categoria_id,
                marca_id=marca_id,
                modelo_id=modelo_id,
                caracteristica_id=caracteristica_id,
                accesorio_id=accesorio_id
            )
            db.session.add(equipo)
            db.session.commit()
            flash('Equipo creado con éxito', 'success')
            return redirect(url_for('equipos'))
    
    return render_template('equipo_form.html', categorias=categorias, marcas=marcas, modelos=modelos, caracteristicas=caracteristicas, accesorios=accesorios)

@app.route('/equipo/editar/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    categorias = Categoria.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()
    caracteristicas = Caracteristica.query.all()
    accesorios = Accesorio.query.all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        categoria_id = request.form.get('categoria_id')
        marca_id = request.form.get('marca_id')
        modelo_id = request.form.get('modelo_id')
        caracteristica_id = request.form.get('caracteristica_id')
        accesorio_id = request.form.get('accesorio_id')
        
        if not nombre or not precio or not categoria_id or not marca_id or not modelo_id or not caracteristica_id or not accesorio_id:
            flash('Todos los campos son requeridos', 'error')
        else:
            equipo.nombre = nombre
            equipo.precio = precio
            equipo.categoria_id = categoria_id
            equipo.marca_id = marca_id
            equipo.modelo_id = modelo_id
            equipo.caracteristica_id = caracteristica_id
            equipo.accesorio_id = accesorio_id
            db.session.commit()
            flash('Equipo actualizado con éxito', 'success')
            return redirect(url_for('equipos'))
    
    return render_template('equipo_form.html', equipo=equipo, categorias=categorias, marcas=marcas, modelos=modelos, caracteristicas=caracteristicas, accesorios=accesorios)

@app.route('/equipo/borrar/<int:id>', methods=['POST'])
def borrar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash('Equipo eliminado con éxito', 'success')
    return redirect(url_for('equipos'))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/inventarios')
def inventarios():
    inventarios = Inventario.query.all()
    return render_template('inventarios.html', inventarios=inventarios)

@app.route('/inventario/nuevo', methods=['GET', 'POST'])
def nuevo_inventario():
    proveedores = Proveedor.query.all()  
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        proveedor_id = request.form.get('proveedor_id')
        cantidad = request.form.get('cantidad')
        fecha = request.form.get('fecha')
        if not nombre or not proveedor_id or not cantidad or not fecha:
            flash('Todos los campos son requeridos', 'error')
        else:
            inventario = Inventario(
                nombre=nombre,
                proveedor_id=proveedor_id,
                cantidad=cantidad,
                fecha=fecha
            )
            db.session.add(inventario)
            db.session.commit()
            flash('Inventario creado con éxito', 'success')
            return redirect(url_for('inventarios'))
    
    return render_template('inventario_form.html', proveedores=proveedores)

@app.route('/inventario/editar/<int:id>', methods=['GET', 'POST'])
def editar_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    proveedores = Proveedor.query.all()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        proveedor_id = request.form.get('proveedor_id')
        cantidad = request.form.get('cantidad')
        fecha = request.form.get('fecha')
        if not nombre or not proveedor_id or not cantidad or not fecha:
            flash('Todos los campos son requeridos', 'error')
        else:
            inventario.nombre = nombre
            inventario.proveedor_id = proveedor_id
            inventario.cantidad = cantidad
            inventario.fecha = fecha
            db.session.commit()
            flash('Inventario actualizado con éxito', 'success')
            return redirect(url_for('inventarios'))
    return render_template('inventario_form.html', inventario=inventario, proveedores=proveedores)

@app.route('/inventario/borrar/<int:id>', methods=['POST'])
def borrar_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    db.session.delete(inventario)
    db.session.commit()
    flash('Inventario eliminado con éxito', 'success')
    return redirect(url_for('inventarios'))


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/cliente/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es requerido', 'error')
        else:
            cliente = Cliente(nombre=nombre)
            db.session.add(cliente)
            db.session.commit()
            return redirect(url_for('clientes'))
    return render_template('cliente_form.html')

@app.route('/cliente/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es requerido', 'error')
        else:
            cliente.nombre = nombre
            db.session.commit()
            return redirect(url_for('clientes'))
    return render_template('cliente_form.html', cliente=cliente)

@app.route('/cliente/borrar/<int:id>', methods=['POST'])
def borrar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('clientes'))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/ventas')
def ventas():
    ventas = Venta.query.all()
    return render_template('ventas.html', ventas=ventas)

@app.route('/venta/nuevo', methods=['GET', 'POST'])
def nuevo_venta():
    clientes = Cliente.query.all()
    equipos = Equipo.query.all()
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        equipo_id = request.form.get('equipo_id')
        precio = request.form.get('precio')
        fecha = request.form.get('fecha')
        if not cliente_id or not equipo_id or not precio or not fecha:
            flash('Todos los campos son requeridos', 'error')
        else:
            venta = Venta(
                cliente_id=cliente_id,
                equipo_id=equipo_id,
                precio=precio,
                fecha=fecha
            )
            db.session.add(venta)
            db.session.commit()
            return redirect(url_for('ventas'))
    return render_template('venta_form.html', clientes=clientes, equipos=equipos)

@app.route('/venta/editar/<int:id>', methods=['GET', 'POST'])
def editar_venta(id):
    venta = Venta.query.get_or_404(id)
    clientes = Cliente.query.all()
    equipos = Equipo.query.all()
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        equipo_id = request.form.get('equipo_id')
        precio = request.form.get('precio')
        fecha = request.form.get('fecha')
        if not cliente_id or not equipo_id or not precio or not fecha:
            flash('Todos los campos son requeridos', 'error')
        else:
            venta.cliente_id = cliente_id
            venta.equipo_id = equipo_id
            venta.precio = precio
            venta.fecha = fecha
            db.session.commit()
            return redirect(url_for('ventas'))
    return render_template('venta_form.html', venta=venta, clientes=clientes, equipos=equipos)


@app.route('/venta/borrar/<int:id>', methods=['POST'])
def borrar_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    return redirect(url_for('ventas'))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

