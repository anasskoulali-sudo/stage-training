"""Shopping cart page."""

import reflex as rx

from frontend.components.cart import cart_row
from full_stack_python.state import CartState, CatalogState, SiteState
from frontend.styles import ACCENT
from frontend.template import template


@rx.page(
    route="/cart",
    title="Nexus Games | Cart",
    on_load=[CatalogState.load_catalog, SiteState.load_site],
)
@template
def cart() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.vstack(
                rx.heading("Your Cart", size="8", weight="bold"),
                rx.text(
                    "Review your picks before checkout.",
                    size="4",
                    color=rx.color("gray", 11),
                ),
                spacing="2",
                align="start",
            ),
            rx.cond(
                CartState.cart_count > 0,
                rx.vstack(
                    rx.foreach(CartState.cart_items, cart_row),
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("Total", size="5", weight="bold"),
                                rx.spacer(),
                                rx.text(
                                    "$",
                                    CartState.cart_total,
                                    size="6",
                                    weight="bold",
                                    color=ACCENT,
                                ),
                                width="100%",
                                align="center",
                            ),
                            rx.hstack(
                                rx.button(
                                    "Clear Cart",
                                    variant="outline",
                                    color_scheme="red",
                                    on_click=CartState.clear_cart,
                                ),
                                rx.link(
                                    rx.button(
                                        "Continue Shopping",
                                        variant="soft",
                                        color_scheme="purple",
                                    ),
                                    href="/shop",
                                ),
                                rx.spacer(),
                                rx.button(
                                    rx.icon("credit-card", size=18),
                                    "Checkout",
                                    size="3",
                                    color_scheme="purple",
                                    on_click=CartState.checkout,
                                ),
                                width="100%",
                                flex_wrap="wrap",
                                spacing="3",
                            ),
                            spacing="4",
                        ),
                        padding="1.5rem",
                        bg=rx.color("gray", 2),
                        border=f"1px solid {rx.color('gray', 6)}",
                        border_radius="0.75rem",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("shopping-cart", size=56, color=rx.color("gray", 9)),
                        rx.heading("Your cart is empty", size="6"),
                        rx.text(
                            "Head to the shop and add some games!",
                            color=rx.color("gray", 11),
                        ),
                        rx.link(
                            rx.button(
                                rx.icon("gamepad-2", size=18),
                                "Browse Shop",
                                color_scheme="purple",
                                size="3",
                            ),
                            href="/shop",
                        ),
                        spacing="4",
                        align="center",
                    ),
                    padding_y="4rem",
                ),
            ),
            rx.cond(
                CartState.checkout_message != "",
                rx.callout(
                    CartState.checkout_message,
                    icon="circle-check",
                    color_scheme="green",
                    width="100%",
                ),
            ),
            spacing="6",
            padding_y="2rem",
        ),
        size="4",
    )
