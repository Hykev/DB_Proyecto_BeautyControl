import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",             # ← tu usuario
    "password": "123456",  # ← tu contraseña (si no tiene, pon "")
    "database": "BeautyControl",  # ← el nombre exacto del schema
    "port": 3306,               # puerto por defecto de MySQL
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_customers(limit=20, offset=0):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM customers LIMIT %s OFFSET %s"
    cursor.execute(query, (limit, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def seed_cities():
    """Crea algunos Countries y Cities de ejemplo si las tablas están vacías."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1) Verificar si hay países
        cursor.execute("SELECT COUNT(*) FROM Countries")
        (count_countries,) = cursor.fetchone()

        if count_countries == 0:
            countries = [
                ("Guatemala",),
                ("México",),
                ("El Salvador",),
            ]
            cursor.executemany(
                "INSERT INTO Countries (Nombre) VALUES (%s)",
                countries,
            )
            conn.commit()

        # 2) Traer IDs de los países
        cursor.execute("SELECT ID, Nombre FROM Countries")
        country_rows = cursor.fetchall()
        country_map = {name: cid for (cid, name) in country_rows}

        # 3) Verificar si hay ciudades
        cursor.execute("SELECT COUNT(*) FROM Cities")
        (count_cities,) = cursor.fetchone()

        if count_cities == 0:
            cities = [
                ("Ciudad de Guatemala", country_map.get("Guatemala")),
                ("Antigua Guatemala", country_map.get("Guatemala")),
                ("Ciudad de México", country_map.get("México")),
                ("San Salvador", country_map.get("El Salvador")),
            ]

            # Filtramos por si algún país no existiera
            cities = [c for c in cities if c[1] is not None]

            cursor.executemany(
                "INSERT INTO Cities (Nombre, Countries_ID) VALUES (%s, %s)",
                cities,
            )
            conn.commit()

        return True

    except Error as e:
        print("Error al crear datos de Cities:", e)
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()