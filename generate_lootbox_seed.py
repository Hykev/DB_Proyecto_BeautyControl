import random
from datetime import datetime, timedelta
from faker import Faker

# =========================================================
# CONFIGURACIÓN
# =========================================================
fake = Faker("es_MX")  # idioma más realista
Faker.seed(42)
random.seed(42)

NUM_CLIENTES = 500
NUM_PROVEEDORES = 50
NUM_PRODUCTOS = 2000
NUM_PAGOS = 3000
NUM_ENVIOS = 2000
NUM_ORDENES = 5000
NUM_DEVOLUCIONES = 600
OUTPUT_FILE = "SQL_DB_Template/seed_lootbox_data.sql"  # guarda directo ahí

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def random_date(start, end):
    delta = end - start
    random_days = random.randrange(delta.days)
    random_seconds = random.randrange(86400)
    return start + timedelta(days=random_days, seconds=random_seconds)

def sql_escape(s):
    return s.replace("'", "''")

# =========================================================
# ARCHIVO DE SALIDA
# =========================================================
sql = []
sql.append("USE LootBox;\n")
sql.append("SET FOREIGN_KEY_CHECKS = 0;\n")

# =========================================================
# 0️⃣ CATEGORÍAS BASE
# =========================================================
sql.append("-- CATEGORÍAS\n")
categorias = [
    ("Electrónica", "Dispositivos y accesorios electrónicos"),
    ("Hogar", "Artículos para el hogar y cocina"),
    ("Deportes", "Ropa y equipo deportivo"),
    ("Moda", "Ropa, calzado y accesorios"),
    ("Juguetes", "Juguetes y entretenimiento"),
    ("Belleza", "Cuidado personal y cosméticos"),
    ("Automotriz", "Repuestos y accesorios para autos"),
    ("Mascotas", "Artículos para animales domésticos"),
    ("Librería", "Libros, papelería y oficina"),
    ("Videojuegos", "Consolas y juegos electrónicos")
]
for nombre, desc in categorias:
    sql.append(f"INSERT INTO Categories (Nombre,Descripción) VALUES ('{nombre}','{desc}');")

# =========================================================
# 1️⃣ PROVEEDORES
# =========================================================
sql.append("\n-- PROVEEDORES\n")
for _ in range(NUM_PROVEEDORES):
    nombre_proveedor = sql_escape(fake.company())
    contacto = sql_escape(fake.name())
    email = sql_escape(fake.company_email())
    telefono = f"+{random.randint(1,99)}-{random.randint(100000000,999999999)}"
    country_id = random.randint(1, 22)
    sql.append(f"INSERT INTO Suppliers (`Nombre de proveedor`,`Nombre de contacto`,Email,`Teléfono`,Countries_ID) "
               f"VALUES ('{nombre_proveedor}','{contacto}','{email}','{telefono}',{country_id});")

# =========================================================
# 2️⃣ PRODUCTOS
# =========================================================
sql.append("\n-- PRODUCTOS\n")
for _ in range(NUM_PRODUCTOS):
    nombre = sql_escape(fake.catch_phrase())
    precio = round(random.uniform(50, 5000), 2)
    cat_id = random.randint(1, 10)
    sup_id = random.randint(1, NUM_PROVEEDORES)
    sql.append(f"INSERT INTO Products (`Nombre del producto`,Precio,`Categories_ID`,`Suppliers_ID`) "
               f"VALUES ('{nombre}',{precio},{cat_id},{sup_id});")

# =========================================================
# 3️⃣ CLIENTES
# =========================================================
sql.append("\n-- CLIENTES\n")
for _ in range(NUM_CLIENTES):
    nombre = sql_escape(fake.first_name())
    apellido = sql_escape(fake.last_name())
    email = sql_escape(fake.email())
    tel = f"+{random.randint(1,99)}-{random.randint(10000000,99999999)}"
    direccion = sql_escape(fake.address().replace("\n", ", "))
    city_id = random.randint(1, 220)
    sql.append(f"INSERT INTO Customers (Nombre,Apellido,Email,`Teléfono`,`Dirección`,Cities_ID) "
               f"VALUES ('{nombre}','{apellido}','{email}','{tel}','{direccion}',{city_id});")

# =========================================================
# 4️⃣ PAGOS
# =========================================================
sql.append("\n-- PAGOS\n")
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
metodos = ["EFECTIVO", "TARJETA", "TRANSFERENCIA"]
for _ in range(NUM_PAGOS):
    fecha = random_date(start_date, end_date).strftime('%Y-%m-%d %H:%M:%S')
    metodo = random.choice(metodos)
    cantidad = round(random.uniform(100, 5000), 2)
    cliente = random.randint(1, NUM_CLIENTES)
    sql.append(f"INSERT INTO Payments (`Fecha de pago`,`Método de  pago`,`Cantidad`,`Customers_ID`) "
               f"VALUES ('{fecha}','{metodo}',{cantidad},{cliente});")

