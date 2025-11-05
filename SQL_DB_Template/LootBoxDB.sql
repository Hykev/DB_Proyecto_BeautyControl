-- LootBox_schema.sql
-- Esquema principal: tablas, PKs y FKs

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema LootBox
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `LootBox` DEFAULT CHARACTER SET utf8 ;
USE `LootBox` ;

-- -----------------------------------------------------
-- Table Countries
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Countries` ;

CREATE TABLE IF NOT EXISTS `Countries` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Cities
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Cities` ;

CREATE TABLE IF NOT EXISTS `Cities` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NOT NULL,
  `Countries_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Cities_Countries_idx` (`Countries_ID` ASC),
  CONSTRAINT `fk_Cities_Countries`
    FOREIGN KEY (`Countries_ID`)
    REFERENCES `Countries` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Customers
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Customers` ;

CREATE TABLE IF NOT EXISTS `Customers` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NOT NULL,
  `Apellido` VARCHAR(100) NOT NULL,
  `Email` VARCHAR(100) NULL,
  `Teléfono` VARCHAR(20) NOT NULL,
  `Dirección` VARCHAR(1000) NOT NULL,
  `Fecha de creación` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `Cities_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Customers_Cities1_idx` (`Cities_ID` ASC),
  CONSTRAINT `fk_Customers_Cities1`
    FOREIGN KEY (`Cities_ID`)
    REFERENCES `Cities` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Suppliers
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Suppliers` ;

CREATE TABLE IF NOT EXISTS `Suppliers` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre de proveedor` VARCHAR(150) NOT NULL,
  `Nombre de contacto` VARCHAR(100) NOT NULL,
  `Email` VARCHAR(100) NOT NULL,
  `Teléfono` VARCHAR(20) NOT NULL,
  `Countries_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Suppliers_Countries1_idx` (`Countries_ID` ASC),
  CONSTRAINT `fk_Suppliers_Countries1`
    FOREIGN KEY (`Countries_ID`)
    REFERENCES `Countries` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Categories
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Categories` ;

