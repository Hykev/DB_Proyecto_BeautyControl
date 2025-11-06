import reflex as rx
from .. import db


class ProductsState(rx.State):
    """Estado para manejar el CRUD de productos."""

    # --- Datos y paginación ---
    products: list[dict] = []
    page: int = 0
    page_size: int = 10

    # --- Filtros ---
    search_name: str = ""
    search_category_id: str = ""   # de momento como texto, luego podemos hacer combos
    search_supplier_id: str = ""

    # --- Formulario (crear / editar) ---
    selected_id: int | None = None
    nombre_producto: str = ""
    precio: str = ""               # lo guardamos como string y lo convertimos a float al guardar
    category_id_str: str = ""
    supplier_id_str: str = ""

    # --- Mensajes ---
    form_message: str = ""

    # ==========================================================
    # Acciones principales
    # ==========================================================

    def load_products(self):
        """Carga los productos con filtros y paginación."""
        category_id = int(self.search_category_id) if self.search_category_id.strip() != "" else None
        supplier_id = int(self.search_supplier_id) if self.search_supplier_id.strip() != "" else None

        self.products = db.get_products(
            nombre=self.search_name or None,
            category_id=category_id,
            supplier_id=supplier_id,
            page=self.page,
            page_size=self.page_size,
        )

    def next_page(self):
        """Paginación siguiente."""
        self.page += 1
        self.load_products()

    def prev_page(self):
        """Paginación anterior."""
        if self.page > 0:
            self.page -= 1
        self.load_products()

    def clear_filters(self):
        """Reinicia filtros y recarga."""
        self.search_name = ""
        self.search_category_id = ""
        self.search_supplier_id = ""
        self.page = 0
        self.load_products()

    # ==========================================================
    # Formulario (crear / editar / eliminar)
    # ==========================================================

    def fill_form(self, product_id: int):
        """Rellena el formulario con los datos del producto seleccionado."""
        p = db.get_product_by_id(product_id)
        if p:
            self.selected_id = p["ID"]
            self.nombre_producto = p["NombreProducto"]
            self.precio = str(p["Precio"])
            self.category_id_str = str(p["Categories_ID"])
            self.supplier_id_str = str(p["Suppliers_ID"])
            self.form_message = f"Editando producto #{self.selected_id}"

    def clear_form(self):
        """Limpia el formulario."""
        self.selected_id = None
        self.nombre_producto = ""
        self.precio = ""
        self.category_id_str = ""
        self.supplier_id_str = ""
        self.form_message = ""

    def save_product(self):
        """Crea o actualiza un producto."""
        # Validaciones básicas
        if not self.nombre_producto:
            self.form_message = "El nombre del producto es obligatorio."
            return

        if not self.precio:
            self.form_message = "El precio es obligatorio."
            return

        try:
            precio_float = float(self.precio)
        except ValueError:
            self.form_message = "El precio debe ser un número válido."
            return

        try:
            category_id = int(self.category_id_str)
            supplier_id = int(self.supplier_id_str)
        except ValueError:
            self.form_message = "Categoría y proveedor deben ser IDs numéricos válidos."
            return

        if self.selected_id:
            ok = db.update_product(
                self.selected_id,
                self.nombre_producto,
                precio_float,
                category_id,
                supplier_id,
            )
            self.form_message = (
                "Producto actualizado correctamente." if ok else "Error al actualizar."
            )
        else:
            ok = db.create_product(
                self.nombre_producto,
                precio_float,
                category_id,
                supplier_id,
            )
            self.form_message = (
                "Producto creado correctamente." if ok else "Error al crear producto."
            )

        self.clear_form()
        self.load_products()

    def delete_product(self, product_id: int):
        """Elimina un producto."""
        ok = db.delete_product(product_id)
        self.form_message = (
            "Producto eliminado correctamente." if ok else "Error al eliminar producto."
        )
        self.load_products()


# ===============================
# COMPONENTES DE UI
# ===============================

