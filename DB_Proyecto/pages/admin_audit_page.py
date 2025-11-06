import reflex as rx
from .. import db


class AdminAuditState(rx.State):
    """Estado para la vista de Administración & Auditoría."""

    # Datos
    logs: list[dict] = []
    page: int = 0
    page_size: int = 20

    # Filtros
    filtro_tabla: str = ""
    filtro_operacion: str = ""
    filtro_usuario: str = ""
    filtro_fecha_desde: str = ""  # 'YYYY-MM-DD' opcional
    filtro_fecha_hasta: str = ""  # 'YYYY-MM-DD' opcional

    mensaje: str = ""

    # ============================
    # Acciones principales
    # ============================

    def load_logs(self):
        """Carga los registros de auditoría con los filtros actuales."""
        self.mensaje = ""

        tabla = self.filtro_tabla.strip() or None
        operacion = self.filtro_operacion.strip() or None
        usuario = self.filtro_usuario.strip() or None
        fecha_desde = self.filtro_fecha_desde.strip() or None
        fecha_hasta = self.filtro_fecha_hasta.strip() or None

        self.logs = db.get_audit_logs(
            tabla=tabla,
            operacion=operacion,
            usuario=usuario,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            page=self.page,
            page_size=self.page_size,
        )

        if self.logs == []:
            self.mensaje = "No se encontraron registros de auditoría con estos filtros."

    def next_page(self):
        """Página siguiente."""
        self.page += 1
        self.load_logs()

    def prev_page(self):
        """Página anterior."""
        if self.page > 0:
            self.page -= 1
        self.load_logs()

    def clear_filters(self):
        """Limpia filtros y regresa a la primera página."""
        self.filtro_tabla = ""
        self.filtro_operacion = ""
        self.filtro_usuario = ""
        self.filtro_fecha_desde = ""
        self.filtro_fecha_hasta = ""
        self.page = 0
        self.load_logs()


# ============================
# Componentes de UI
# ============================

def audit_filters_bar() -> rx.Component:
    """Barra de filtros para el audit log."""
    return rx.vstack(
        rx.hstack(
            rx.input(
                placeholder="Tabla (ej. Customers, Products...)",
                value=AdminAuditState.filtro_tabla,
                on_change=AdminAuditState.set_filtro_tabla,
                width="14rem",
            ),
            rx.select(
                items=["INSERT", "UPDATE", "DELETE"],
                value=AdminAuditState.filtro_operacion,
                on_change=AdminAuditState.set_filtro_operacion,
                placeholder="Operación",
                width="10rem",
            ),
            rx.input(
                placeholder="Usuario (contiene...)",
                value=AdminAuditState.filtro_usuario,
                on_change=AdminAuditState.set_filtro_usuario,
                width="12rem",
            ),
            spacing="3",
            wrap="wrap",
        ),
        rx.hstack(
            rx.input(
                placeholder="Desde (YYYY-MM-DD)",
                value=AdminAuditState.filtro_fecha_desde,
                on_change=AdminAuditState.set_filtro_fecha_desde,
                width="12rem",
            ),
            rx.input(
                placeholder="Hasta (YYYY-MM-DD)",
                value=AdminAuditState.filtro_fecha_hasta,
                on_change=AdminAuditState.set_filtro_fecha_hasta,
                width="12rem",
            ),
            rx.button(
                "Aplicar filtros",
                color_scheme="orange",
                on_click=AdminAuditState.load_logs,
            ),
            rx.button(
                "Limpiar",
                variant="soft",
                on_click=AdminAuditState.clear_filters,
            ),
            spacing="3",
            wrap="wrap",
        ),
        align_items="flex-start",
        spacing="2",
        width="100%",
    )


def audit_table() -> rx.Component:
    """Tabla de registros de auditoría."""
    headers = [
        "ID",
        "Fecha evento",
        "Tabla afectada",
        "Operación",
        "Registro ID",
        "Usuario ID",
    ]

    def render_row(log: dict):
        return rx.table.row(
            rx.table.cell(log["ID"]),
            rx.table.cell(log["Fecha_evento"]),
            rx.table.cell(log["Tabla_afectada"]),
            rx.table.cell(log["Operacion"]),
            rx.table.cell(log["Registro_ID"]),
            rx.table.cell(
                rx.cond(
                    log["Users_ID"] != None,
                    log["Users_ID"],
                    "admin_1",
                )
            ),
        )

    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    *[rx.table.column_header_cell(h) for h in headers],
                )
            ),
            rx.table.body(
                rx.foreach(AdminAuditState.logs, render_row)
            ),
        ),
        width="100%",
        overflow_x="auto",
        bg="white",
        padding="1rem",
        border_radius="1rem",
        box_shadow="0 8px 16px rgba(15,23,42,0.08)",
    )


def audit_pagination() -> rx.Component:
    """Botones de paginación."""
    return rx.hstack(
        rx.button("← Anterior", on_click=AdminAuditState.prev_page),
        rx.button("Siguiente →", on_click=AdminAuditState.next_page),
        spacing="4",
    )

def audit_pagination() -> rx.Component:
    """Botones de paginación."""
    return rx.hstack(
        rx.button("← Anterior", on_click=AdminAuditState.prev_page),
        rx.button("Siguiente →", on_click=AdminAuditState.next_page),
        spacing="4",
    )


# ============================
# Página principal
# ============================

def admin_audit_page() -> rx.Component:
    """Vista principal de Administración & Auditoría."""
    return rx.vstack(
        rx.heading("Administración & Auditoría", size="6", color="orange.9"),
        rx.text(
            "Revisa el historial de cambios en las tablas de LootBox (INSERT, UPDATE, DELETE).",
        ),
        rx.divider(margin_y="0.5rem"),
        audit_filters_bar(),
        rx.cond(
            AdminAuditState.mensaje != "",
            rx.text(
                AdminAuditState.mensaje,
                color="orange.10",
                font_size="0.85rem",
            ),
        ),
        audit_table(),
        audit_pagination(),
        spacing="4",
        width="100%",
        on_mount=AdminAuditState.load_logs,
    )
