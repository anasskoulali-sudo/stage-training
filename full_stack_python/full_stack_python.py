"""Nexus Games — a multi-page video game shop built with Reflex."""

import reflex as rx

from full_stack_python.pages import about, account, admin, cart, contact, game_detail, home, shop

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="purple",
        radius="medium",
    ),
)

# Import pages so @rx.page decorators register with the app.
__all__ = ["app"]
