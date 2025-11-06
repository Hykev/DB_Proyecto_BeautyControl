import reflex as rx
from .. import db


class InventoryState(rx.State):
    """Estado para manejar inventario e información logística."""

    # --- Datos de inventario (vista vw_inventario_producto_bodega) ---
    inventory_rows: list[dict] = []
    filter_product_id: str = ""
    filter_warehouse_id: str = ""

    # --- Consulta de stock puntual (SP sp_calcular_stock_producto_bodega) ---
    stock_query_product_id: str = ""
    stock_query_warehouse_id: str = ""
    stock_result: list[dict] = []
    has_stock_result: bool = False  # para poder hacer rx.cond sin problemas

    # --- Registro de movimiento de inventario (SP sp_registrar_movimiento_inventario) ---
    movement_product_id: str = ""
    movement_warehouse_id: str = ""
    movement_empleado_id: str = ""
    movement_cantidad: str = ""
    movement_tipo: str = "IN"  # IN / OUT
    movement_message: str = ""

    # ==========================================================
    # Inventario (vista)
    # ==========================================================

    def load_inventory(self):
        """Carga el inventario desde la vista vw_inventario_producto_bodega."""
        product_id = None
        warehouse_id = None

        if self.filter_product_id.strip() != "":
            try:
                product_id = int(self.filter_product_id)
            except ValueError:
                product_id = None

        if self.filter_warehouse_id.strip() != "":
            try:
                warehouse_id = int(self.filter_warehouse_id)
            except ValueError:
                warehouse_id = None

        self.inventory_rows = db.get_inventory_view(
            product_id=product_id,
            warehouse_id=warehouse_id,
        )

    def clear_inventory_filters(self):
        """Limpia filtros de inventario y recarga."""
        self.filter_product_id = ""
        self.filter_warehouse_id = ""
        self.load_inventory()

    # ==========================================================
    # Stock puntual (SP sp_calcular_stock_producto_bodega)
    # ==========================================================

    def query_stock(self):
        """Consulta el stock de un producto en una bodega específica."""
        if not self.stock_query_product_id or not self.stock_query_warehouse_id:
            self.movement_message = "Para consultar stock, ingresa producto y bodega."
            self.stock_result = []
            self.has_stock_result = False
            return

        try:
            product_id = int(self.stock_query_product_id)
            warehouse_id = int(self.stock_query_warehouse_id)
        except ValueError:
            self.movement_message = "Producto y bodega deben ser IDs numéricos."
            self.stock_result = []
            self.has_stock_result = False
            return

        result = db.get_stock_producto_bodega(product_id, warehouse_id)
        self.stock_result = result
        self.has_stock_result = len(result) > 0

    # ==========================================================
    # Registro de movimiento (SP sp_registrar_movimiento_inventario)
    # ==========================================================

    def register_movement(self):
        """Registra un movimiento IN/OUT de inventario usando el SP."""
        if not (
            self.movement_product_id
            and self.movement_warehouse_id
            and self.movement_empleado_id
            and self.movement_cantidad
        ):
            self.movement_message = "Producto, bodega, empleado y cantidad son obligatorios."
            return

        try:
            product_id = int(self.movement_product_id)
            warehouse_id = int(self.movement_warehouse_id)
            empleado_id = int(self.movement_empleado_id)
            cantidad = int(self.movement_cantidad)
        except ValueError:
            self.movement_message = "IDs y cantidad deben ser numéricos."
            return

        if self.movement_tipo not in ("IN", "OUT"):
            self.movement_message = "Tipo de movimiento debe ser IN o OUT."
            return

        ok = db.register_inventory_movement(
            product_id=product_id,
            warehouse_id=warehouse_id,
            empleado_id=empleado_id,
            cantidad=cantidad,
            tipo_movimiento=self.movement_tipo,
        )

        if ok:
            self.movement_message = "Movimiento registrado correctamente."
            # Refrescamos inventario y stock (si el usuario los tenía en pantalla)
            self.load_inventory()
            self.query_stock()
            self.movement_cantidad = ""
        else:
            self.movement_message = "Error al registrar movimiento."


# ===============================
# COMPONENTES DE UI
# ===============================

def inventory_filters_bar() -> rx.Component:
    """Barra de filtros para el inventario."""
    return rx.hstack(
        rx.input(
            placeholder="Filtrar por ID de producto...",
            value=InventoryState.filter_product_id,
            on_change=InventoryState.set_filter_product_id,
            width="16rem",
        ),
        rx.input(
            placeholder="Filtrar por ID de bodega...",
            value=InventoryState.filter_warehouse_id,
            on_change=InventoryState.set_filter_warehouse_id,
            width="16rem",
        ),
        rx.button(
            "Filtrar",
            color_scheme="orange",
            on_click=InventoryState.load_inventory,
        ),
        rx.button(
            "Limpiar",
            variant="soft",
            on_click=InventoryState.clear_inventory_filters,
        ),
        spacing="3",
        wrap="wrap",
        align_items="flex-end",
    )


def inventory_table() -> rx.Component:
    """Tabla principal de inventario (vista vw_inventario_producto_bodega)."""
    headers = [
        "ID Producto",
        "Producto",
        "ID Bodega",
        "Bodega",
        "Stock actual",
    ]

    def render_row(r: dict):
        return rx.table.row(
            rx.table.cell(str(r["product_id"])),
            rx.table.cell(r["NombreProducto"]),
            rx.table.cell(str(r["warehouse_id"])),
            rx.table.cell(r["warehouse_nombre"]),
            rx.table.cell(str(r["stock_actual"])),
        )

    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    *[rx.table.column_header_cell(h) for h in headers],
                )
            ),
            rx.table.body(
                rx.foreach(InventoryState.inventory_rows, render_row)
            ),
        ),
        width="100%",
        overflow_x="auto",
        bg="white",
        padding="1rem",
        border_radius="1rem",
        box_shadow="0 8px 16px rgba(15,23,42,0.08)",
    )