CREATE TABLE IF NOT EXISTS `Categories` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NOT NULL,
  `Descripción` VARCHAR(500) NULL,
  PRIMARY KEY (`ID`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Products
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Products` ;

CREATE TABLE IF NOT EXISTS `Products` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre del producto` VARCHAR(150) NOT NULL,
  `Precio` DECIMAL(10,2) NOT NULL,
  `Fecha de creación` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Categories_ID` INT NOT NULL,
  `Suppliers_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Products_Categories1_idx` (`Categories_ID` ASC),
  INDEX `fk_Products_Suppliers1_idx` (`Suppliers_ID` ASC),
  CONSTRAINT `fk_Products_Categories1`
    FOREIGN KEY (`Categories_ID`)
    REFERENCES `Categories` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_Suppliers1`
    FOREIGN KEY (`Suppliers_ID`)
    REFERENCES `Suppliers` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Warehouses
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Warehouses` ;

CREATE TABLE IF NOT EXISTS `Warehouses` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NOT NULL,
  `Dirección` VARCHAR(150) NOT NULL,
  `Cities_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Warehouses_Cities1_idx` (`Cities_ID` ASC),
  CONSTRAINT `fk_Warehouses_Cities1`
    FOREIGN KEY (`Cities_ID`)
    REFERENCES `Cities` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Payments
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Payments` ;

CREATE TABLE IF NOT EXISTS `Payments` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Fecha de pago` DATETIME NOT NULL,
  `Método de  pago` ENUM('EFECTIVO', 'TARJETA', 'TRANSFERENCIA') NOT NULL,
  `Cantidad` DECIMAL(10,2) NOT NULL,
  `Customers_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Payments_Customers_idx` (`Customers_ID` ASC),
  CONSTRAINT `fk_Payments_Customers`
    FOREIGN KEY (`Customers_ID`)
    REFERENCES `Customers` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Users
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Users` ;

CREATE TABLE IF NOT EXISTS `Users` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre de usuario` VARCHAR(50) NOT NULL,
  `Email` VARCHAR(100) NOT NULL,
  `Contraseña` VARCHAR(255) NOT NULL,
  `Rol` ENUM('cliente', 'empleado', 'admin') NOT NULL,
  `Creado` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Actualizado` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Estado` ENUM('activo', 'inactivo') NOT NULL,
  `Customers_ID` INT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Users_Customers1_idx` (`Customers_ID` ASC),
  CONSTRAINT `fk_Users_Customers1`
    FOREIGN KEY (`Customers_ID`)
    REFERENCES `Customers` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Employees
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Employees` ;

CREATE TABLE IF NOT EXISTS `Employees` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(45) NOT NULL,
  `Apellido` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Teléfono` VARCHAR(45) NOT NULL,
  `Rol` VARCHAR(45) NOT NULL,
  `Users_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Employees_Users1_idx` (`Users_ID` ASC),
  CONSTRAINT `fk_Employees_Users1`
    FOREIGN KEY (`Users_ID`)
    REFERENCES `Users` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Shipments
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Shipments` ;

CREATE TABLE IF NOT EXISTS `Shipments` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Fecha de envio` DATETIME NOT NULL,
  `Fecha de entrega` DATETIME NOT NULL,
  `Status` ENUM('EN TRANSITO', 'ENTREGADO', 'RETRASADO') NOT NULL,
  `Warehouses_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Shipments_Warehouses1_idx` (`Warehouses_ID` ASC),
  CONSTRAINT `fk_Shipments_Warehouses1`
    FOREIGN KEY (`Warehouses_ID`)
    REFERENCES `Warehouses` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Ordenes
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Ordenes` ;

CREATE TABLE IF NOT EXISTS `Ordenes` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Fecha de la orden` DATETIME NOT NULL,
  `Status` ENUM('PENDIENTE', 'ENVIADO', 'ENTREGADO', 'REGRESADO') NOT NULL,
  `Total` DECIMAL(10,2) NOT NULL,
  `Payments_ID` INT NOT NULL,
  `Customers_ID` INT NOT NULL,
  `Employees_ID` INT NOT NULL,
  `Shipments_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Ordenes_Payments1_idx` (`Payments_ID` ASC),
  INDEX `fk_Ordenes_Customers1_idx` (`Customers_ID` ASC),
  INDEX `fk_Ordenes_Employees1_idx` (`Employees_ID` ASC),
  INDEX `fk_Ordenes_Shipments1_idx` (`Shipments_ID` ASC),
  CONSTRAINT `fk_Ordenes_Payments1`
    FOREIGN KEY (`Payments_ID`)
    REFERENCES `Payments` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ordenes_Customers1`
    FOREIGN KEY (`Customers_ID`)
    REFERENCES `Customers` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ordenes_Employees1`
    FOREIGN KEY (`Employees_ID`)
    REFERENCES `Employees` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ordenes_Shipments1`
    FOREIGN KEY (`Shipments_ID`)
    REFERENCES `Shipments` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Devoluciones
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Devoluciones` ;

CREATE TABLE IF NOT EXISTS `Devoluciones` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Razón` VARCHAR(500) NOT NULL,
  `Fecha de devolución` DATETIME NOT NULL,
  `Cantidad de reembolso` DECIMAL(10,2) NOT NULL,
  `Ordenes_ID` INT NOT NULL,
  `Customers_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Devoluciones_Ordenes_idx` (`Ordenes_ID` ASC),
  INDEX `fk_Devoluciones_Customers_idx` (`Customers_ID` ASC),
  CONSTRAINT `fk_Devoluciones_Ordenes`
    FOREIGN KEY (`Ordenes_ID`)
    REFERENCES `Ordenes` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Devoluciones_Customers`
    FOREIGN KEY (`Customers_ID`)
    REFERENCES `Customers` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Order_items
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Order_items` ;

CREATE TABLE IF NOT EXISTS `Order_items` (
  `Products_ID` INT NOT NULL,
  `Ordenes_ID` INT NOT NULL,
  `Cantidad` INT NOT NULL,
  `Precio por unidad` DECIMAL(10,2) NOT NULL,
  `Devoluciones_ID` INT NULL,
  PRIMARY KEY (`Products_ID`, `Ordenes_ID`),
  INDEX `fk_Products_has_Ordenes_Ordenes1_idx` (`Ordenes_ID` ASC),
  INDEX `fk_Products_has_Ordenes_Products1_idx` (`Products_ID` ASC),
  INDEX `fk_Order_items_Devoluciones1_idx` (`Devoluciones_ID` ASC),
  CONSTRAINT `fk_Products_has_Ordenes_Products1`
    FOREIGN KEY (`Products_ID`)
    REFERENCES `Products` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_has_Ordenes_Ordenes1`
    FOREIGN KEY (`Ordenes_ID`)
    REFERENCES `Ordenes` (`ID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Order_items_Devoluciones1`
    FOREIGN KEY (`Devoluciones_ID`)
    REFERENCES `Devoluciones` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table inventory_movements
-- -----------------------------------------------------
DROP TABLE IF EXISTS `inventory_movements` ;

CREATE TABLE IF NOT EXISTS `inventory_movements` (
  `Products_ID` INT NOT NULL,
  `Warehouses_ID` INT NOT NULL,
  `Cantidad` INT NOT NULL,
  `Tipo de movimiento` ENUM('IN', 'OUT') NOT NULL,
  `Fecha del movimiento` DATETIME NOT NULL,
  `Employees_ID` INT NOT NULL,
  PRIMARY KEY (`Products_ID`, `Warehouses_ID`, `Fecha del movimiento`),
  INDEX `fk_Products_has_Warehouses_Warehouses1_idx` (`Warehouses_ID` ASC),
  INDEX `fk_Products_has_Warehouses_Products1_idx` (`Products_ID` ASC),
  INDEX `fk_inventory_movements_Employees_idx` (`Employees_ID` ASC),
  CONSTRAINT `fk_Products_has_Warehouses_Products1`
    FOREIGN KEY (`Products_ID`)
    REFERENCES `Products` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_has_Warehouses_Warehouses1`
    FOREIGN KEY (`Warehouses_ID`)
    REFERENCES `Warehouses` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_inventory_movements_Employees`
    FOREIGN KEY (`Employees_ID`)
    REFERENCES `Employees` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Promotions (opcional para puntos extra)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Promotions` ;

CREATE TABLE IF NOT EXISTS `Promotions` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(150) NOT NULL,
  `Descripción` VARCHAR(500) NULL,
  `Descuento_porcentaje` DECIMAL(5,2) NOT NULL,
  `Fecha_inicio` DATETIME NOT NULL,
  `Fecha_fin` DATETIME NOT NULL,
  `Activa` TINYINT(1) NOT NULL DEFAULT 1,
  `Categories_ID` INT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Promotions_Categories_idx` (`Categories_ID` ASC),
  CONSTRAINT `fk_Promotions_Categories`
    FOREIGN KEY (`Categories_ID`)
    REFERENCES `Categories` (`ID`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Loyalty_movements (opcional para puntos extra)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Loyalty_movements` ;

CREATE TABLE IF NOT EXISTS `Loyalty_movements` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Fecha` DATETIME NOT NULL,
  `Puntos_cambio` INT NOT NULL,
  `Descripción` VARCHAR(500) NULL,
  `Customers_ID` INT NOT NULL,
  `Ordenes_ID` INT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Loyalty_Customers_idx` (`Customers_ID` ASC),
  INDEX `fk_Loyalty_Ordenes_idx` (`Ordenes_ID` ASC),
  CONSTRAINT `fk_Loyalty_Customers`
    FOREIGN KEY (`Customers_ID`)
    REFERENCES `Customers` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Loyalty_Ordenes`
    FOREIGN KEY (`Ordenes_ID`)
    REFERENCES `Ordenes` (`ID`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Audit_log (opcional para puntos extra)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Audit_log` ;

CREATE TABLE IF NOT EXISTS `Audit_log` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Fecha_evento` DATETIME NOT NULL,
  `Tabla_afectada` VARCHAR(100) NOT NULL,
  `Operación` ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
  `Registro_ID` INT NOT NULL,
  `Users_ID` INT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Audit_Users_idx` (`Users_ID` ASC),
  CONSTRAINT `fk_Audit_Users`
    FOREIGN KEY (`Users_ID`)
    REFERENCES `Users` (`ID`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
