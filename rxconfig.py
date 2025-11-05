import reflex as rx

config = rx.Config(
    app_name="DB_Proyecto",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)