-- LootBox_extras.sql
USE `LootBox`;

-- =========================
-- 1) ÍNDICES COMPUESTOS
-- =========================

-- 1. Órdenes por cliente y fecha
CREATE INDEX idx_Ordenes_customer_fecha
ON `Ordenes` (`Customers_ID`, `Fecha de la orden`);

-- 2. Órdenes por status y fecha
CREATE INDEX idx_Ordenes_status_fecha
ON `Ordenes` (`Status`, `Fecha de la orden`);

-- 3. Items por orden y producto
CREATE INDEX idx_Order_items_orden_producto
ON `Order_items` (`Ordenes_ID`, `Products_ID`);

-- 4. Movimientos por bodega y fecha
CREATE INDEX idx_inventory_movements_warehouse_fecha
ON `inventory_movements` (`Warehouses_ID`, `Fecha del movimiento`);

-- 5. Movimientos por producto y fecha
CREATE INDEX idx_inventory_movements_producto_fecha
ON `inventory_movements` (`Products_ID`, `Fecha del movimiento`);

-- 6. Envíos por bodega y fecha de envío
CREATE INDEX idx_Shipments_warehouse_fecha_envio
ON `Shipments` (`Warehouses_ID`, `Fecha de envio`);

-- 7. Movimientos de lealtad por cliente y fecha
CREATE INDEX idx_Loyalty_customer_fecha
ON `Loyalty_movements` (`Customers_ID`, `Fecha`);


-- =========================
-- 2) ÍNDICES SOBRE EXPRESIONES
-- =========================

-- Búsqueda case-insensitive de email en Customers
CREATE INDEX idx_Customers_email_lower
ON `Customers` ((LOWER(`Email`)));

-- Búsqueda case-insensitive de email en Users
CREATE INDEX idx_Users_email_lower
ON `Users` ((LOWER(`Email`)));


-- =========================
-- 3) VISTAS (≥ 8)
-- =========================

-- 1) Ventas por categoría
CREATE OR REPLACE VIEW vw_ventas_por_categoria AS
SELECT
  c.ID AS categoria_id,
  c.Nombre AS categoria_nombre,
  SUM(oi.`Cantidad` * oi.`Precio por unidad`) AS total_ventas
FROM Categories c
JOIN Products p ON p.Categories_ID = c.ID
JOIN Order_items oi ON oi.Products_ID = p.ID
JOIN Ordenes o ON o.ID = oi.Ordenes_ID
GROUP BY c.ID, c.Nombre;

-- 2) Ticket promedio mensual
CREATE OR REPLACE VIEW vw_ticket_promedio_mensual AS
SELECT
  YEAR(o.`Fecha de la orden`) AS anio,
  MONTH(o.`Fecha de la orden`) AS mes,
  AVG(o.`Total`) AS ticket_promedio
FROM Ordenes o
GROUP BY YEAR(o.`Fecha de la orden`), MONTH(o.`Fecha de la orden`);

-- 3) SLA de envíos (días entre envío y entrega)
CREATE OR REPLACE VIEW vw_sla_envios AS
SELECT
  s.ID AS shipment_id,
  w.Nombre AS bodega,
  DATEDIFF(s.`Fecha de entrega`, s.`Fecha de envio`) AS dias_entrega,
  s.Status
FROM Shipments s
JOIN Warehouses w ON w.ID = s.Warehouses_ID;

-- 4) Tasa de devoluciones por mes
CREATE OR REPLACE VIEW vw_tasa_devoluciones_mensual AS
SELECT
  anio,
  mes,
  total_ordenes,
  total_devoluciones,
  CASE 
    WHEN total_ordenes = 0 THEN 0
    ELSE total_devoluciones / total_ordenes
  END AS tasa_devolucion
FROM (
  SELECT
    YEAR(o.`Fecha de la orden`) AS anio,
    MONTH(o.`Fecha de la orden`) AS mes,
    COUNT(DISTINCT o.ID) AS total_ordenes,
    COUNT(DISTINCT d.ID) AS total_devoluciones
  FROM Ordenes o
  LEFT JOIN Devoluciones d ON d.Ordenes_ID = o.ID
  GROUP BY YEAR(o.`Fecha de la orden`), MONTH(o.`Fecha de la orden`)
) t;

-- 5) Clientes con LTV alto (Lifetime Value)
CREATE OR REPLACE VIEW vw_clientes_ltv_alto AS
SELECT
  c.ID AS customer_id,
  c.Nombre,
  c.Apellido,
  SUM(o.`Total`) AS ltv
FROM Customers c
JOIN Ordenes o ON o.Customers_ID = c.ID
GROUP BY c.ID, c.Nombre, c.Apellido
HAVING ltv >= 1000;  -- umbral ajustable

-- 6) Inventario actual por producto y bodega
CREATE OR REPLACE VIEW vw_inventario_producto_bodega AS
SELECT
  p.ID AS product_id,
  p.`Nombre del producto`,
  w.ID AS warehouse_id,
  w.Nombre AS warehouse_nombre,
  SUM(
    CASE 
      WHEN im.`Tipo de movimiento` = 'IN' THEN im.Cantidad
      ELSE -im.Cantidad
    END
  ) AS stock_actual
FROM inventory_movements im
JOIN Products p ON p.ID = im.Products_ID
JOIN Warehouses w ON w.ID = im.Warehouses_ID
GROUP BY p.ID, p.`Nombre del producto`, w.ID, w.Nombre;

-- 7) Clientes por país (clientes multipaís a nivel de reporte)
CREATE OR REPLACE VIEW vw_clientes_por_pais AS
SELECT
  co.ID AS country_id,
  co.Nombre AS country_nombre,
  COUNT(cu.ID) AS total_clientes
