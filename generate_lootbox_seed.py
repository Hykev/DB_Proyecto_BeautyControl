# =========================================================
# GENERADOR DE DATOS PARA LOOTBOX DATABASE
# =========================================================
# Autor: Kevin & Marisa
# Salida: SQL_DB_Template/seed_lootbox_data.sql
# =========================================================

import random
from datetime import datetime, timedelta
from faker import Faker

# Inicializar Faker y semillas de aleatoriedad
fake = Faker('es_ES')
Faker.seed(42)
random.seed(42)

# =========================================================
# CONFIGURACIÓN GLOBAL
# =========================================================
OUTPUT_FILE = "SQL_DB_Template/seed_lootbox_data.sql"

NUM_PAISES = 22       # ya existen por seed_countries_cities.sql
NUM_CIUDADES = 220    # idem
NUM_CATEGORIES = 10
NUM_SUPPLIERS = 50
NUM_PRODUCTS = 2000
NUM_CUSTOMERS = 500
NUM_EMPLOYEES = 10
NUM_PAYMENTS = 3000
NUM_SHIPMENTS = 2000
NUM_ORDERS = 5000
NUM_ORDER_ITEMS_MAX = 5
NUM_DEVOLUCIONES = 600
NUM_WAREHOUSES = 5
NUM_PROMOTIONS = 10
NUM_LOYALTY_MOVES = 200
NUM_INVENTORY_MOVES = 2000

# Fechas aleatorias entre el último año
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365)

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def random_date(start=START_DATE, end=END_DATE):
    """Devuelve una fecha aleatoria entre start y end."""
    delta = end - start
    random_days = random.randrange(delta.days)
    random_seconds = random.randrange(86400)
    return start + timedelta(days=random_days, seconds=random_seconds)

def sql_escape(s: str) -> str:
    """Escapa comillas simples para SQL."""
    return s.replace("'", "''")

def random_phone():
    """Genera un número de teléfono internacional ficticio."""
    return f"+{random.randint(1,99)}-{random.randint(10000000,999999999)}"

def print_progress(section):
    print(f"✅ Generando {section}...")

# =========================================================
# ARCHIVO DE SALIDA
# =========================================================
sql_lines = []
sql_lines.append("USE LootBox;\n")
sql_lines.append("SET FOREIGN_KEY_CHECKS = 0;\n")

print("🧩 Iniciando generación de datos para LootBox...\n")

# =========================================================
# 🧱 BLOQUE 2 — CATEGORÍAS, PROVEEDORES Y PRODUCTOS
# =========================================================

print_progress("Categorías, Proveedores y Productos")

# ---------------------------------------------------------
# 1️⃣ CATEGORÍAS
# ---------------------------------------------------------
category_names = [
    "Figuras Funko Pop", "Cartas Coleccionables", "Cómics y Mangas", "Ropa Geek",
    "Videojuegos", "Accesorios de Anime", "Coleccionables de Cine", "Decoración Gamer",
    "Consolas Retro", "Posters y Arte"
]

sql_lines.append("-- CATEGORÍAS\n")

for name in category_names:
    descripcion = sql_escape(fake.sentence(nb_words=8))
    sql_lines.append(
        f"INSERT INTO Categories (Nombre, Descripción) VALUES ('{name}', '{descripcion}');"
    )

# ---------------------------------------------------------
# 2️⃣ PROVEEDORES
# ---------------------------------------------------------
sql_lines.append("\n-- PROVEEDORES\n")

# Proveedores adaptados a marcas geek populares
geek_suppliers = [
    "Funko Inc.", "Bandai Spirits", "Nintendo Merch", "Hasbro Collectibles", "Crunchyroll Store",
    "Marvel Licensing", "DC Universe Goods", "Square Enix Shop", "GameStop Partners", "Hot Topic Co.",
    "Loungefly", "Good Smile Company", "Kotobukiya", "The Pokémon Company", "LEGO Collectors",
    "Capcom Gear", "Namco Toys", "Wizards of the Coast", "Ubisoft Merch", "Blizzard Gear Store"
]