def products_table() -> rx.Component:
    """Tabla principal de productos."""
    headers = [
        "ID",
        "Nombre",
        "Categoría",
        "Proveedor",
        "Precio",
        "Fecha creación",
        "Acciones",
    ]

    def render_row(p: dict):
        """Renderiza una fila de la tabla de productos (compatible Reflex 0.8+)."""
        return rx.table.row(
            rx.table.cell(str(p["ID"])),
            rx.table.cell(p["NombreProducto"]),
            rx.table.cell(
                rx.cond(
                    p.get("CategoriaNombre") != None,
                    p.get("CategoriaNombre"),
                    "",
                )
            ),
            rx.table.cell(
                rx.cond(
                    p.get("SupplierNombre") != None,
                    p.get("SupplierNombre"),
                    "",
                )
            ),
            rx.table.cell(f"Q {p['Precio']}"),
            rx.table.cell(str(p["FechaCreacion"])),
            rx.table.cell(
                rx.hstack(
                    rx.button(
                        "✏️",
                        size="1",
                        variant="soft",
                        color_scheme="orange",
                        on_click=lambda: ProductsState.fill_form(p["ID"]),
                    ),
                    rx.button(
                        "🗑️",
                        size="1",
                        variant="ghost",
                        color_scheme="red",
                        on_click=lambda: ProductsState.delete_product(p["ID"]),
                    ),
                    spacing="2",
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
                rx.foreach(ProductsState.products, render_row)
            ),
        ),
        width="100%",
        overflow_x="auto",
        bg="white",
        padding="1rem",
        border_radius="1rem",
        box_shadow="0 8px 16px rgba(15,23,42,0.08)",
    )


def product_form() -> rx.Component:
    """Formulario para crear o editar un producto."""
    return rx.box(
        rx.vstack(
            rx.heading("Formulario de Producto", size="5", color="orange.9"),
            rx.input(
                placeholder="Nombre del producto",
                value=ProductsState.nombre_producto,
                on_change=ProductsState.set_nombre_producto,
            ),
            rx.input(
                placeholder="Precio (ej. 199.99)",
                value=ProductsState.precio,
                on_change=ProductsState.set_precio,
            ),
            rx.input(
                placeholder="ID de categoría (Categories_ID)",
                value=ProductsState.category_id_str,
                on_change=ProductsState.set_category_id_str,
            ),
            rx.input(
                placeholder="ID de proveedor (Suppliers_ID)",
                value=ProductsState.supplier_id_str,
                on_change=ProductsState.set_supplier_id_str,
            ),
            rx.hstack(
                rx.button(
                    rx.cond(
                        ProductsState.selected_id != None,
                        "Actualizar",
                        "Crear",
                    ),
                    color_scheme="orange",
                    on_click=ProductsState.save_product,
                ),
                rx.button(
                    "Limpiar",
                    variant="soft",
                    on_click=ProductsState.clear_form,
                ),
                spacing="3",
            ),
            rx.cond(
                ProductsState.form_message != "",
                rx.text(ProductsState.form_message, color="orange.10"),
            ),
            spacing="3",
        ),
        bg="#fff8f0",
        border="1px solid #fed7aa",
        border_radius="1rem",
        padding="1.5rem",
        width="22rem",
    )


def filters_bar() -> rx.Component:
    """Barra de filtros arriba de la tabla de productos."""
    return rx.hstack(
        rx.input(
            placeholder="Buscar por nombre...",
            value=ProductsState.search_name,
            on_change=ProductsState.set_search_name,
            width="16rem",
        ),
        rx.input(
            placeholder="Filtrar por ID categoría...",
            value=ProductsState.search_category_id,
            on_change=ProductsState.set_search_category_id,
            width="12rem",
        ),
        rx.input(
            placeholder="Filtrar por ID proveedor...",
            value=ProductsState.search_supplier_id,
            on_change=ProductsState.set_search_supplier_id,
            width="12rem",
        ),
        rx.button(
            "Filtrar",
            color_scheme="orange",
            on_click=ProductsState.load_products,
        ),
        rx.button(
            "Limpiar",
            variant="soft",
            on_click=ProductsState.clear_filters,
        ),
        spacing="3",
        wrap="wrap",
    )


def pagination_controls() -> rx.Component:
    """Botones de paginación para productos."""
    return rx.hstack(
        rx.button("← Anterior", on_click=ProductsState.prev_page),
        rx.button("Siguiente →", on_click=ProductsState.next_page),
        spacing="4",
    )


# ===============================
# PÁGINA PRINCIPAL
# ===============================

def products_page() -> rx.Component:
    """Vista principal del módulo Productos."""
    return rx.vstack(
        rx.heading("Gestión de Productos", size="6", color="orange.9"),
        rx.text("Administra el catálogo de figuras, funkos, cartas y otros coleccionables."),
        rx.divider(margin_y="0.5rem"),
        filters_bar(),
        products_table(),
        pagination_controls(),
        rx.divider(margin_y="1rem"),
        product_form(),
        spacing="4",
        width="100%",
        on_mount=ProductsState.load_products,
    )
