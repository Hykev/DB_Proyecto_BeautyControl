USE LootBox;

SET FOREIGN_KEY_CHECKS = 0;


-- PAISES Y CIUDADES PRINCIPALES DE AMERICA


-- Canadá

INSERT INTO Countries (Nombre) VALUES ('Canadá');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Toronto', @country_id),
('Vancouver', @country_id),
('Montreal', @country_id),
('Calgary', @country_id),
('Ottawa', @country_id),
('Edmonton', @country_id),
('Winnipeg', @country_id),
('Québec', @country_id),
('Halifax', @country_id),
('Victoria', @country_id);


-- Estados Unidos

INSERT INTO Countries (Nombre) VALUES ('Estados Unidos');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('New York', @country_id),
('Los Angeles', @country_id),
('Chicago', @country_id),
('Houston', @country_id),
('Phoenix', @country_id),
('Philadelphia', @country_id),
('San Antonio', @country_id),
('San Diego', @country_id),
('Dallas', @country_id),
('San Jose', @country_id);


-- México

INSERT INTO Countries (Nombre) VALUES ('México');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Ciudad de México', @country_id),
('Guadalajara', @country_id),
('Monterrey', @country_id),
('Puebla', @country_id),
('Mérida', @country_id),
('Tijuana', @country_id),
('León', @country_id),
('Cancún', @country_id),
('Toluca', @country_id),
('Chihuahua', @country_id);


-- Guatemala

INSERT INTO Countries (Nombre) VALUES ('Guatemala');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Guatemala City', @country_id),
('Quetzaltenango', @country_id),
('Escuintla', @country_id),
('Cobán', @country_id),
('Puerto Barrios', @country_id),
('Huehuetenango', @country_id),
('Chiquimula', @country_id),
('Mazatenango', @country_id),
('Jalapa', @country_id),
('Antigua Guatemala', @country_id);


-- Belice

INSERT INTO Countries (Nombre) VALUES ('Belice');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Belmopan', @country_id),
('Belize City', @country_id),
('San Ignacio', @country_id),
('Orange Walk', @country_id),
('Dangriga', @country_id),
('Corozal', @country_id),
('San Pedro', @country_id),
('Benque Viejo', @country_id),
('Punta Gorda', @country_id),
('Placencia', @country_id);


-- El Salvador

INSERT INTO Countries (Nombre) VALUES ('El Salvador');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('San Salvador', @country_id),
('Santa Ana', @country_id),
('San Miguel', @country_id),
('Soyapango', @country_id),
('Usulután', @country_id),
('Santa Tecla', @country_id),
('Sonsonate', @country_id),
('Ahuachapán', @country_id),
('Zacatecoluca', @country_id),
('La Unión', @country_id);


-- Honduras

INSERT INTO Countries (Nombre) VALUES ('Honduras');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Tegucigalpa', @country_id),
('San Pedro Sula', @country_id),
('La Ceiba', @country_id),
('Choluteca', @country_id),
('Comayagua', @country_id),
('Puerto Cortés', @country_id),
('El Progreso', @country_id),
('Danlí', @country_id),
('Juticalpa', @country_id),
('Siguatepeque', @country_id);


-- Nicaragua

INSERT INTO Countries (Nombre) VALUES ('Nicaragua');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Managua', @country_id),
('León', @country_id),
('Granada', @country_id),
('Masaya', @country_id),
('Estelí', @country_id),
('Chinandega', @country_id),
('Matagalpa', @country_id),
('Jinotega', @country_id),
('Bluefields', @country_id),
('Rivas', @country_id);


-- Costa Rica

INSERT INTO Countries (Nombre) VALUES ('Costa Rica');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('San José', @country_id),
('Alajuela', @country_id),
('Cartago', @country_id),
('Heredia', @country_id),
('Liberia', @country_id),
('Puntarenas', @country_id),
('Limón', @country_id),
('San Carlos', @country_id),
('Turrialba', @country_id),
('Nicoya', @country_id);


-- Panamá

INSERT INTO Countries (Nombre) VALUES ('Panamá');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Ciudad de Panamá', @country_id),
('Colón', @country_id),
('David', @country_id),
('Santiago', @country_id),
('Penonomé', @country_id),
('Chitré', @country_id),
('La Chorrera', @country_id),
('Las Tablas', @country_id),
('Aguadulce', @country_id),
('Boquete', @country_id);


-- Cuba

INSERT INTO Countries (Nombre) VALUES ('Cuba');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('La Habana', @country_id),
('Santiago de Cuba', @country_id),
('Camagüey', @country_id),
('Holguín', @country_id),
('Santa Clara', @country_id),
('Guantánamo', @country_id),
('Bayamo', @country_id),
('Cienfuegos', @country_id),
('Pinar del Río', @country_id),
('Matanzas', @country_id);


