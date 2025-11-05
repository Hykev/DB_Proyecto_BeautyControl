USE LootBox;

SET FOREIGN_KEY_CHECKS = 0;


-- PAISES Y CIUDADES PRINCIPALES DE AMERICA


-- Canadá

INSERT INTO Countries (Nombre) VALUES ('Canadá');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Toronto', 1),
('Vancouver', 1),
('Montreal', 1),
('Calgary', 1),
('Ottawa', 1),
('Edmonton', 1),
('Winnipeg', 1),
('Québec', 1),
('Halifax', 1),
('Victoria', 1);


-- Estados Unidos

INSERT INTO Countries (Nombre) VALUES ('Estados Unidos');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('New York', 2),
('Los Angeles', 2),
('Chicago', 2),
('Houston', 2),
('Phoenix', 2),
('Philadelphia', 2),
('San Antonio', 2),
('San Diego', 2),
('Dallas', 2),
('San Jose', 2);


-- México

INSERT INTO Countries (Nombre) VALUES ('México');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Ciudad de México', 3),
('Guadalajara', 3),
('Monterrey', 3),
('Puebla', 3),
('Mérida', 3),
('Tijuana', 3),
('León', 3),
('Cancún', 3),
('Toluca', 3),
('Chihuahua', 3);


-- Guatemala

INSERT INTO Countries (Nombre) VALUES ('Guatemala');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Guatemala City', 4),
('Quetzaltenango', 4),
('Escuintla', 4),
('Cobán', 4),
('Puerto Barrios', 4),
('Huehuetenango', 4),
('Chiquimula', 4),
('Mazatenango', 4),
('Jalapa', 4),
('Antigua Guatemala', 4);


-- Belice

INSERT INTO Countries (Nombre) VALUES ('Belice');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Belmopan', 5),
('Belize City', 5),
('San Ignacio', 5),
('Orange Walk', 5),
('Dangriga', 5),
('Corozal', 5),
('San Pedro', 5),
('Benque Viejo', 5),
('Punta Gorda', 5),
('Placencia', 5);


-- El Salvador

INSERT INTO Countries (Nombre) VALUES ('El Salvador');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('San Salvador', 6),
('Santa Ana', 6),
('San Miguel', 6),
('Soyapango', 6),
('Usulután', 6),
('Santa Tecla', 6),
('Sonsonate', 6),
('Ahuachapán', 6),
('Zacatecoluca', 6),
('La Unión', 6);


-- Honduras

INSERT INTO Countries (Nombre) VALUES ('Honduras');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Tegucigalpa', 7),
('San Pedro Sula', 7),
('La Ceiba', 7),
('Choluteca', 7),
('Comayagua', 7),
('Puerto Cortés', 7),
('El Progreso', 7),
('Danlí', 7),
('Juticalpa', 7),
('Siguatepeque', 7);


-- Nicaragua

INSERT INTO Countries (Nombre) VALUES ('Nicaragua');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Managua', 8),
('León', 8),
('Granada', 8),
('Masaya', 8),
('Estelí', 8),
('Chinandega', 8),
('Matagalpa', 8),
('Jinotega', 8),
('Bluefields', 8),
('Rivas', 8);


-- Costa Rica

INSERT INTO Countries (Nombre) VALUES ('Costa Rica');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('San José', 9),
('Alajuela', 9),
('Cartago', 9),
('Heredia', 9),
('Liberia', 9),
('Puntarenas', 9),
('Limón', 9),
('San Carlos', 9),
('Turrialba', 9),
('Nicoya', 9);


-- Panamá

INSERT INTO Countries (Nombre) VALUES ('Panamá');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Ciudad de Panamá', 10),
('Colón', 10),
('David', 10),
('Santiago', 10),
('Penonomé', 10),
('Chitré', 10),
('La Chorrera', 10),
('Las Tablas', 10),
('Aguadulce', 10),
('Boquete', 10);


-- Cuba

INSERT INTO Countries (Nombre) VALUES ('Cuba');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('La Habana', 11),
('Santiago de Cuba', 11),
('Camagüey', 11),
('Holguín', 11),
('Santa Clara', 11),
('Guantánamo', 11),
('Bayamo', 11),
('Cienfuegos', 11),
('Pinar del Río', 11),
('Matanzas', 11);