for i in range(NUM_SUPPLIERS):
    nombre_prov = sql_escape(random.choice(geek_suppliers) + f" #{i+1}")
    contacto = sql_escape(fake.name())
    email = sql_escape(fake.company_email())
    telefono = random_phone()
    country_id = random.randint(1, NUM_PAISES)
    sql_lines.append(
        f"INSERT INTO Suppliers (`Nombre de proveedor`, `Nombre de contacto`, Email, `Teléfono`, Countries_ID) "
        f"VALUES ('{nombre_prov}', '{contacto}', '{email}', '{telefono}', {country_id});"
    )

# ---------------------------------------------------------
# 3️⃣ PRODUCTOS
# ---------------------------------------------------------
sql_lines.append("\n-- PRODUCTOS\n")

# Temas geek para productos
geek_brands = [
    "Marvel", "DC", "Star Wars", "Harry Potter", "Pokémon", "Dragon Ball", "Naruto",
    "One Piece", "Zelda", "Halo", "Spider-Man", "Batman", "Stranger Things", "Attack on Titan",
    "Demon Slayer", "League of Legends", "Minecraft", "Elden Ring", "Final Fantasy", "Genshin Impact"
]

geek_items = [
    "Funko Pop", "Figura de acción", "Camiseta", "Taza temática", "Sudadera", "Poster",
    "Cartas coleccionables", "Set de pines", "Consola retro", "Mousepad RGB",
    "Control Edición Limitada", "Llavero metálico", "Lámpara LED", "Caja misteriosa", "Réplica coleccionable"
]

# Relación aproximada entre tipo de ítem y categoría
category_map = {
    "Funko Pop": 1,  # Figuras Funko Pop
    "Figura de acción": 1,
    "Cartas coleccionables": 2,
    "Cómic": 3,
    "Manga": 3,
    "Camiseta": 4,
    "Sudadera": 4,
    "Videojuego": 5,
    "Accesorio": 6,
    "Poster": 10,
    "Set de pines": 6,
    "Lámpara": 8,
    "Consola retro": 9,
    "Control Edición Limitada": 9,
    "Caja misteriosa": 7,
    "Réplica coleccionable": 7
}

for i in range(NUM_PRODUCTS):
    brand = random.choice(geek_brands)
    item = random.choice(geek_items)
    personaje = fake.first_name()
    nombre = sql_escape(f"{item} de {brand}: {personaje}")
    precio = round(random.uniform(10, 800), 2)
    categoria_id = category_map.get(item, random.randint(1, NUM_CATEGORIES))
    supplier_id = random.randint(1, NUM_SUPPLIERS)
    sql_lines.append(
        f"INSERT INTO Products (`Nombre del producto`, Precio, `Categories_ID`, `Suppliers_ID`) "
        f"VALUES ('{nombre}', {precio}, {categoria_id}, {supplier_id});"
    )

# =========================================================
# 🧍 BLOQUE 3 — CLIENTES, USUARIOS Y EMPLEADOS
# =========================================================

print_progress("Clientes, Usuarios y Empleados")

# ---------------------------------------------------------
# CLIENTES
# ---------------------------------------------------------
sql_lines.append("\n-- CLIENTES\n")

for i in range(NUM_CUSTOMERS):
    nombre = sql_escape(fake.first_name())
    apellido = sql_escape(fake.last_name())
    email = sql_escape(fake.email())
    telefono = random_phone()
    direccion = sql_escape(fake.address().replace("\n", ", "))
    city_id = random.randint(1, NUM_CIUDADES)
    sql_lines.append(
        f"INSERT INTO Customers (Nombre, Apellido, Email, `Teléfono`, `Dirección`, Cities_ID) "
        f"VALUES ('{nombre}', '{apellido}', '{email}', '{telefono}', '{direccion}', {city_id});"
    )

# ---------------------------------------------------------
# USUARIOS (Clientes + Admin + Empleados)
# ---------------------------------------------------------
sql_lines.append("\n-- USUARIOS\n")

# Usuarios de clientes (1 por cliente)
for i in range(1, NUM_CUSTOMERS + 1):
    username = f"user{i}"
    email = f"user{i}@lootbox.com"
    password = "user123"
    sql_lines.append(
        f"INSERT INTO Users (`Nombre de usuario`, Email, Contraseña, Rol, Estado, Customers_ID) "
        f"VALUES ('{username}', '{email}', '{password}', 'cliente', 'activo', {i});"
    )

