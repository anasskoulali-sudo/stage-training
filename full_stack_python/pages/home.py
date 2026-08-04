"""Home page with hero and featured games."""

import reflex as rx

from full_stack_python.components.game_card import game_card
from full_stack_python.components.layout import page_layout
from full_stack_python.data import CATEGORIES, get_featured_games


@rx.page(route="/", title="Nexus Games | Home")
def home() -> rx.Component:
    featured = get_featured_games()

    return page_layout(
        rx.box(
            rx.container(
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.badge("New releases every week", color_scheme="purple", size="2"),
                            rx.heading(
                                "Level Up Your Game Library",
                                size="9",
                                weight="bold",
                                text_align="center",
                            ),
                            rx.text(
                                "Discover blockbuster titles, indie gems, and everything in between. "
                                "One shop, every platform.",
                                size="5",
                                color=rx.color("gray", 11),
                                text_align="center",
                                max_width="40rem",
                            ),
                            rx.hstack(
                                rx.link(
                                    rx.button(
                                        rx.icon("gamepad-2", size=18),
                                        "Browse Shop",
                                        size="3",
                                        color_scheme="purple",
                                    ),
                                    href="/shop",
                                ),
                                rx.link(
                                    rx.button(
                                        "View Cart",
                                        size="3",
                                        variant="outline",
                                        color_scheme="purple",
                                    ),
                                    href="/cart",
                                ),
                                spacing="4",
                                justify="center",
                                flex_wrap="wrap",
                            ),
                            spacing="5",
                            align="center",
                            padding_y="4rem",
                        ),
                        width="100%",
                        background="radial-gradient(ellipse at top, rgba(124,58,237,0.2), transparent 60%)",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Featured Games", size="7", weight="bold"),
                            rx.spacer(),
                            rx.link(
                                rx.button("See all", variant="ghost", color_scheme="purple"),
                                href="/shop",
                            ),
                            width="100%",
                            align="center",
                        ),
                        rx.grid(
                            *[game_card(game) for game in featured[:6]],
                            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                            spacing="5",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.heading("Shop by Category", size="7", weight="bold"),
                        rx.grid(
                            *[
                                rx.link(
                                    rx.box(
                                        rx.vstack(
                                            rx.icon("layers", size=28, color="#a78bfa"),
                                            rx.text(category, size="4", weight="bold"),
                                            rx.text(
                                                "Browse titles",
                                                size="2",
                                                color=rx.color("gray", 11),
                                            ),
                                            spacing="2",
                                            align="center",
                                        ),
                                        padding="1.5rem",
                                        bg=rx.color("gray", 2),
                                        border=f"1px solid {rx.color('gray', 6)}",
                                        border_radius="0.75rem",
                                        _hover={"border_color": "#7c3aed"},
                                    ),
                                    href=f"/shop?category={category}",
                                    text_decoration="none",
                                    color="inherit",
                                )
                                for category in CATEGORIES
                            ],
                            columns=rx.breakpoints(initial="2", sm="3", lg="5"),
                            spacing="4",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    spacing="8",
                    padding_y="2rem",
                ),
                size="4",
            ),
        ),
    )
