"""About page for Nexus Games."""

import reflex as rx

from full_stack_python.components.layout import page_layout


@rx.page(route="/about", title="Nexus Games | About")
def about() -> rx.Component:
    return page_layout(
        rx.container(
            rx.vstack(
                rx.heading("About Nexus Games", size="8", weight="bold"),
                rx.text(
                    "Nexus Games is a demo gaming shop built with Reflex — a full-stack Python "
                    "framework for modern web apps. Browse titles, add them to your cart, and "
                    "explore linked pages across the store.",
                    size="4",
                    color=rx.color("gray", 11),
                    line_height="1.8",
                    max_width="48rem",
                ),
                rx.grid(
                    rx.box(
                        rx.icon("gamepad-2", size=32, color="#a78bfa"),
                        rx.heading("Curated Catalog", size="5"),
                        rx.text(
                            "Hand-picked games across RPG, action, sports, and more.",
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
                        rx.heading("Smart Cart", size="5"),
                        rx.text(
                            "Add games from any page and manage quantities in your cart.",
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
                        rx.heading("Connected Pages", size="5"),
                        rx.text(
                            "Home, shop, game details, cart, and about — all linked together.",
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
