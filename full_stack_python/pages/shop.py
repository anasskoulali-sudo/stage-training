"""Shop catalog page with search and filters."""

import reflex as rx

from full_stack_python.components.game_card import game_card_var
from full_stack_python.components.layout import page_layout
from full_stack_python.state import ShopState


def category_button(category: str) -> rx.Component:
    is_active = ShopState.selected_category == category
    return rx.button(
        category,
        size="2",
        variant=rx.cond(is_active, "solid", "soft"),
        color_scheme="purple",
        on_click=ShopState.set_category(category),
    )


def category_button_var(category: rx.Var[str]) -> rx.Component:
    is_active = ShopState.selected_category == category
    return rx.button(
        category,
        size="2",
        variant=rx.cond(is_active, "solid", "soft"),
        color_scheme="purple",
        on_click=ShopState.set_category(category),
    )


@rx.page(route="/shop", title="Nexus Games | Shop", on_load=ShopState.on_load_shop)
def shop() -> rx.Component:
    return page_layout(
        rx.container(
            rx.vstack(
                rx.vstack(
                    rx.heading(ShopState.shop_title, size="8", weight="bold"),
                    rx.text(
                        ShopState.shop_subtitle,
                        size="4",
                        color=rx.color("gray", 11),
                    ),
                    spacing="2",
                    align="start",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Search games...",
                        value=ShopState.search_query,
                        on_change=ShopState.set_search,
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
                    rx.foreach(ShopState.categories, category_button_var),
                    spacing="2",
                    flex_wrap="wrap",
                    width="100%",
                ),
                rx.cond(
                    ShopState.filtered_games.length() > 0,
                    rx.grid(
                        rx.foreach(ShopState.filtered_games, game_card_var),
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
        ),
    )
