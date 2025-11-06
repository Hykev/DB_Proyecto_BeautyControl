import reflex as rx
from .. import db


class PromosLoyaltyState(rx.State):
    """Estado para manejar promociones y movimientos de lealtad."""

    # --- Promociones ---
    promotions: list[dict] = []

    # --- Movimientos de lealtad ---
    loyalty_customer_id: str = ""
    loyalty_rows: list[dict] = []
    has_loyalty_rows: bool = False
    loyalty_puntos_total: int = 0
    loyalty_message: str = ""

    # --- Formulario para registrar movimiento manual de lealtad ---
    form_customer_id: str = ""
    form_order_id: str = ""
    form_puntos: str = ""
    form_descripcion: str = ""
    form_message: str = ""

    # ==========================================================
    # Promociones
    # ==========================================================

    def load_promotions(self):
        """Carga las promociones (por ahora, solo las activas)."""
        self.promotions = db.get_promotions(only_active=True)

    # ==========================================================
    # Movimientos de lealtad
    # ==========================================================

    def load_loyalty_movements(self):
        """Carga los movimientos de lealtad de un cliente."""
        self.loyalty_message = ""
        self.loyalty_rows = []
        self.has_loyalty_rows = False
        self.loyalty_puntos_total = 0

        if not self.loyalty_customer_id.strip():
            self.loyalty_message = "Ingresa un ID de cliente para ver sus puntos."
            return

        try:
            customer_id = int(self.loyalty_customer_id)
        except ValueError:
            self.loyalty_message = "El ID de cliente debe ser numérico."
            return

        rows = db.get_loyalty_movements_by_customer(customer_id)
        self.loyalty_rows = rows
        self.has_loyalty_rows = len(rows) > 0
        self.loyalty_puntos_total = sum(r.get("Puntos_cambio", 0) for r in rows)

        if not rows:
            self.loyalty_message = "Este cliente no tiene movimientos de lealtad."

    # ==========================================================
    # Registrar movimiento manual de lealtad
    # ==========================================================

    def register_loyalty_movement(self):
        """Registra un movimiento de lealtad (puntos + / -)."""
        self.form_message = ""

        if not self.form_customer_id.strip():
            self.form_message = "El ID de cliente es obligatorio."
            return

        if not self.form_puntos.strip():
            self.form_message = "Debes indicar cuántos puntos sumar o restar."
            return

        try:
            customer_id = int(self.form_customer_id)
        except ValueError:
            self.form_message = "El ID de cliente debe ser numérico."
            return

        order_id = None
        if self.form_order_id.strip() != "":
            try:
                order_id = int(self.form_order_id)
            except ValueError:
                self.form_message = "El ID de orden debe ser numérico."
                return

        try:
            puntos = int(self.form_puntos)
        except ValueError:
            self.form_message = "Los puntos deben ser un número entero (positivo o negativo)."
            return

        descripcion = self.form_descripcion.strip() or "Ajuste manual de puntos"

        db.register_loyalty_movement(
            customer_id=customer_id,
            order_id=order_id,
            puntos=puntos,
            descripcion=descripcion,
        )

        self.form_message = "Movimiento de lealtad registrado correctamente."

        # Si el cliente del formulario es el mismo de la pestaña de consulta, recargamos
        if self.loyalty_customer_id.strip() == self.form_customer_id.strip():
            self.load_loyalty_movements()

        # Limpiar campos de puntos y descripción
        self.form_puntos = ""
        self.form_descripcion = ""


# ===============================
# COMPONENTES DE UI
# ===============================

def promotions_table() -> rx.Component:
    """Tabla de promociones activas."""
    headers = [
        "ID",
        "Nombre",
        "Descripción",
        "Descuento %",
        "Inicio",
        "Fin",
        "Categoría",
        "Activa",
    ]

    def render_row(promo: dict):
        return rx.table.row(
            rx.table.cell(str(promo["ID"])),
            rx.table.cell(promo["Nombre"]),
            rx.table.cell(
                rx.cond(
                    promo.get("Descripcion") != None,
                    promo.get("Descripcion"),
                    "",
                )
            ),
            rx.table.cell(str(promo.get("Descuento_porcentaje", ""))),
            rx.table.cell(str(promo.get("Fecha_inicio", ""))),
            rx.table.cell(str(promo.get("Fecha_fin", ""))),
            rx.table.cell(
                rx.cond(
                    promo.get("CategoriaNombre") != None,
                    promo.get("CategoriaNombre"),
                    "-",
                )
            ),
            rx.table.cell(
                rx.cond(
                    promo["Activa"] == 1,
                    "Sí",
                    "No",
                )
            ),
        )


    return rx.box(
        rx.heading("Promociones activas", size="5", color="orange.9"),
        rx.text(
            "Promociones actuales sobre categorías de productos coleccionables.",
            font_size="0.9rem",
            color="gray.9",
        ),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        *[rx.table.column_header_cell(h) for h in headers],
                    )
                ),
                rx.table.body(
                    rx.foreach(PromosLoyaltyState.promotions, render_row)
                ),
            ),
            width="100%",
            overflow_x="auto",
            bg="white",
            padding="1rem",
            border_radius="1rem",
            box_shadow="0 8px 16px rgba(15,23,42,0.08)",
            margin_top="0.75rem",
        ),
        width="100%",
        spacing="2",
    )


