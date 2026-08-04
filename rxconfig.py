import reflex as rx

config = rx.Config(
    app_name="full_stack_python",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)