# Usuario administrador general
sql_lines.append(
    "INSERT INTO Users (`Nombre de usuario`, Email, Contraseña, Rol, Estado) "
    "VALUES ('admin', 'admin@lootbox.com', 'admin123', 'admin', 'activo');"
)

# Usuarios de empleados (después del admin)
for i in range(NUM_EMPLOYEES):
    username = f"empleado{i+1}"
    email = f"empleado{i+1}@lootbox.com"
    password = "emp123"
    sql_lines.append(
        f"INSERT INTO Users (`Nombre de usuario`, Email, Contraseña, Rol, Estado) "
        f"VALUES ('{username}', '{email}', '{password}', 'empleado', 'activo');"
    )

# ---------------------------------------------------------
# EMPLEADOS
# ---------------------------------------------------------
sql_lines.append("\n-- EMPLEADOS\n")

roles = ["Vendedor", "Atención al cliente", "Repartidor", "Gerente", "Supervisor"]
for i in range(NUM_EMPLOYEES):
    nombre = sql_escape(fake.first_name())
    apellido = sql_escape(fake.last_name())
    email = f"empleado{i+1}@lootbox.com"
    telefono = random_phone()
    rol = random.choice(roles)
    # ID de usuario correspondiente (clientes + 1 admin + offset empleados)
    user_id = NUM_CUSTOMERS + 1 + (i + 1)
    sql_lines.append(
        f"INSERT INTO Employees (Nombre, Apellido, Email, `Teléfono`, Rol, Users_ID) "
        f"VALUES ('{nombre}', '{apellido}', '{email}', '{telefono}', '{rol}', {user_id});"
    )

# =========================================================
# 🚚 BLOQUE 4 — WAREHOUSES, INVENTORY MOVEMENTS Y SHIPMENTS
# =========================================================

print_progress("Warehouses, Movimientos de Inventario y Envíos")

# ---------------------------------------------------------
# WAREHOUSES
# ---------------------------------------------------------
sql_lines.append("\n-- WAREHOUSES\n")

for i in range(NUM_WAREHOUSES):
    nombre = f"Bodega {i+1}"
    direccion = sql_escape(fake.street_address())
    city_id = random.randint(1, NUM_CIUDADES)
    sql_lines.append(
        f"INSERT INTO Warehouses (Nombre, `Dirección`, Cities_ID) "
        f"VALUES ('{nombre}', '{direccion}', {city_id});"
    )

# ---------------------------------------------------------
# INVENTORY MOVEMENTS
# ---------------------------------------------------------
sql_lines.append("\n-- INVENTORY MOVEMENTS\n")

tipos_mov = ["IN", "OUT"]
for i in range(NUM_INVENTORY_MOVES):
    producto_id = random.randint(1, NUM_PRODUCTS)
    warehouse_id = random.randint(1, NUM_WAREHOUSES)
    cantidad = random.randint(1, 50)
    tipo = random.choice(tipos_mov)
    fecha = random_date()
    empleado_id = random.randint(1, NUM_EMPLOYEES)
    sql_lines.append(
        f"INSERT INTO inventory_movements (Products_ID, Warehouses_ID, Cantidad, `Tipo de movimiento`, `Fecha del movimiento`, Employees_ID) "
        f"VALUES ({producto_id}, {warehouse_id}, {cantidad}, '{tipo}', '{fecha:%Y-%m-%d %H:%M:%S}', {empleado_id});"
    )

# ---------------------------------------------------------
# SHIPMENTS
# ---------------------------------------------------------
sql_lines.append("\n-- SHIPMENTS\n")

status_opts = ["EN TRANSITO", "ENTREGADO", "RETRASADO"]
for i in range(NUM_SHIPMENTS):
    f_envio = random_date()
    f_entrega = f_envio + timedelta(days=random.randint(1, 7))
    status = random.choice(status_opts)
    warehouse_id = random.randint(1, NUM_WAREHOUSES)
    sql_lines.append(
        f"INSERT INTO Shipments (`Fecha de envio`, `Fecha de entrega`, Status, Warehouses_ID) "
        f"VALUES ('{f_envio:%Y-%m-%d %H:%M:%S}', '{f_entrega:%Y-%m-%d %H:%M:%S}', '{status}', {warehouse_id});"
    )

