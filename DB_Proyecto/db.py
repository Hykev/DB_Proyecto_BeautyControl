from mysql.connector import Error, IntegrityError

"""
Capa de acceso a datos para el proyecto LootBox.

- Maneja la conexión a MySQL (schema LootBox).
- Expone funciones de CRUD para:
  - Customers
  - Products
  - Orders (resumen + detalle)
  - Inventory & Warehouses
  - Promotions & Loyalty
  - Audit log
- Expone funciones genéricas para:
  - Ejecutar SELECT que regresan listas de diccionarios.
  - Ejecutar INSERT/UPDATE/DELETE y SPs.
"""

import mysql.connector
from mysql.connector import Error

# -----------------------------------------------------------------------------
# Configuración de conexión
# -----------------------------------------------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "lootbox", 
    "port": 3306,
}


def get_connection():
    """Crea y devuelve una conexión nueva a MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


# -----------------------------------------------------------------------------
# Helpers genéricos
# -----------------------------------------------------------------------------

def run_select(query: str, params: tuple | None = None) -> list[dict]:
    """
    Ejecuta un SELECT y devuelve una lista de diccionarios.
    Cada diccionario representa una fila: {columna: valor}.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print("Error en run_select:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def run_execute(query: str, params: tuple | None = None) -> int:
    """
    Ejecuta un INSERT/UPDATE/DELETE y devuelve el número de filas afectadas.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.rowcount
    except Error as e:
        print("Error en run_execute:", e)
        if conn:
            conn.rollback()
        return 0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def run_callproc(proc_name: str, params: list | tuple | None = None):
    """
    Ejecuta un procedimiento almacenado y devuelve (filas, valores_salida).

    - filas: lista de diccionarios si el SP devuelve un resultset.
    - valores_salida: tupla con los parámetros OUT/INOUT (si los hay).
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc(proc_name, params or [])

        # MySQL Connector expone los result sets de cada ejecución
        result_sets = []
        for result in cursor.stored_results():
            result_sets.extend(result.fetchall())

        # Los parámetros de salida modificados están en cursor._stored_results,
        # pero para simplificar, devolvemos únicamente el resultset.
        conn.commit()
        return result_sets
    except Error as e:
        print(f"Error al ejecutar SP {proc_name}:", e)
        if conn:
            conn.rollback()
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# -----------------------------------------------------------------------------
# Customers (CRUD + listados con filtros)
# -----------------------------------------------------------------------------

def get_customers(
    nombre: str | None = None,
    email: str | None = None,
    country_id: int | None = None,
    page: int = 0,
    page_size: int = 20,
) -> list[dict]:
    """
    Devuelve un listado paginado de clientes, con joins a ciudad y país.
    Aplica filtros opcionales por nombre, email y país.
    """
    base_query = """
        SELECT
            cu.ID,
            cu.Nombre,
            cu.Apellido,
            cu.Email,
            cu.`Teléfono` AS Telefono,
            cu.`Dirección` AS Direccion,
            cu.`Fecha de creación` AS FechaCreacion,
            ci.Nombre AS Ciudad,
            co.Nombre AS Pais,
            ci.ID AS Cities_ID,
            co.ID AS Countries_ID
        FROM Customers cu
        JOIN Cities ci ON ci.ID = cu.Cities_ID
        JOIN Countries co ON co.ID = ci.Countries_ID
        WHERE 1 = 1
    """
    params: list = []

    # Filtro por nombre/apellido (LIKE)
    if nombre:
        base_query += " AND (cu.Nombre LIKE %s OR cu.Apellido LIKE %s) "
        like = f"%{nombre}%"
        params.extend([like, like])

    # Filtro por email (usando índice funcional LOWER(Email))
    if email:
        base_query += " AND LOWER(cu.Email) = LOWER(%s) "
        params.append(email)

    # Filtro por país
    if country_id:
        base_query += " AND co.ID = %s "
        params.append(country_id)

    base_query += " ORDER BY cu.ID ASC LIMIT %s OFFSET %s "
    params.extend([page_size, page * page_size])

    return run_select(base_query, tuple(params))


def get_customer_by_id(customer_id: int) -> dict | None:
    """Devuelve un cliente específico por ID (o None si no existe)."""
    rows = run_select(
        """
        SELECT
            cu.ID,
            cu.Nombre,
            cu.Apellido,
            cu.Email,
            cu.`Teléfono` AS Telefono,
            cu.`Dirección` AS Direccion,
            cu.`Fecha de creación` AS FechaCreacion,
            cu.Cities_ID
        FROM Customers cu
        WHERE cu.ID = %s
        """,
        (customer_id,),
    )
    return rows[0] if rows else None


def create_customer(nombre, apellido, email, telefono, direccion, city_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO customers (Nombre, Apellido, Email, Teléfono, Dirección, Cities_ID)
            SELECT %s, %s, %s, %s, %s, c.ID FROM cities c WHERE c.ID = %s
            """,
            (nombre, apellido, email, telefono, direccion, city_id),
        )
        conn.commit()
        return True
    except Error as e:
        print("Error en run_execute:", e)
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def update_customer(
    customer_id: int,
    nombre: str,
    apellido: str,
    email: str | None,
    telefono: str,
    direccion: str,
    city_id: int,
) -> bool:
    """Actualiza un cliente existente."""
    rowcount = run_execute(
        """
        UPDATE Customers
        SET
            Nombre = %s,
            Apellido = %s,
            Email = %s,
            `Teléfono` = %s,
            `Dirección` = %s,
            Cities_ID = %s
        WHERE ID = %s
        """,
        (nombre, apellido, email, telefono, direccion, city_id, customer_id),
    )
    return rowcount == 1


def delete_customer(customer_id: int) -> tuple[bool, str | None]:
    """Intenta eliminar un cliente. Devuelve (ok, mensaje_error) y registra en Audit_log si procede."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Customers WHERE ID = %s", (customer_id,))
        if cursor.rowcount == 0:
            conn.rollback()
            return False, "No se encontró el cliente a eliminar."

        # Registrar en Audit_log solo si el DELETE fue exitoso
        cursor.execute(
            """
            INSERT INTO Audit_log
                (Fecha_evento, Tabla_afectada, `Operación`, Registro_ID, Users_ID)
            VALUES (NOW(), 'Customers', 'DELETE', %s, NULL)
            """,
            (customer_id,),
        )

        conn.commit()
        return True, None
    except IntegrityError:
        conn.rollback()
        return (
            False,
            "No se puede eliminar el cliente porque tiene registros relacionados (por ejemplo, órdenes o devoluciones)."
        )
    except Error as e:
        conn.rollback()
        return False, f"Error al eliminar cliente: {e}"
    finally:
        cursor.close()
        conn.close()


# -----------------------------------------------------------------------------
# Products (CRUD + listados)
# -----------------------------------------------------------------------------

def get_products(
    category_id: int | None = None,
    category_name: str | None = None,
    supplier_id: int | None = None,
    name: str | None = None,
    page: int = 0,
    page_size: int = 20,
) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            p.ID,
            p.`Nombre del producto` AS NombreProducto,
            p.Precio,
            p.`Fecha de creación` AS FechaCreacion,
            c.Nombre AS CategoriaNombre,
            s.`Nombre de proveedor` AS NombreProveedor
        FROM Products p
        JOIN Categories c ON c.ID = p.Categories_ID
        JOIN Suppliers s ON s.ID = p.Suppliers_ID
        WHERE 1 = 1
    """
    params: list = []

    if category_id is not None:
        query += " AND p.Categories_ID = %s"
        params.append(category_id)

    if category_name:
        query += " AND c.Nombre LIKE %s"
        params.append(f"%{category_name}%")

    if supplier_id is not None:
        query += " AND p.Suppliers_ID = %s"
        params.append(supplier_id)

    if name:
        query += " AND p.`Nombre del producto` LIKE %s"
        params.append(f"%{name}%")

    query += " ORDER BY p.ID LIMIT %s OFFSET %s"
    offset = page * page_size
    params.extend([page_size, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows



def get_product_by_id(product_id: int) -> dict | None:
    """Devuelve un producto por ID."""
    rows = run_select(
        """
        SELECT
            p.ID,
            p.`Nombre del producto` AS NombreProducto,
            p.Precio,
            p.`Fecha de creación` AS FechaCreacion,
            p.Categories_ID,
            p.Suppliers_ID
        FROM Products p
        WHERE p.ID = %s
        """,
        (product_id,),
    )
    return rows[0] if rows else None


def create_product(
    nombre_producto: str,
    precio: float,
    category_id: int,
    supplier_id: int,
) -> bool:
    """Crea un nuevo producto."""
    rowcount = run_execute(
        """
        INSERT INTO Products
            (`Nombre del producto`, Precio, Categories_ID, Suppliers_ID)
        VALUES (%s, %s, %s, %s)
        """,
        (nombre_producto, precio, category_id, supplier_id),
    )
    return rowcount == 1


def update_product(
    product_id: int,
    nombre_producto: str,
    precio: float,
    category_id: int,
    supplier_id: int,
) -> bool:
    """Actualiza un producto."""
    rowcount = run_execute(
        """
        UPDATE Products
        SET
            `Nombre del producto` = %s,
            Precio = %s,
            Categories_ID = %s,
            Suppliers_ID = %s
        WHERE ID = %s
        """,
        (nombre_producto, precio, category_id, supplier_id, product_id),
    )
    return rowcount == 1


def delete_product(product_id: int) -> tuple[bool, str | None]:
    """
    Elimina un producto e inserta un registro en Audit_log si tiene éxito.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Intentamos borrar el producto
        cursor.execute("DELETE FROM Products WHERE ID = %s", (product_id,))
        if cursor.rowcount == 0:
            # No se borró nada (ID inexistente)
            conn.rollback()
            return False, "No se encontró el producto a eliminar."

        # Si llegó aquí, el DELETE sí se realizó → registramos en Audit_log
        cursor.execute(
            """
            INSERT INTO Audit_log
                (Fecha_evento, Tabla_afectada, `Operación`, Registro_ID, Users_ID)
            VALUES (NOW(), 'Products', 'DELETE', %s, NULL)
            """,
            (product_id,),
        )

        conn.commit()
        return True, None

    except IntegrityError:
        # FK: el producto tiene órdenes o movimientos de inventario asociados
        conn.rollback()
        return (
            False,
            "No se puede eliminar el producto porque aparece en órdenes o movimientos de inventario."
        )
    except Error as e:
        conn.rollback()
        return False, f"Error al eliminar producto: {e}"
    finally:
        cursor.close()
        conn.close()



# -----------------------------------------------------------------------------
# Orders (resumen + detalle) y SP para crear orden
# -----------------------------------------------------------------------------

def get_orders(
    customer_id: int | None = None,
    status: str | None = None,
    fecha_desde: str | None = None,
    fecha_hasta: str | None = None,
    page: int = 0,
    page_size: int = 20,
) -> list[dict]:
    """
    Devuelve listado de órdenes con info de cliente, pago y envío.
    fecha_desde / fecha_hasta en formato 'YYYY-MM-DD' (opcional).
    """
    query = """
        SELECT
            o.ID,
            o.`Fecha de la orden` AS FechaOrden,
            o.Status,
            o.Total,
            c.Nombre AS NombreCliente,
            c.Apellido AS ApellidoCliente,
            pay.`Método de  pago` AS MetodoPago,
            s.Status AS EstadoEnvio
        FROM Ordenes o
        JOIN Customers c ON c.ID = o.Customers_ID
        JOIN Payments pay ON pay.ID = o.Payments_ID
        JOIN Shipments s ON s.ID = o.Shipments_ID
        WHERE 1 = 1
    """
    params: list = []

    if customer_id:
        query += " AND o.Customers_ID = %s "
        params.append(customer_id)

    if status:
        query += " AND o.Status = %s "
        params.append(status)

    if fecha_desde:
        query += " AND DATE(o.`Fecha de la orden`) >= %s "
        params.append(fecha_desde)

    if fecha_hasta:
        query += " AND DATE(o.`Fecha de la orden`) <= %s "
        params.append(fecha_hasta)

    query += " ORDER BY o.`Fecha de la orden` DESC LIMIT %s OFFSET %s "
    params.extend([page_size, page * page_size])

    return run_select(query, tuple(params))


def get_order_detail(order_id: int) -> dict:
    """
    Devuelve un diccionario con:
      - 'order': info general de la orden
      - 'items': listado de líneas de orden
      - 'devoluciones': devoluciones asociadas
    """
    order_info = run_select(
        """
        SELECT
            o.ID,
            o.`Fecha de la orden` AS FechaOrden,
            o.Status,
            o.Total,
            c.Nombre AS NombreCliente,
            c.Apellido AS ApellidoCliente,
            c.Email AS EmailCliente,
            pay.`Método de  pago` AS MetodoPago,
            pay.`Fecha de pago` AS FechaPago,
            s.`Fecha de envio` AS FechaEnvio,
            s.`Fecha de entrega` AS FechaEntrega,
            s.Status AS EstadoEnvio
        FROM Ordenes o
        JOIN Customers c ON c.ID = o.Customers_ID
        JOIN Payments pay ON pay.ID = o.Payments_ID
        JOIN Shipments s ON s.ID = o.Shipments_ID
        WHERE o.ID = %s
        """,
        (order_id,),
    )
    order = order_info[0] if order_info else None

    items = run_select(
        """
        SELECT
            oi.Products_ID,
            p.`Nombre del producto` AS NombreProducto,
            oi.Cantidad,
            oi.`Precio por unidad` AS PrecioUnidad,
            (oi.Cantidad * oi.`Precio por unidad`) AS Subtotal,
            oi.Devoluciones_ID
        FROM Order_items oi
        JOIN Products p ON p.ID = oi.Products_ID
        WHERE oi.Ordenes_ID = %s
        """,
        (order_id,),
    )

    devoluciones = run_select(
        """
        SELECT
            d.ID,
            d.`Razón` AS Razon,
            d.`Fecha de devolución` AS FechaDevolucion,
            d.`Cantidad de reembolso` AS Reembolso
        FROM Devoluciones d
        WHERE d.Ordenes_ID = %s
        """,
        (order_id,),
    )

    return {
        "order": order,
        "items": items,
        "devoluciones": devoluciones,
    }

def create_order_simple(
    customer_id: int,
    product_id: int,
    quantity: int,
    employee_id: int,
    warehouse_id: int,
) -> tuple[bool, str | None]:
    """
    Llama al SP sp_crear_orden_simple.
    Devuelve (ok, mensaje_error).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(
            "sp_crear_orden_simple",
            [customer_id, product_id, quantity, employee_id, warehouse_id],
        )
        conn.commit()
        return True, None
    except IntegrityError:
        return (
            False,
            "No se pudo crear la orden: verifica que el cliente, producto, empleado y bodega existan.",
        )
    except Error as e:
        return False, f"Error al crear la orden: {e}"
    finally:
        cursor.close()
        conn.close()
        
# -----------------------------------------------------------------------------
# Inventario: vistas y SPs
# -----------------------------------------------------------------------------
def get_inventory_view(
    product_id: int | None = None,
    warehouse_id: int | None = None,
    page: int = 0,
    page_size: int = 20,
) -> list[dict]:
    """
    Devuelve los datos de la vista vw_inventario_producto_bodega,
    con filtros opcionales por producto y bodega y paginación.

    Aquí normalizamos stock_actual para que nunca sea negativo en la UI.
    """
    query = """
        SELECT
            product_id,
            `Nombre del producto` AS NombreProducto,
            warehouse_id,
            warehouse_nombre,
            GREATEST(stock_actual, 0) AS stock_actual
        FROM vw_inventario_producto_bodega
        WHERE 1 = 1
    """
    params: list = []

    if product_id:
        query += " AND product_id = %s "
        params.append(product_id)

    if warehouse_id:
        query += " AND warehouse_id = %s "
        params.append(warehouse_id)

    query += " ORDER BY NombreProducto, warehouse_nombre LIMIT %s OFFSET %s "
    params.extend([page_size, page * page_size])

    return run_select(query, tuple(params))


def get_stock_producto_bodega(product_id: int, warehouse_id: int) -> list[dict]:
    """
    Usa el SP sp_calcular_stock_producto_bodega para obtener el stock puntual.
    """
    return run_callproc(
        "sp_calcular_stock_producto_bodega",
        [product_id, warehouse_id],
    )


def register_inventory_movement(
    product_id: int,
    warehouse_id: int,
    empleado_id: int,
    cantidad: int,
    tipo_movimiento: str,  # 'IN' o 'OUT'
) -> bool:
    """
    Registra un movimiento de inventario con el SP sp_registrar_movimiento_inventario.
    """
    result = run_callproc(
        "sp_registrar_movimiento_inventario",
        [product_id, warehouse_id, empleado_id, cantidad, tipo_movimiento],
    )
    # Si no lanza error, asumimos éxito
    return True

def get_inventory_summary(page: int = 0, page_size: int = 20) -> list[dict]:
    """
    Devuelve stock actual por producto y bodega.

    Se apoya en la vista vw_inventario_producto_bodega.
    Las columnas reales de la vista son:
      - product_id
      - `Nombre del producto`
      - warehouse_id
      - warehouse_nombre
      - stock_actual
    Aquí las aliasamos para que el frontend pueda usar nombres amigables.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            product_id,
            `Nombre del producto` AS NombreProducto,
            warehouse_id,
            warehouse_nombre AS NombreBodega,
            stock_actual
        FROM vw_inventario_producto_bodega
        ORDER BY product_id, warehouse_id
        LIMIT %s OFFSET %s
    """
    offset = page * page_size
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_stock_for_product_warehouse(product_id: int, warehouse_id: int) -> int:
    """
    Usa el SP sp_calcular_stock_producto_bodega para obtener stock actual.
    Nunca devuelve valores negativos (se truncan a 0).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_calcular_stock_producto_bodega", [product_id, warehouse_id])
        for result in cursor.stored_results():
            row = result.fetchone()
            if row is not None:
                try:
                    stock = int(row[0])
                except (TypeError, ValueError):
                    stock = 0
                return max(stock, 0)
        return 0
    except Error:
        # Si falla el SP, devolvemos 0 para no romper la UI
        return 0
    finally:
        cursor.close()
        conn.close()



def registrar_movimiento_inventario(
    product_id: int,
    warehouse_id: int,
    cantidad: int,
    tipo: str,
) -> tuple[bool, str | None]:
    """
    Llama al SP sp_registrar_movimiento_inventario.
    Devuelve (ok, mensaje_error).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(
            "sp_registrar_movimiento_inventario",
            [product_id, warehouse_id, cantidad, tipo],
        )
        conn.commit()
        return True, None
    except IntegrityError:
        return (
            False,
            "No se pudo registrar el movimiento: verifica que el producto y la bodega existan.",
        )
    except Error as e:
        return False, f"Error al registrar movimiento de inventario: {e}"
    finally:
        cursor.close()
        conn.close()

# -----------------------------------------------------------------------------
# Promociones & Loyalty
# -----------------------------------------------------------------------------

def get_promotions(only_active: bool = True) -> list[dict]:
    """
    Devuelve las promociones, opcionalmente filtrando solo las activas
    y dentro de su rango de fechas.
    """
    query = """
        SELECT
            p.ID,
            p.Nombre,
            p.`Descripción` AS Descripcion,
            p.Descuento_porcentaje,
            p.Fecha_inicio,
            p.Fecha_fin,
            p.Activa,
            c.Nombre AS CategoriaNombre
        FROM Promotions p
        LEFT JOIN Categories c ON c.ID = p.Categories_ID
        WHERE 1 = 1
    """
    params: list = []

    if only_active:
        query += " AND p.Activa = 1 AND NOW() BETWEEN p.Fecha_inicio AND p.Fecha_fin "

    query += " ORDER BY p.Fecha_inicio DESC "
    return run_select(query, tuple(params))


def get_loyalty_movements_by_customer(customer_id: int) -> list[dict]:
    """
    Devuelve los movimientos de lealtad de un cliente.
    """
    query = """
        SELECT
            lm.ID,
            lm.Fecha,
            lm.Puntos_cambio,
            lm.`Descripción` AS Descripcion,
            lm.Ordenes_ID,
            o.`Fecha de la orden` AS FechaOrden,
            o.Total AS TotalOrden
        FROM Loyalty_movements lm
        LEFT JOIN Ordenes o ON o.ID = lm.Ordenes_ID
        WHERE lm.Customers_ID = %s
        ORDER BY lm.Fecha DESC
    """
    return run_select(query, (customer_id,))


from mysql.connector import Error, IntegrityError  # asegúrate de tener ambos importados arriba


def register_loyalty_movement(
    customer_id: int,
    order_id: int | None,
    puntos: int,
    descripcion: str,
) -> tuple[bool, str | None]:
    """
    Registra un movimiento de lealtad usando sp_registrar_movimiento_lealtad.
    Devuelve (ok, mensaje_error).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(
            "sp_registrar_movimiento_lealtad",
            [customer_id, order_id, puntos, descripcion],
        )
        conn.commit()
        return True, None
    except IntegrityError:
        # Error típico de llave foránea: cliente u orden no existen
        return (
            False,
            "No se pudo registrar el movimiento: verifica que el cliente y (si aplica) la orden existan.",
        )
    except Error as e:
        return False, f"Error al ejecutar sp_registrar_movimiento_lealtad: {e}"
    finally:
        cursor.close()
        conn.close()



# -----------------------------------------------------------------------------
# Analytics: vistas genéricas y consultas parametrizadas
# -----------------------------------------------------------------------------

_ALLOWED_VIEWS = {
    "vw_ventas_por_categoria",
    "vw_ticket_promedio_mensual",
    "vw_sla_envios",
    "vw_tasa_devoluciones_mensual",
    "vw_clientes_ltv_alto",
    "vw_inventario_producto_bodega",
    "vw_clientes_por_pais",
    "vw_abc_productos",
}


def get_view_data(view_name: str) -> list[dict]:
    """
    Ejecuta SELECT * sobre una vista permitida.
    Esto sirve para el módulo de Analítica en la web.
    """
    if view_name not in _ALLOWED_VIEWS:
        print("Vista no permitida:", view_name)
        return []

    query = f"SELECT * FROM {view_name}"
    return run_select(query)


def run_sql_with_explain(sql: str, params: tuple | None = None, explain: bool = False) -> list[dict]:
    """
    Ejecuta una consulta arbitraria (para módulo de analítica).
    Si explain=True, ejecuta EXPLAIN <sql> en lugar de la consulta.
    """
    if explain:
        query = "EXPLAIN " + sql
    else:
        query = sql
    return run_select(query, params or ())


# -----------------------------------------------------------------------------
# Audit log
# -----------------------------------------------------------------------------
def get_audit_logs(
    tabla: str | None = None,
    operacion: str | None = None,
    usuario: str | None = None,
    fecha_desde: str | None = None,
    fecha_hasta: str | None = None,
    page: int = 0,
    page_size: int = 20,
) -> list[dict]:
    """
    Obtiene registros del Audit_log con paginación.

    Usa las columnas reales de la tabla Audit_log:
    ID, Fecha_evento, Tabla_afectada, Operación, Registro_ID, Users_ID.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            ID,
            Fecha_evento,
            Tabla_afectada,
            `Operación` AS Operacion,
            Registro_ID,
            Users_ID
        FROM Audit_log
        WHERE 1 = 1
    """
    params: list = []

    # Filtros básicos (opcionales, por si luego los usas en la UI)
    if tabla:
        query += " AND Tabla_afectada = %s"
        params.append(tabla)

    if operacion:
        query += " AND `Operación` = %s"
        params.append(operacion)

    # usuario = Users_ID (por simplicidad lo comparo directo, si quieres LIKE cambia lógica)
    if usuario:
        query += " AND CAST(Users_ID AS CHAR) LIKE %s"
        params.append(f"%{usuario}%")

    if fecha_desde:
        query += " AND Fecha_evento >= %s"
        params.append(fecha_desde)

    if fecha_hasta:
        query += " AND Fecha_evento <= %s"
        params.append(fecha_hasta)

    query += " ORDER BY Fecha_evento DESC LIMIT %s OFFSET %s"
    offset = page * page_size
    params.extend([page_size, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
