"""Shared layout components: navbar, footer, page shell."""

import reflex as rx

from full_stack_python.state import ShopState


NAV_LINKS: list[tuple[str, str, str]] = [
    ("Home", "home", "/"),
    ("Shop", "gamepad-2", "/shop"),
    ("Cart", "shopping-cart", "/cart"),
    ("About", "info", "/about"),
]


def nav_link(text: str, icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text, size="3", weight="medium"),
            spacing="2",
            align="center",
        ),
        href=url,
        color=rx.color("gray", 12),
        _hover={"color": "#a78bfa"},
        text_decoration="none",
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.container(
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.box(
                            rx.icon("gamepad-2", size=28, color="white"),
                            bg="linear-gradient(135deg, #7c3aed, #4f46e5)",
                            padding="0.5rem",
                            border_radius="0.5rem",
                        ),
                        rx.vstack(
                            rx.text("Nexus Games", size="5", weight="bold"),
                            rx.text("Your gaming destination", size="1", color=rx.color("gray", 11)),
                            spacing="0",
                            align="start",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    href="/",
                    text_decoration="none",
                    color="inherit",
                ),
                rx.desktop_only(
                    rx.hstack(
                        *[nav_link(text, icon, url) for text, icon, url in NAV_LINKS],
                        spacing="6",
                        align="center",
                    ),
                ),
                rx.spacer(),
                rx.link(
                    rx.button(
                        rx.icon("shopping-cart", size=18),
                        rx.text(ShopState.cart_count),
                        "Cart",
                        variant="soft",
                        color_scheme="purple",
                    ),
                    href="/cart",
                ),
                rx.mobile_and_tablet(
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(rx.icon("menu", size=22), variant="ghost"),
                        ),
                        rx.menu.content(
                            *[
                                rx.menu.item(
                                    rx.link(
                                        rx.hstack(
                                            rx.icon(icon, size=16),
                                            rx.text(text),
                                            spacing="2",
                                        ),
                                        href=url,
                                        width="100%",
                                    ),
                                )
                                for text, icon, url in NAV_LINKS
                            ],
                        ),
                    ),
                ),
                width="100%",
                align="center",
                padding_y="0.75rem",
            ),
            size="4",
        ),
        bg=rx.color("gray", 1),
        border_bottom=f"1px solid {rx.color('gray', 6)}",
        position="sticky",
        top="0",
        z_index="50",
        backdrop_filter="blur(12px)",
    )


def footer() -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading("Nexus Games", size="5"),
                        rx.text(
                            "The best place to discover and buy video games.",
                            size="2",
                            color=rx.color("gray", 11),
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    rx.vstack(
                        rx.text("Quick Links", weight="bold", size="3"),
                        rx.link("Browse Shop", href="/shop", size="2"),
                        rx.link("Your Cart", href="/cart", size="2"),
                        rx.link("About Us", href="/about", size="2"),
                        spacing="2",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Categories", weight="bold", size="3"),
                        rx.link("RPG Games", href="/shop?category=RPG", size="2"),
                        rx.link("Action Games", href="/shop?category=Action", size="2"),
                        rx.link("Sports Games", href="/shop?category=Sports", size="2"),
                        spacing="2",
                        align="start",
                    ),
                    width="100%",
                    align="start",
                    spacing="6",
                    flex_wrap="wrap",
                ),
                rx.divider(),
                rx.text(
                    "© 2026 Nexus Games. Built with Reflex.",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                spacing="4",
                padding_y="3rem",
            ),
            size="4",
        ),
        bg=rx.color("gray", 2),
        border_top=f"1px solid {rx.color('gray', 6)}",
        margin_top="auto",
    )


def page_layout(*children: rx.Component) -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(*children, flex="1", width="100%"),
        footer(),
        min_height="100vh",
        display="flex",
        flex_direction="column",
        bg=rx.color("gray", 1),
    )