# =========================================================
# 💳 BLOQUE 5 — PAYMENTS, ORDERS, ORDER_ITEMS Y DEVOLUCIONES
# =========================================================

print_progress("Pagos, Órdenes, Detalles y Devoluciones")

# ---------------------------------------------------------
# PAYMENTS
# ---------------------------------------------------------
sql_lines.append("\n-- PAYMENTS\n")

metodos_pago = ["EFECTIVO", "TARJETA", "TRANSFERENCIA"]
for i in range(NUM_PAYMENTS):
    fecha_pago = random_date()
    metodo = random.choice(metodos_pago)
    cantidad = round(random.uniform(50, 8000), 2)
    cliente_id = random.randint(1, NUM_CUSTOMERS)
    sql_lines.append(
        f"INSERT INTO Payments (`Fecha de pago`, `Método de  pago`, `Cantidad`, Customers_ID) "
        f"VALUES ('{fecha_pago:%Y-%m-%d %H:%M:%S}', '{metodo}', {cantidad}, {cliente_id});"
    )

# ---------------------------------------------------------
# ORDERS
# ---------------------------------------------------------
sql_lines.append("\n-- ORDERS\n")

status_orden = ["PENDIENTE", "ENVIADO", "ENTREGADO", "REGRESADO"]
for i in range(NUM_ORDERS):
    fecha_orden = random_date()
    status = random.choice(status_orden)
    total = round(random.uniform(100, 15000), 2)
    payment_id = random.randint(1, NUM_PAYMENTS)
    customer_id = random.randint(1, NUM_CUSTOMERS)
    employee_id = random.randint(1, NUM_EMPLOYEES)
    shipment_id = random.randint(1, NUM_SHIPMENTS)
    sql_lines.append(
        f"INSERT INTO Ordenes (`Fecha de la orden`, Status, Total, Payments_ID, Customers_ID, Employees_ID, Shipments_ID) "
        f"VALUES ('{fecha_orden:%Y-%m-%d %H:%M:%S}', '{status}', {total}, {payment_id}, {customer_id}, {employee_id}, {shipment_id});"
    )

# ---------------------------------------------------------
# ORDER ITEMS
# ---------------------------------------------------------
sql_lines.append("\n-- ORDER ITEMS\n")

for order_id in range(1, NUM_ORDERS + 1):
    num_items = random.randint(1, NUM_ORDER_ITEMS_MAX)
    productos_asignados = set()  # evitar productos duplicados por orden
    for _ in range(num_items):
        prod_id = random.randint(1, NUM_PRODUCTS)
        while prod_id in productos_asignados:
            prod_id = random.randint(1, NUM_PRODUCTS)
        productos_asignados.add(prod_id)
        cantidad = random.randint(1, 5)
        precio_u = round(random.uniform(20, 5000), 2)
        sql_lines.append(
            f"INSERT INTO Order_items (Products_ID, Ordenes_ID, Cantidad, `Precio por unidad`) "
            f"VALUES ({prod_id}, {order_id}, {cantidad}, {precio_u});"
        )

# ---------------------------------------------------------
# DEVOLUCIONES
# ---------------------------------------------------------
sql_lines.append("\n-- DEVOLUCIONES\n")

razones = [
    "Producto defectuoso", "Error en el tamaño", "Color incorrecto",
    "Retraso en la entrega", "No era lo esperado", "Pedido incompleto"
]
for i in range(NUM_DEVOLUCIONES):
    fecha_dev = random_date()
    monto = round(random.uniform(50, 2000), 2)
    orden_id = random.randint(1, NUM_ORDERS)
    cliente_id = random.randint(1, NUM_CUSTOMERS)
    razon = sql_escape(random.choice(razones))
    sql_lines.append(
        f"INSERT INTO Devoluciones (Razón, `Fecha de devolución`, `Cantidad de reembolso`, Ordenes_ID, Customers_ID) "
        f"VALUES ('{razon}', '{fecha_dev:%Y-%m-%d %H:%M:%S}', {monto}, {orden_id}, {cliente_id});"
    )

# ---------------------------------------------------------
# RELACIONAR DEVOLUCIONES CON ORDER_ITEMS
# ---------------------------------------------------------
sql_lines.append("\n-- RELACIONAR DEVOLUCIONES CON ORDER_ITEMS\n")