-- República Dominicana

INSERT INTO Countries (Nombre) VALUES ('República Dominicana');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Santo Domingo', @country_id),
('Santiago', @country_id),
('La Romana', @country_id),
('San Pedro de Macorís', @country_id),
('San Cristóbal', @country_id),
('Puerto Plata', @country_id),
('La Vega', @country_id),
('Higüey', @country_id),
('Bonao', @country_id),
('Moca', @country_id);


-- Colombia

INSERT INTO Countries (Nombre) VALUES ('Colombia');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Bogotá', @country_id),
('Medellín', @country_id),
('Cali', @country_id),
('Barranquilla', @country_id),
('Cartagena', @country_id),
('Cúcuta', @country_id),
('Bucaramanga', @country_id),
('Ibagué', @country_id),
('Pereira', @country_id),
('Santa Marta', @country_id);


-- Venezuela

INSERT INTO Countries (Nombre) VALUES ('Venezuela');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Caracas', @country_id),
('Maracaibo', @country_id),
('Valencia', @country_id),
('Barquisimeto', @country_id),
('Maracay', @country_id),
('Maturín', @country_id),
('Barcelona', @country_id),
('Ciudad Guayana', @country_id),
('Cumaná', @country_id),
('San Cristóbal', @country_id);


-- Ecuador

INSERT INTO Countries (Nombre) VALUES ('Ecuador');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Quito', @country_id),
('Guayaquil', @country_id),
('Cuenca', @country_id),
('Ambato', @country_id),
('Manta', @country_id),
('Portoviejo', @country_id),
('Machala', @country_id),
('Loja', @country_id),
('Riobamba', @country_id),
('Ibarra', @country_id);


-- Perú

INSERT INTO Countries (Nombre) VALUES ('Perú');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Lima', @country_id),
('Arequipa', @country_id),
('Trujillo', @country_id),
('Chiclayo', @country_id),
('Piura', @country_id),
('Cusco', @country_id),
('Huancayo', @country_id),
('Iquitos', @country_id),
('Tacna', @country_id),
('Puno', @country_id);


-- Bolivia

INSERT INTO Countries (Nombre) VALUES ('Bolivia');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('La Paz', @country_id),
('Santa Cruz de la Sierra', @country_id),
('Cochabamba', @country_id),
('Sucre', @country_id),
('Oruro', @country_id),
('Potosí', @country_id),
('Tarija', @country_id),
('Trinidad', @country_id),
('Cobija', @country_id),
('El Alto', @country_id);


-- Brasil

INSERT INTO Countries (Nombre) VALUES ('Brasil');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('São Paulo', @country_id),
('Rio de Janeiro', @country_id),
('Brasilia', @country_id),
('Salvador', @country_id),
('Fortaleza', @country_id),
('Belo Horizonte', @country_id),
('Curitiba', @country_id),
('Manaus', @country_id),
('Recife', @country_id),
('Porto Alegre', @country_id);


-- Chile

INSERT INTO Countries (Nombre) VALUES ('Chile');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Santiago', @country_id),
('Valparaíso', @country_id),
('Concepción', @country_id),
('La Serena', @country_id),
('Antofagasta', @country_id),
('Temuco', @country_id),
('Iquique', @country_id),
('Rancagua', @country_id),
('Talca', @country_id),
('Puerto Montt', @country_id);


-- Argentina

INSERT INTO Countries (Nombre) VALUES ('Argentina');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Buenos Aires', @country_id),
('Córdoba', @country_id),
('Rosario', @country_id),
('Mendoza', @country_id),
('La Plata', @country_id),
('Mar del Plata', @country_id),
('Salta', @country_id),
('San Miguel de Tucumán', @country_id),
('Santa Fe', @country_id),
('Neuquén', @country_id);


-- Paraguay

INSERT INTO Countries (Nombre) VALUES ('Paraguay');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Asunción', @country_id),
('Ciudad del Este', @country_id),
('Encarnación', @country_id),
('Pedro Juan Caballero', @country_id),
('Concepción', @country_id),
('Villarrica', @country_id),
('Coronel Oviedo', @country_id),
('Caaguazú', @country_id),
('Itauguá', @country_id),
('San Lorenzo', @country_id);


-- Uruguay

INSERT INTO Countries (Nombre) VALUES ('Uruguay');
SET @country_id = LAST_INSERT_ID();
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Montevideo', @country_id),
('Salto', @country_id),
('Paysandú', @country_id),
('Las Piedras', @country_id),
('Rivera', @country_id),
('Maldonado', @country_id),
('Tacuarembó', @country_id),
('Canelones', @country_id),
('San José de Mayo', @country_id),
('Durazno', @country_id);


SET FOREIGN_KEY_CHECKS = 1;