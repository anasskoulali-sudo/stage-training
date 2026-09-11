"""About page for Nexus Games."""

import reflex as rx

from full_stack_python.state import CatalogState, SiteState
from frontend.styles import ACCENT
from frontend.template import template


@rx.page(
    route="/about",
    title="Nexus Games | About",
    on_load=[CatalogState.load_catalog, SiteState.load_site],
)
@template
def about() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading(SiteState.about_title, size="8", weight="bold"),
            rx.text(
                SiteState.about_description,
                size="4",
                color=rx.color("gray", 11),
                line_height="1.8",
                max_width="48rem",
            ),
            rx.grid(
                rx.box(
                    rx.icon("gamepad-2", size=32, color=ACCENT),
                    rx.heading(SiteState.about_feature_1_title, size="5"),
                    rx.text(
                        SiteState.about_feature_1_text,
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
                    rx.icon("shopping-cart", size=32, color=ACCENT),
                    rx.heading(SiteState.about_feature_2_title, size="5"),
                    rx.text(
                        SiteState.about_feature_2_text,
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
                    rx.icon("link", size=32, color=ACCENT),
                    rx.heading(SiteState.about_feature_3_title, size="5"),
                    rx.text(
                        SiteState.about_feature_3_text,
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
    )