# Elegimos algunas devoluciones para vincular con un item específico
num_relaciones = min(NUM_DEVOLUCIONES, NUM_ORDERS // 2)  # máximo la mitad de las órdenes
for i in range(1, num_relaciones + 1):
    devolucion_id = i
    orden_id = random.randint(1, NUM_ORDERS)
    sql_lines.append(
        f"UPDATE Order_items "
        f"SET Devoluciones_ID = {devolucion_id} "
        f"WHERE Ordenes_ID = {orden_id} "
        f"AND Devoluciones_ID IS NULL "
        f"LIMIT 1;"
    )

# =========================================================
# 🎁 BLOQUE 6 — PROMOTIONS Y LOYALTY MOVEMENTS
# =========================================================

print_progress("Promociones y Movimientos de Lealtad")

# ---------------------------------------------------------
# PROMOTIONS
# ---------------------------------------------------------
sql_lines.append("\n-- PROMOTIONS\n")

geek_promos = [
    "Semana del Anime",
    "2x1 en Funkos Marvel",
    "Descuento Gamer Weekend",
    "Mes de los Superhéroes",
    "Evento Retro Consolas",
    "Black Friday Geek",
    "Colecciona y Gana",
    "Semana del Cómic",
    "Festival Otaku",
    "Cyber LootBox Days"
]

for i in range(NUM_PROMOTIONS):
    nombre = f"{geek_promos[i % len(geek_promos)]}"
    descripcion = sql_escape(fake.sentence(nb_words=10))
    descuento = round(random.uniform(5, 40), 2)
    fecha_inicio = random_date(START_DATE, END_DATE - timedelta(days=30))
    fecha_fin = fecha_inicio + timedelta(days=random.randint(10, 60))
    activa = random.choice([0, 1])
    categoria_id = random.randint(1, NUM_CATEGORIES)
    sql_lines.append(
        f"INSERT INTO Promotions (Nombre, Descripción, Descuento_porcentaje, Fecha_inicio, Fecha_fin, Activa, Categories_ID) "
        f"VALUES ('{nombre}', '{descripcion}', {descuento}, '{fecha_inicio:%Y-%m-%d %H:%M:%S}', '{fecha_fin:%Y-%m-%d %H:%M:%S}', {activa}, {categoria_id});"
    )

# ---------------------------------------------------------
# LOYALTY MOVEMENTS
# ---------------------------------------------------------
sql_lines.append("\n-- LOYALTY MOVEMENTS\n")

geek_loyalty_descriptions = [
    "Compra de figura Funko",
    "Canje de puntos por carta rara",
    "Bonificación por evento de anime",
    "Devolución de producto coleccionable",
    "Compra durante promoción gamer",
    "Participación en torneo de TCG",
    "Compra anticipada de edición limitada"
]

for i in range(NUM_LOYALTY_MOVES):
    fecha = random_date()
    puntos = random.randint(-50, 150)  # algunos suman, otros restan
    descripcion = sql_escape(random.choice(geek_loyalty_descriptions))
    cliente_id = random.randint(1, NUM_CUSTOMERS)
    orden_id = random.randint(1, NUM_ORDERS)
    sql_lines.append(
        f"INSERT INTO Loyalty_movements (Fecha, Puntos_cambio, Descripción, Customers_ID, Ordenes_ID) "
        f"VALUES ('{fecha:%Y-%m-%d %H:%M:%S}', {puntos}, '{descripcion}', {cliente_id}, {orden_id});"
    )

# ---------------------------------------------------------
# FINALIZAR ARCHIVO
# ---------------------------------------------------------
sql_lines.append("\n-- REACTIVAR CLAVES FORÁNEAS\n")
sql_lines.append("SET FOREIGN_KEY_CHECKS = 1;\n")

# Guardar archivo SQL
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(sql_lines))

print("\n✅ Archivo generado con éxito:")
print(f"📄 {OUTPUT_FILE}")

print("\n🎉 Generación completa de datos para LootBox finalizada con éxito.")
print(f"📦 Datos generados para {NUM_CUSTOMERS} clientes, {NUM_PRODUCTS} productos, {NUM_ORDERS} órdenes, etc.")