FROM Countries co
JOIN Cities ci ON ci.Countries_ID = co.ID
JOIN Customers cu ON cu.Cities_ID = ci.ID
GROUP BY co.ID, co.Nombre;

-- 8) ABC de productos (clasificación por ventas acumuladas)
CREATE OR REPLACE VIEW vw_abc_productos AS
WITH ventas AS (
  SELECT
    p.ID AS product_id,
    p.`Nombre del producto`,
    SUM(oi.`Cantidad` * oi.`Precio por unidad`) AS total_ventas
  FROM Products p
  JOIN Order_items oi ON oi.Products_ID = p.ID
  JOIN Ordenes o ON o.ID = oi.Ordenes_ID
  GROUP BY p.ID, p.`Nombre del producto`
),
ordenado AS (
  SELECT
    v.*,
    SUM(v.total_ventas) OVER (ORDER BY v.total_ventas DESC) AS acumulado,
    SUM(v.total_ventas) OVER () AS total_general
  FROM ventas v
)
SELECT
  product_id,
  `Nombre del producto`,
  total_ventas,
  acumulado,
  total_general,
  CASE
    WHEN acumulado / total_general <= 0.80 THEN 'A'
    WHEN acumulado / total_general <= 0.95 THEN 'B'
    ELSE 'C'
  END AS categoria_abc
FROM ordenado;


-- =========================
-- 4) STORED PROCEDURES (5)
-- =========================

DELIMITER $$

-- 1) Crear una orden simple (pago + envío + orden)
CREATE PROCEDURE sp_crear_orden_simple (
  IN p_customer_id INT,
  IN p_empleado_id INT,
  IN p_warehouse_id INT,
  IN p_total DECIMAL(10,2),
  IN p_metodo_pago VARCHAR(20)
)
BEGIN
  DECLARE v_payment_id INT;
  DECLARE v_shipment_id INT;

  INSERT INTO Payments (`Fecha de pago`, `Método de  pago`, `Cantidad`, `Customers_ID`)
  VALUES (NOW(), p_metodo_pago, p_total, p_customer_id);
  SET v_payment_id = LAST_INSERT_ID();

  INSERT INTO Shipments (`Fecha de envio`, `Fecha de entrega`, `Status`, `Warehouses_ID`)
  VALUES (NOW(), NOW(), 'EN TRANSITO', p_warehouse_id);
  SET v_shipment_id = LAST_INSERT_ID();

  INSERT INTO Ordenes (`Fecha de la orden`, `Status`, `Total`, `Payments_ID`, `Customers_ID`, `Employees_ID`, `Shipments_ID`)
  VALUES (NOW(), 'PENDIENTE', p_total, v_payment_id, p_customer_id, p_empleado_id, v_shipment_id);
END$$


-- 2) Obtener órdenes de un cliente
CREATE PROCEDURE sp_obtener_ordenes_cliente (
  IN p_customer_id INT
)
BEGIN
  SELECT
    o.ID,
    o.`Fecha de la orden`,
    o.Status,
    o.Total
  FROM Ordenes o
  WHERE o.Customers_ID = p_customer_id
  ORDER BY o.`Fecha de la orden` DESC;
END$$


-- 3) Registrar un movimiento de inventario
CREATE PROCEDURE sp_registrar_movimiento_inventario (
  IN p_product_id INT,
  IN p_warehouse_id INT,
  IN p_empleado_id INT,
  IN p_cantidad INT,
  IN p_tipo ENUM('IN','OUT')
)
BEGIN
  INSERT INTO inventory_movements (
    `Products_ID`,
    `Warehouses_ID`,
    `Cantidad`,
    `Tipo de movimiento`,
    `Fecha del movimiento`,
    `Employees_ID`
  )
  VALUES (
    p_product_id,
    p_warehouse_id,
    p_cantidad,
    p_tipo,
    NOW(),
    p_empleado_id
  );
END$$


-- 4) Calcular stock de un producto en una bodega
CREATE PROCEDURE sp_calcular_stock_producto_bodega (
  IN p_product_id INT,
  IN p_warehouse_id INT
)
BEGIN
  SELECT
    p.ID AS product_id,
    p.`Nombre del producto`,
    w.ID AS warehouse_id,
    w.Nombre AS warehouse_nombre,
    COALESCE(SUM(
      CASE 
        WHEN im.`Tipo de movimiento` = 'IN' THEN im.Cantidad
        ELSE -im.Cantidad
      END
    ), 0) AS stock_actual
  FROM Products p
  JOIN inventory_movements im
    ON im.Products_ID = p.ID
   AND im.Warehouses_ID = p_warehouse_id
  JOIN Warehouses w
    ON w.ID = im.Warehouses_ID
  WHERE p.ID = p_product_id
  GROUP BY p.ID, p.`Nombre del producto`, w.ID, w.Nombre;
END$$


-- 5) Registrar movimiento de lealtad (puntos)
CREATE PROCEDURE sp_registrar_movimiento_lealtad (
  IN p_customer_id INT,
  IN p_orden_id INT,
  IN p_puntos INT,
  IN p_descripcion VARCHAR(500)
)
BEGIN
  INSERT INTO Loyalty_movements (
    `Fecha`,
    `Puntos_cambio`,
    `Descripción`,
    `Customers_ID`,
    `Ordenes_ID`
  )
  VALUES (
    NOW(),
    p_puntos,
    p_descripcion,
    p_customer_id,
    p_orden_id
  );
END$$

DELIMITER ;
