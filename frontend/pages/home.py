"""Home page with hero and featured games."""

import reflex as rx

from frontend.components.game_card import game_card_var
from full_stack_python.state import CatalogState, SiteState
from frontend.styles import ACCENT, ACCENT_HOVER, HERO_GLOW
from frontend.template import template


def category_link(category: rx.Var[str]) -> rx.Component:
    return rx.link(
        rx.box(
            rx.vstack(
                rx.icon("layers", size=28, color=ACCENT),
                rx.text(category, size="4", weight="bold"),
                rx.text("Browse titles", size="2", color=rx.color("gray", 11)),
                spacing="2",
                align="center",
            ),
            padding="1.5rem",
            bg=rx.color("gray", 2),
            border=f"1px solid {rx.color('gray', 6)}",
            border_radius="0.75rem",
            _hover={"border_color": ACCENT_HOVER},
        ),
        href="/shop?category=" + category,
        text_decoration="none",
        color="inherit",
    )


@rx.page(route="/", title="Nexus Games | Home", on_load=[CatalogState.load_catalog, SiteState.load_site])
@template
def home() -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.badge(SiteState.hero_badge, color_scheme="purple", size="2"),
                        rx.heading(
                            SiteState.hero_title,
                            size="9",
                            weight="bold",
                            text_align="center",
                        ),
                        rx.text(
                            SiteState.hero_subtitle,
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
                    background=HERO_GLOW,
                ),
                rx.cond(
                    CatalogState.featured_games.length() > 0,
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
                            rx.foreach(CatalogState.featured_games, game_card_var),
                            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                            spacing="5",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                ),
                rx.cond(
                    CatalogState.categories.length() > 0,
                    rx.vstack(
                        rx.heading("Shop by Category", size="7", weight="bold"),
                        rx.grid(
                            rx.foreach(CatalogState.categories, category_link),
                            columns=rx.breakpoints(initial="2", sm="3", lg="5"),
                            spacing="4",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                ),
                spacing="8",
                padding_y="2rem",
            ),
            size="4",
        ),
    )
