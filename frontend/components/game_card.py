"""Reusable game card used on home, shop, and related-title grids."""

import reflex as rx

from full_stack_python.models import Game
from full_stack_python.state import CartState
from frontend.styles import ACCENT, STAR


def game_card_var(game: rx.Var[Game]) -> rx.Component:
    return rx.box(
        rx.link(
            rx.box(
                rx.image(
                    src=game.image,
                    alt=game.title,
                    width="100%",
                    height="180px",
                    object_fit="cover",
                    border_radius="0.75rem 0.75rem 0 0",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.badge(game.category, color_scheme="purple", variant="soft"),
                        rx.spacer(),
                        rx.hstack(
                            rx.icon("star", size=14, color=STAR),
                            rx.text(game.rating, size="2", weight="medium"),
                            spacing="1",
                            align="center",
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.heading(game.title, size="4", weight="bold"),
                    rx.text(game.platform, size="2", color=rx.color("gray", 11)),
                    rx.hstack(
                        rx.text("$", size="5", weight="bold", color=ACCENT),
                        rx.text(game.price, size="5", weight="bold", color=ACCENT),
                        width="100%",
                        align="center",
                    ),
                    spacing="2",
                    align="start",
                    padding="1rem",
                ),
                bg=rx.color("gray", 2),
                border=f"1px solid {rx.color('gray', 6)}",
                border_radius="0.75rem",
                overflow="hidden",
                width="100%",
            ),
            href="/game/" + game.id,
            text_decoration="none",
            color="inherit",
        ),
        rx.button(
            "Add to Cart",
            size="2",
            variant="soft",
            color_scheme="purple",
            width="100%",
            margin_top="0.5rem",
            on_click=CartState.add_to_cart(game.id),
        ),
        width="100%",
    )