-- República Dominicana

INSERT INTO Countries (Nombre) VALUES ('República Dominicana');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Santo Domingo', 12),
('Santiago', 12),
('La Romana', 12),
('San Pedro de Macorís', 12),
('San Cristóbal', 12),
('Puerto Plata', 12),
('La Vega', 12),
('Higüey', 12),
('Bonao', 12),
('Moca', 12);


-- Colombia

INSERT INTO Countries (Nombre) VALUES ('Colombia');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Bogotá', 13),
('Medellín', 13),
('Cali', 13),
('Barranquilla', 13),
('Cartagena', 13),
('Cúcuta', 13),
('Bucaramanga', 13),
('Ibagué', 13),
('Pereira', 13),
('Santa Marta', 13);


-- Venezuela

INSERT INTO Countries (Nombre) VALUES ('Venezuela');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Caracas', 14),
('Maracaibo', 14),
('Valencia', 14),
('Barquisimeto', 14),
('Maracay', 14),
('Maturín', 14),
('Barcelona', 14),
('Ciudad Guayana', 14),
('Cumaná', 14),
('San Cristóbal', 14);


-- Ecuador

INSERT INTO Countries (Nombre) VALUES ('Ecuador');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Quito', 15),
('Guayaquil', 15),
('Cuenca', 15),
('Ambato', 15),
('Manta', 15),
('Portoviejo', 15),
('Machala', 15),
('Loja', 15),
('Riobamba', 15),
('Ibarra', 15);


-- Perú

INSERT INTO Countries (Nombre) VALUES ('Perú');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Lima', 16),
('Arequipa', 16),
('Trujillo', 16),
('Chiclayo', 16),
('Piura', 16),
('Cusco', 16),
('Huancayo', 16),
('Iquitos', 16),
('Tacna', 16),
('Puno', 16);


-- Bolivia

INSERT INTO Countries (Nombre) VALUES ('Bolivia');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('La Paz', 17),
('Santa Cruz de la Sierra', 17),
('Cochabamba', 17),
('Sucre', 17),
('Oruro', 17),
('Potosí', 17),
('Tarija', 17),
('Trinidad', 17),
('Cobija', 17),
('El Alto', 17);


-- Brasil

INSERT INTO Countries (Nombre) VALUES ('Brasil');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('São Paulo', 18),
('Rio de Janeiro', 18),
('Brasilia', 18),
('Salvador', 18),
('Fortaleza', 18),
('Belo Horizonte', 18),
('Curitiba', 18),
('Manaus', 18),
('Recife', 18),
('Porto Alegre', 18);


-- Chile

INSERT INTO Countries (Nombre) VALUES ('Chile');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Santiago', 19),
('Valparaíso', 19),
('Concepción', 19),
('La Serena', 19),
('Antofagasta', 19),
('Temuco', 19),
('Iquique', 19),
('Rancagua', 19),
('Talca', 19),
('Puerto Montt', 19);


-- Argentina

INSERT INTO Countries (Nombre) VALUES ('Argentina');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Buenos Aires', 20),
('Córdoba', 20),
('Rosario', 20),
('Mendoza', 20),
('La Plata', 20),
('Mar del Plata', 20),
('Salta', 20),
('San Miguel de Tucumán', 20),
('Santa Fe', 20),
('Neuquén', 20);


-- Paraguay

INSERT INTO Countries (Nombre) VALUES ('Paraguay');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Asunción', 21),
('Ciudad del Este', 21),
('Encarnación', 21),
('Pedro Juan Caballero', 21),
('Concepción', 21),
('Villarrica', 21),
('Coronel Oviedo', 21),
('Caaguazú', 21),
('Itauguá', 21),
('San Lorenzo', 21);


-- Uruguay

INSERT INTO Countries (Nombre) VALUES ('Uruguay');
INSERT INTO Cities (Nombre, Countries_ID) VALUES
('Montevideo', 22),
('Salto', 22),
('Paysandú', 22),
('Las Piedras', 22),
('Rivera', 22),
('Maldonado', 22),
('Tacuarembó', 22),
('Canelones', 22),
('San José de Mayo', 22),
('Durazno', 22);


SET FOREIGN_KEY_CHECKS = 1;