# =========================================================
# 5️⃣ ENVIOS
# =========================================================
sql.append("\n-- ENVIOS\n")
status_opts = ["EN TRANSITO", "ENTREGADO", "RETRASADO"]
for _ in range(NUM_ENVIOS):
    f_envio = random_date(start_date, end_date)
    f_entrega = f_envio + timedelta(days=random.randint(1, 7))
    status = random.choice(status_opts)
    wh_id = random.randint(1, 5)
    sql.append(f"INSERT INTO Shipments (`Fecha de envio`,`Fecha de entrega`,Status,Warehouses_ID) "
               f"VALUES ('{f_envio:%Y-%m-%d %H:%M:%S}','{f_entrega:%Y-%m-%d %H:%M:%S}','{status}',{wh_id});")

# =========================================================
# 6️⃣ EMPLEADO BASE
# =========================================================
sql.append("\n-- EMPLEADOS BASE\n")
sql.append("INSERT INTO Users (`Nombre de usuario`,Email,Contraseña,Rol,Estado) VALUES "
           "('empleado1','empleado1@lootbox.com','emp123','empleado','activo');")
sql.append("INSERT INTO Employees (Nombre,Apellido,Email,`Teléfono`,Rol,Users_ID) VALUES "
           "('Pedro','Santos','pedro.santos@lootbox.com','+502-4000-0001','Vendedor',1);")

# =========================================================
# 7️⃣ ORDENES
# =========================================================
sql.append("\n-- ORDENES\n")
for i in range(NUM_ORDENES):
    f_orden = random_date(start_date, end_date)
    status = random.choice(["PENDIENTE", "ENVIADO", "ENTREGADO", "REGRESADO"])
    total = round(random.uniform(100, 8000), 2)
    pay_id = random.randint(1, NUM_PAGOS)
    cust_id = random.randint(1, NUM_CLIENTES)
    emp_id = 1
    ship_id = random.randint(1, NUM_ENVIOS)
    sql.append(f"INSERT INTO Ordenes (`Fecha de la orden`,Status,Total,Payments_ID,Customers_ID,Employees_ID,Shipments_ID) "
               f"VALUES ('{f_orden:%Y-%m-%d %H:%M:%S}','{status}',{total},{pay_id},{cust_id},{emp_id},{ship_id});")

# =========================================================
# 8️⃣ ORDER ITEMS (productos únicos por orden)
# =========================================================
sql.append("\n-- ORDER ITEMS\n")
for orden_id in range(1, NUM_ORDENES + 1):
    used_products = set()
    num_items = random.randint(1, 5)
    while len(used_products) < num_items:
        prod_id = random.randint(1, NUM_PRODUCTOS)
        if prod_id in used_products:
            continue  # evita duplicar el mismo producto en la misma orden
        used_products.add(prod_id)
        cantidad = random.randint(1, 5)
        precio_u = round(random.uniform(50, 5000), 2)
        sql.append(f"INSERT INTO Order_items (Products_ID,Ordenes_ID,Cantidad,`Precio por unidad`) "
                   f"VALUES ({prod_id},{orden_id},{cantidad},{precio_u});")

# =========================================================
# 9️⃣ DEVOLUCIONES
# =========================================================
sql.append("\n-- DEVOLUCIONES\n")
razones = [
    "Producto defectuoso", "Error en el tamaño", "Color diferente",
    "Retraso en la entrega", "No era lo esperado", "Error en el pedido"
]
for _ in range(NUM_DEVOLUCIONES):
    f_dev = random_date(start_date, end_date)
    monto = round(random.uniform(50, 1000), 2)
    orden_id = random.randint(1, NUM_ORDENES)
    cust_id = random.randint(1, NUM_CLIENTES)
    razon = sql_escape(random.choice(razones))
    sql.append(f"INSERT INTO Devoluciones (Razón,`Fecha de devolución`,`Cantidad de reembolso`,Ordenes_ID,Customers_ID) "
               f"VALUES ('{razon}','{f_dev:%Y-%m-%d %H:%M:%S}',{monto},{orden_id},{cust_id});")

sql.append("\nSET FOREIGN_KEY_CHECKS = 1;")

# =========================================================
# GUARDAR ARCHIVO
# =========================================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(sql))

print(f"\n✅ Archivo '{OUTPUT_FILE}' generado correctamente con orden lógico y dependencias listas.")
