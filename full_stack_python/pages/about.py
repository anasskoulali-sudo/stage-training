"""About page for Nexus Games."""

import reflex as rx

from full_stack_python.components.layout import page_layout
from full_stack_python.state import ShopState


@rx.page(route="/about", title="Nexus Games | About")
def about() -> rx.Component:
    return page_layout(
        rx.container(
            rx.vstack(
                rx.heading(ShopState.about_title, size="8", weight="bold"),
                rx.text(
                    ShopState.about_description,
                    size="4",
                    color=rx.color("gray", 11),
                    line_height="1.8",
                    max_width="48rem",
                ),
                rx.grid(
                    rx.box(
                        rx.icon("gamepad-2", size=32, color="#a78bfa"),
                        rx.heading(ShopState.about_feature_1_title, size="5"),
                        rx.text(
                            ShopState.about_feature_1_text,
                            size="3",
                            color=rx.color("gray", 11),
                        ),
                        spacing="3",
                        align="start",
                        padding="1.5rem",
                        bg=rx.color("gray", 2),
                        border_radius="0.75rem",
                    ),
                    rx.box(
                        rx.icon("shopping-cart", size=32, color="#a78bfa"),
                        rx.heading(ShopState.about_feature_2_title, size="5"),
                        rx.text(
                            ShopState.about_feature_2_text,
                            size="3",
                            color=rx.color("gray", 11),
                        ),
                        spacing="3",
                        align="start",
                        padding="1.5rem",
                        bg=rx.color("gray", 2),
                        border_radius="0.75rem",
                    ),
                    rx.box(
                        rx.icon("link", size=32, color="#a78bfa"),
                        rx.heading(ShopState.about_feature_3_title, size="5"),
                        rx.text(
                            ShopState.about_feature_3_text,
                            size="3",
                            color=rx.color("gray", 11),
                        ),
                        spacing="3",
                        align="start",
                        padding="1.5rem",
                        bg=rx.color("gray", 2),
                        border_radius="0.75rem",
                    ),
                    columns=rx.breakpoints(initial="1", md="3"),
                    spacing="5",
                    width="100%",
                ),
                rx.box(
                    rx.vstack(
                        rx.heading("Explore the Store", size="6", weight="bold"),
                        rx.hstack(
                            rx.link(
                                rx.button("Home", variant="soft", color_scheme="purple"),
                                href="/",
                            ),
                            rx.link(
                                rx.button("Shop", variant="soft", color_scheme="purple"),
                                href="/shop",
                            ),
                            rx.link(
                                rx.button("Cart", variant="soft", color_scheme="purple"),
                                href="/cart",
                            ),
                            spacing="3",
                            flex_wrap="wrap",
                        ),
                        spacing="4",
                        align="start",
                    ),
                    padding="1.5rem",
                    bg=rx.color("gray", 2),
                    border=f"1px solid {rx.color('gray', 6)}",
                    border_radius="0.75rem",
                    width="100%",
                ),
                spacing="6",
                padding_y="2rem",
            ),
            size="4",
        ),
    )
