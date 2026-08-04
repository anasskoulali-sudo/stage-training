"""Shopping cart page."""

import reflex as rx

from full_stack_python.components.layout import page_layout
from full_stack_python.state import CartItem, ShopState


def cart_row(item: rx.Var[CartItem]) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.image(
                    src=item.image,
                    alt=item.title,
                    width="80px",
                    height="80px",
                    object_fit="cover",
                    border_radius="0.5rem",
                ),
                href="/game/" + item.game_id,
            ),
            rx.vstack(
                rx.link(
                    rx.text(item.title, weight="bold", size="4"),
                    href="/game/" + item.game_id,
                    color="inherit",
                    text_decoration="none",
                ),
                rx.text(
                    "$",
                    item.price,
                    " each",
                    size="2",
                    color=rx.color("gray", 11),
                ),
                spacing="1",
                align="start",
                flex="1",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("minus", size=14),
                    size="1",
                    variant="soft",
                    on_click=ShopState.decrease_quantity(item.id),
                ),
                rx.text(
                    item.quantity,
                    size="3",
                    weight="medium",
                    min_width="1.5rem",
                    text_align="center",
                ),
                rx.icon_button(
                    rx.icon("plus", size=14),
                    size="1",
                    variant="soft",
                    on_click=ShopState.increase_quantity(item.id),
                ),
                spacing="2",
                align="center",
            ),
            rx.text("$", item.price * item.quantity, size="4", weight="bold", color="#a78bfa"),
            rx.icon_button(
                rx.icon("trash-2", size=16),
                color_scheme="red",
                variant="ghost",
                on_click=ShopState.remove_from_cart(item.id),
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        padding="1rem",
        bg=rx.color("gray", 2),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="0.75rem",
    )


@rx.page(route="/cart", title="Nexus Games | Cart")
def cart() -> rx.Component:
    return page_layout(
        rx.container(
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
                    ShopState.cart_count > 0,
                    rx.vstack(
                        rx.foreach(ShopState.cart_items, cart_row),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Total", size="5", weight="bold"),
                                    rx.spacer(),
                                    rx.text(
                                        "$",
                                        ShopState.cart_total,
                                        size="6",
                                        weight="bold",
                                        color="#a78bfa",
                                    ),
                                    width="100%",
                                    align="center",
                                ),
                                rx.hstack(
                                    rx.button(
                                        "Clear Cart",
                                        variant="outline",
                                        color_scheme="red",
                                        on_click=ShopState.clear_cart,
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
                                        on_click=ShopState.checkout,
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
                    ShopState.checkout_message != "",
                    rx.callout(
                        ShopState.checkout_message,
                        icon="circle-check",
                        color_scheme="green",
                        width="100%",
                    ),
                ),
                spacing="6",
                padding_y="2rem",
            ),
            size="4",
        ),
    )
