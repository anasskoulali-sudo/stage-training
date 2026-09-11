"""Shop catalog page with search and filters."""

import reflex as rx

from frontend.components.game_card import game_card_var
from full_stack_python.state import CatalogState, SiteState
from frontend.template import template


def category_button(category: str) -> rx.Component:
    is_active = CatalogState.selected_category == category
    return rx.button(
        category,
        size="2",
        variant=rx.cond(is_active, "solid", "soft"),
        color_scheme="purple",
        on_click=CatalogState.set_category(category),
    )


def category_button_var(category: rx.Var[str]) -> rx.Component:
    is_active = CatalogState.selected_category == category
    return rx.button(
        category,
        size="2",
        variant=rx.cond(is_active, "solid", "soft"),
        color_scheme="purple",
        on_click=CatalogState.set_category(category),
    )


@rx.page(
    route="/shop",
    title="Nexus Games | Shop",
    on_load=[CatalogState.on_load_shop, SiteState.load_site],
)
@template
def shop() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.vstack(
                rx.heading(SiteState.shop_title, size="8", weight="bold"),
                rx.text(
                    SiteState.shop_subtitle,
                    size="4",
                    color=rx.color("gray", 11),
                ),
                spacing="2",
                align="start",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Search games...",
                    value=CatalogState.search_query,
                    on_change=CatalogState.set_search,
                    width=rx.breakpoints(initial="100%", md="24rem"),
                    size="3",
                ),
                rx.link(
                    rx.button(
                        rx.icon("shopping-cart", size=16),
                        "Go to Cart",
                        variant="outline",
                        color_scheme="purple",
                    ),
                    href="/cart",
                ),
                spacing="3",
                width="100%",
                flex_wrap="wrap",
            ),
            rx.hstack(
                category_button("All"),
                rx.foreach(CatalogState.categories, category_button_var),
                spacing="2",
                flex_wrap="wrap",
                width="100%",
            ),
            rx.cond(
                CatalogState.filtered_games.length() > 0,
                rx.grid(
                    rx.foreach(CatalogState.filtered_games, game_card_var),
                    columns=rx.breakpoints(initial="1", sm="2", lg="3", xl="4"),
                    spacing="5",
                    width="100%",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("search-x", size=48, color=rx.color("gray", 9)),
                        rx.text("No games match your search.", size="4"),
                        rx.link(
                            rx.button("Clear filters", variant="soft"),
                            href="/shop",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    padding_y="4rem",
                ),
            ),
            spacing="6",
            padding_y="2rem",
        ),
        size="4",
    )
