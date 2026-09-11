"""Dedicated contact customer support page — customers only."""

import reflex as rx

from frontend.components.contact import contact_us_widget
from full_stack_python.state import AuthState, CatalogState, SiteState, SupportState
from frontend.template import template


@rx.page(
    route="/contact",
    title="Nexus Games | Contact Support",
    on_load=[CatalogState.load_catalog, SiteState.load_site, AuthState.guard_customer, SupportState.load_tickets],
)
@template
def contact() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.vstack(
                rx.badge("Customer Support", color_scheme="purple", variant="soft"),
                rx.heading("Contact Us", size="8", weight="bold"),
                rx.text(
                    "Need help with an order, refund, or technical issue? "
                    "Send a message to our support team.",
                    size="4",
                    color=rx.color("gray", 11),
                    max_width="40rem",
                ),
                spacing="3",
                align="start",
            ),
            contact_us_widget(),
            spacing="6",
            padding_y="3rem",
            width="100%",
            max_width="40rem",
        ),
        size="4",
    )
