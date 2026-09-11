"""Cart line item used on the cart page."""

import reflex as rx

from full_stack_python.models import CartItem
from full_stack_python.state import CartState
from frontend.styles import ACCENT


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
                    on_click=CartState.decrease_quantity(item.id),
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
                    on_click=CartState.increase_quantity(item.id),
                ),
                spacing="2",
                align="center",
            ),
            rx.text("$", item.price * item.quantity, size="4", weight="bold", color=ACCENT),
            rx.icon_button(
                rx.icon("trash-2", size=16),
                color_scheme="red",
                variant="ghost",
                on_click=CartState.remove_from_cart(item.id),
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
