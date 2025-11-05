# =========================================================
# GENERADOR DE PAISES Y CIUDADES PRINCIPALES DE AMERICA
# =========================================================
OUTPUT_FILE = "SQL_DB_Template/seed_countries_cities.sql"

# Lista simplificada: países del continente americano con sus principales ciudades
countries_cities = {
    "Canadá": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Winnipeg", "Québec", "Halifax", "Victoria"],
    "Estados Unidos": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
    "México": ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Mérida", "Tijuana", "León", "Cancún", "Toluca", "Chihuahua"],
    "Guatemala": ["Guatemala City", "Quetzaltenango", "Escuintla", "Cobán", "Puerto Barrios", "Huehuetenango", "Chiquimula", "Mazatenango", "Jalapa", "Antigua Guatemala"],
    "Belice": ["Belmopan", "Belize City", "San Ignacio", "Orange Walk", "Dangriga", "Corozal", "San Pedro", "Benque Viejo", "Punta Gorda", "Placencia"],
    "El Salvador": ["San Salvador", "Santa Ana", "San Miguel", "Soyapango", "Usulután", "Santa Tecla", "Sonsonate", "Ahuachapán", "Zacatecoluca", "La Unión"],
    "Honduras": ["Tegucigalpa", "San Pedro Sula", "La Ceiba", "Choluteca", "Comayagua", "Puerto Cortés", "El Progreso", "Danlí", "Juticalpa", "Siguatepeque"],
    "Nicaragua": ["Managua", "León", "Granada", "Masaya", "Estelí", "Chinandega", "Matagalpa", "Jinotega", "Bluefields", "Rivas"],
    "Costa Rica": ["San José", "Alajuela", "Cartago", "Heredia", "Liberia", "Puntarenas", "Limón", "San Carlos", "Turrialba", "Nicoya"],
    "Panamá": ["Ciudad de Panamá", "Colón", "David", "Santiago", "Penonomé", "Chitré", "La Chorrera", "Las Tablas", "Aguadulce", "Boquete"],
    "Cuba": ["La Habana", "Santiago de Cuba", "Camagüey", "Holguín", "Santa Clara", "Guantánamo", "Bayamo", "Cienfuegos", "Pinar del Río", "Matanzas"],
    "República Dominicana": ["Santo Domingo", "Santiago", "La Romana", "San Pedro de Macorís", "San Cristóbal", "Puerto Plata", "La Vega", "Higüey", "Bonao", "Moca"],
    "Colombia": ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Cúcuta", "Bucaramanga", "Ibagué", "Pereira", "Santa Marta"],
    "Venezuela": ["Caracas", "Maracaibo", "Valencia", "Barquisimeto", "Maracay", "Maturín", "Barcelona", "Ciudad Guayana", "Cumaná", "San Cristóbal"],
    "Ecuador": ["Quito", "Guayaquil", "Cuenca", "Ambato", "Manta", "Portoviejo", "Machala", "Loja", "Riobamba", "Ibarra"],
    "Perú": ["Lima", "Arequipa", "Trujillo", "Chiclayo", "Piura", "Cusco", "Huancayo", "Iquitos", "Tacna", "Puno"],
    "Bolivia": ["La Paz", "Santa Cruz de la Sierra", "Cochabamba", "Sucre", "Oruro", "Potosí", "Tarija", "Trinidad", "Cobija", "El Alto"],
    "Brasil": ["São Paulo", "Rio de Janeiro", "Brasilia", "Salvador", "Fortaleza", "Belo Horizonte", "Curitiba", "Manaus", "Recife", "Porto Alegre"],
    "Chile": ["Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta", "Temuco", "Iquique", "Rancagua", "Talca", "Puerto Montt"],
    "Argentina": ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata", "Mar del Plata", "Salta", "San Miguel de Tucumán", "Santa Fe", "Neuquén"],
    "Paraguay": ["Asunción", "Ciudad del Este", "Encarnación", "Pedro Juan Caballero", "Concepción", "Villarrica", "Coronel Oviedo", "Caaguazú", "Itauguá", "San Lorenzo"],
    "Uruguay": ["Montevideo", "Salto", "Paysandú", "Las Piedras", "Rivera", "Maldonado", "Tacuarembó", "Canelones", "San José de Mayo", "Durazno"]
}

# =========================================================
# GENERACIÓN DEL SQL AGRUPADO
# =========================================================
sql_lines = []
sql_lines.append("USE LootBox;\n")
sql_lines.append("SET FOREIGN_KEY_CHECKS = 0;\n\n")
sql_lines.append("-- PAISES Y CIUDADES PRINCIPALES DE AMERICA\n")

country_id = 1
for country, cities in countries_cities.items():
    sql_lines.append(f"\n-- {country}\n")
    sql_lines.append(f"INSERT INTO Countries (Nombre) VALUES ('{country}');")
    city_values = ",\n".join([f"('{city}', {country_id})" for city in cities])
    sql_lines.append(f"INSERT INTO Cities (Nombre, Countries_ID) VALUES\n{city_values};\n")
    country_id += 1

sql_lines.append("\nSET FOREIGN_KEY_CHECKS = 1;")

# =========================================================
# GUARDAR ARCHIVO
# =========================================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(sql_lines))

print(f"✅ Archivo '{OUTPUT_FILE}' generado con {len(countries_cities)} países y {len(countries_cities)*10} ciudades principales.")
