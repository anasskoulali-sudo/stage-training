"""Dedicated contact customer support page — customers only."""

import reflex as rx

from full_stack_python.components.contact_widget import contact_us_widget
from full_stack_python.components.layout import page_layout
from full_stack_python.state import AuthState


@rx.page(
    route="/contact",
    title="Nexus Games | Contact Support",
    on_load=AuthState.guard_customer,
)
def contact() -> rx.Component:
    return page_layout(
        rx.container(
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
        ),
    )