def stock_query_panel() -> rx.Component:
    """Panel para consultar stock puntual por producto y bodega."""
    def stock_result_box() -> rx.Component:
        return rx.cond(
            InventoryState.has_stock_result,
            _stock_result_content(),
        )

    return rx.box(
        rx.vstack(
            rx.heading("Consulta de stock puntual", size="5", color="orange.9"),
            rx.text(
                "Consulta el stock de un producto en una bodega específica usando el SP sp_calcular_stock_producto_bodega.",
                font_size="0.85rem",
                color="gray.9",
            ),
            rx.hstack(
                rx.input(
                    placeholder="ID de producto",
                    value=InventoryState.stock_query_product_id,
                    on_change=InventoryState.set_stock_query_product_id,
                    width="10rem",
                ),
                rx.input(
                    placeholder="ID de bodega",
                    value=InventoryState.stock_query_warehouse_id,
                    on_change=InventoryState.set_stock_query_warehouse_id,
                    width="10rem",
                ),
                rx.button(
                    "Consultar stock",
                    color_scheme="orange",
                    on_click=InventoryState.query_stock,
                ),
                spacing="3",
                wrap="wrap",
            ),
            stock_result_box(),
            spacing="3",
        ),
        bg="white",
        padding="1.5rem",
        border_radius="1.25rem",
        box_shadow="0 10px 30px rgba(15,23,42,0.12)",
        width="100%",
    )


def _stock_result_content() -> rx.Component:
    """Contenido que muestra el resultado del SP de stock."""
    # Result es una lista, normalmente de 0 o 1 fila
    def render_row(r: dict):
        return rx.vstack(
            rx.text(
                f'Producto #{r["product_id"]}: {r["Nombre del producto"]}',
                font_weight="medium",
            ),
            rx.text(
                f'Bodega #{r["warehouse_id"]}: {r["warehouse_nombre"]}',
            ),
            rx.text(
                f'Stock actual: {r["stock_actual"]}',
                font_weight="bold",
                color="orange.9",
            ),
            spacing="1",
        )

    return rx.vstack(
        rx.heading("Resultado", size="4", color="orange.9"),
        rx.foreach(InventoryState.stock_result, render_row),
        spacing="2",
        bg="#fff7ed",
        padding="1rem",
        border_radius="1rem",
        border="1px solid #fed7aa",
    )


def movement_form() -> rx.Component:
    """Formulario para registrar un movimiento de inventario (IN / OUT)."""
    return rx.box(
        rx.vstack(
            rx.heading("Registrar movimiento de inventario", size="5", color="orange.9"),
            rx.text(
                "Usa el SP sp_registrar_movimiento_inventario para entradas y salidas de inventario.",
                font_size="0.85rem",
                color="gray.9",
            ),
            rx.hstack(
                rx.input(
                    placeholder="ID de producto",
                    value=InventoryState.movement_product_id,
                    on_change=InventoryState.set_movement_product_id,
                    width="10rem",
                ),
                rx.input(
                    placeholder="ID de bodega",
                    value=InventoryState.movement_warehouse_id,
                    on_change=InventoryState.set_movement_warehouse_id,
                    width="10rem",
                ),
                rx.input(
                    placeholder="ID de empleado",
                    value=InventoryState.movement_empleado_id,
                    on_change=InventoryState.set_movement_empleado_id,
                    width="10rem",
                ),
                spacing="3",
                wrap="wrap",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Cantidad",
                    value=InventoryState.movement_cantidad,
                    on_change=InventoryState.set_movement_cantidad,
                    width="10rem",
                ),
                rx.select(
                    items=["IN", "OUT"],
                    value=InventoryState.movement_tipo,
                    on_change=InventoryState.set_movement_tipo,
                    label="Tipo de movimiento",
                    width="10rem",
                ),
                spacing="3",
                wrap="wrap",
            ),
            rx.button(
                "Registrar movimiento",
                color_scheme="orange",
                on_click=InventoryState.register_movement,
            ),
            rx.cond(
                InventoryState.movement_message != "",
                rx.text(InventoryState.movement_message, color="orange.10"),
            ),
            spacing="3",
        ),
        bg="white",
        padding="1.5rem",
        border_radius="1.25rem",
        box_shadow="0 10px 30px rgba(15,23,42,0.12)",
        width="100%",
    )


# ===============================
# PÁGINA PRINCIPAL
# ===============================

def inventory_page() -> rx.Component:
    """Vista principal del módulo Inventario & Logística."""
    return rx.vstack(
        rx.heading("Inventario & Logística", size="6", color="orange.9"),
        rx.text(
            "Consulta el stock por producto y bodega, y registra movimientos de inventario.",
        ),
        rx.divider(margin_y="0.5rem"),
        inventory_filters_bar(),
        inventory_table(),
        rx.divider(margin_y="1rem"),
        stock_query_panel(),
        rx.divider(margin_y="1rem"),
        movement_form(),
        spacing="4",
        width="100%",
        on_mount=InventoryState.load_inventory,
    )