def loyalty_query_panel() -> rx.Component:
    """Panel para consultar movimientos de lealtad de un cliente."""
    def loyalty_table() -> rx.Component:
        def render_row(m: dict):
            return rx.table.row(
                rx.table.cell(str(m["Fecha"])),
                rx.table.cell(str(m["Puntos_cambio"])),
                rx.table.cell(m["Descripcion"]),
                rx.table.cell(
                    rx.cond(
                        m.get("Ordenes_ID") != None,
                        str(m.get("Ordenes_ID")),
                        "-",
                    )
                ),
                rx.table.cell(
                    rx.cond(
                        m.get("FechaOrden") != None,
                        str(m.get("FechaOrden")),
                        "-",
                    )
                ),
                rx.table.cell(
                    rx.cond(
                        m.get("TotalOrden") != None,
                        f'Q {m.get("TotalOrden")}',
                        "-",
                    )
                ),
            )

        table_component = rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Fecha"),
                        rx.table.column_header_cell("Puntos"),
                        rx.table.column_header_cell("Descripción"),
                        rx.table.column_header_cell("Orden"),
                        rx.table.column_header_cell("Fecha orden"),
                        rx.table.column_header_cell("Total orden"),
                    )
                ),
                rx.table.body(
                    rx.foreach(PromosLoyaltyState.loyalty_rows, render_row)
                ),
            ),
            width="100%",
            overflow_x="auto",
            bg="white",
            padding="1rem",
            border_radius="1rem",
            box_shadow="0 8px 16px rgba(15,23,42,0.08)",
        )

        return rx.vstack(
            table_component,
            rx.text(
                f"Puntos netos de este cliente: {PromosLoyaltyState.loyalty_puntos_total}",
                font_weight="medium",
                color="orange.9",
            ),
            spacing="2",
        )

    return rx.box(
        rx.vstack(
            rx.heading("Lealtad por cliente", size="5", color="orange.9"),
            rx.text(
                "Consulta los puntos ganados y redimidos por un cliente.",
                font_size="0.9rem",
                color="gray.9",
            ),
            rx.hstack(
                rx.input(
                    placeholder="ID de cliente...",
                    value=PromosLoyaltyState.loyalty_customer_id,
                    on_change=PromosLoyaltyState.set_loyalty_customer_id,
                    width="12rem",
                ),
                rx.button(
                    "Cargar movimientos",
                    color_scheme="orange",
                    on_click=PromosLoyaltyState.load_loyalty_movements,
                ),
                spacing="3",
                wrap="wrap",
            ),
            rx.cond(
                PromosLoyaltyState.loyalty_message != "",
                rx.text(
                    PromosLoyaltyState.loyalty_message,
                    color="orange.10",
                    font_size="0.85rem",
                ),
            ),
            rx.cond(
                PromosLoyaltyState.has_loyalty_rows,
                loyalty_table(),
            ),
            spacing="3",
        ),
        bg="#fff8f0",
        padding="1.5rem",
        border_radius="1.25rem",
        border="1px solid #fed7aa",
        width="100%",
    )


def loyalty_form_panel() -> rx.Component:
    """Formulario para registrar un movimiento manual de puntos."""
    return rx.box(
        rx.vstack(
            rx.heading("Registrar movimiento de lealtad", size="5", color="orange.9"),
            rx.text(
                "Registra ajustes de puntos (por correcciones, bonos especiales, etc.).",
                font_size="0.9rem",
                color="gray.9",
            ),
            rx.hstack(
                rx.input(
                    placeholder="ID de cliente",
                    value=PromosLoyaltyState.form_customer_id,
                    on_change=PromosLoyaltyState.set_form_customer_id,
                    width="10rem",
                ),
                rx.input(
                    placeholder="ID de orden (opcional)",
                    value=PromosLoyaltyState.form_order_id,
                    on_change=PromosLoyaltyState.set_form_order_id,
                    width="10rem",
                ),
                spacing="3",
                wrap="wrap",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Puntos (+ ganados / - utilizados)",
                    value=PromosLoyaltyState.form_puntos,
                    on_change=PromosLoyaltyState.set_form_puntos,
                    width="14rem",
                ),
                spacing="3",
                wrap="wrap",
            ),
            rx.text_area(
                placeholder="Descripción del movimiento",
                value=PromosLoyaltyState.form_descripcion,
                on_change=PromosLoyaltyState.set_form_descripcion,
            ),
            rx.button(
                "Registrar movimiento",
                color_scheme="orange",
                on_click=PromosLoyaltyState.register_loyalty_movement,
            ),
            rx.cond(
                PromosLoyaltyState.form_message != "",
                rx.text(
                    PromosLoyaltyState.form_message,
                    color="orange.10",
                    font_size="0.85rem",
                ),
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

def promos_loyalty_page() -> rx.Component:
    """Vista principal del módulo Promociones & Lealtad."""
    return rx.vstack(
        rx.heading("Promociones & Lealtad", size="6", color="orange.9"),
        rx.text(
            "Administra las promociones activas y consulta los puntos de tus clientes más fieles.",
        ),
        rx.divider(margin_y="0.5rem"),
        promotions_table(),
        rx.divider(margin_y="1.5rem"),
        rx.hstack(
            loyalty_query_panel(),
            loyalty_form_panel(),
            spacing="4",              
            wrap="wrap",
            align_items="flex-start",
        ),
        spacing="4",
        width="100%",
        on_mount=PromosLoyaltyState.load_promotions,
    )

