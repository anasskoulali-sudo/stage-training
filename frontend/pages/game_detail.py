"""Individual game detail page."""

import reflex as rx

from frontend.components.community import game_community_section
from frontend.components.game_card import game_card_var
from full_stack_python.state import CartState, CatalogState, CommunityState, SiteState
from frontend.styles import ACCENT, STAR
from frontend.template import template


@rx.page(
    route="/game/[game_id]",
    title="Nexus Games | Game Details",
    on_load=[CatalogState.load_catalog, SiteState.load_site, CommunityState.load_community],
)
@template
def game_detail() -> rx.Component:
    return rx.container(
        rx.cond(
            CatalogState.current_game,
            rx.vstack(
                rx.link(
                    rx.hstack(
                        rx.icon("arrow-left", size=16),
                        rx.text("Back to Shop"),
                        spacing="2",
                        align="center",
                    ),
                    href="/shop",
                    color=rx.color("gray", 11),
                    margin_bottom="1rem",
                ),
                rx.box(
                    rx.grid(
                        rx.image(
                            src=CatalogState.current_game.image,
                            alt=CatalogState.current_game.title,
                            width="100%",
                            height=rx.breakpoints(initial="220px", md="360px"),
                            object_fit="cover",
                            border_radius="1rem",
                        ),
                        rx.vstack(
                            rx.badge(
                                CatalogState.current_game.category,
                                color_scheme="purple",
                                size="2",
                            ),
                            rx.heading(
                                CatalogState.current_game.title,
                                size="8",
                                weight="bold",
                            ),
                            rx.hstack(
                                rx.icon("star", size=18, color=STAR),
                                rx.text(
                                    CatalogState.current_game.rating,
                                    size="4",
                                    weight="medium",
                                ),
                                rx.text("·", color=rx.color("gray", 9)),
                                rx.text(
                                    CatalogState.current_game.platform,
                                    size="3",
                                    color=rx.color("gray", 11),
                                ),
                                spacing="2",
                                align="center",
                            ),
                            rx.text(
                                CatalogState.current_game.description,
                                size="4",
                                color=rx.color("gray", 11),
                                line_height="1.7",
                            ),
                            rx.hstack(
                                rx.text("$", size="8", weight="bold", color=ACCENT),
                                rx.text(
                                    CatalogState.current_game.price,
                                    size="8",
                                    weight="bold",
                                    color=ACCENT,
                                ),
                                spacing="1",
                                align="center",
                            ),
                            rx.hstack(
                                rx.button(
                                    rx.icon("shopping-cart", size=18),
                                    "Add to Cart",
                                    size="3",
                                    color_scheme="purple",
                                    on_click=CartState.add_to_cart(CatalogState.game_id),
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
                                spacing="3",
                                flex_wrap="wrap",
                            ),
                            spacing="4",
                            align="start",
                        ),
                        columns=rx.breakpoints(initial="1", md="2"),
                        spacing="6",
                        width="100%",
                    ),
                    width="100%",
                ),
                game_community_section(),
                rx.cond(
                    CatalogState.related_games.length() > 0,
                    rx.vstack(
                        rx.heading("You may also like", size="6", weight="bold"),
                        rx.grid(
                            rx.foreach(CatalogState.related_games, game_card_var),
                            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                            spacing="5",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                ),
                spacing="6",
                padding_y="2rem",
            ),
            rx.center(
                rx.vstack(
                    rx.icon("ghost", size=48, color=rx.color("gray", 9)),
                    rx.heading("Game not found", size="6"),
                    rx.text("This title isn't in our catalog.", color=rx.color("gray", 11)),
                    rx.link(
                        rx.button("Back to Shop", color_scheme="purple"),
                        href="/shop",
                    ),
                    spacing="4",
                    align="center",
                ),
                padding_y="6rem",
            ),
        ),
        size="4",
    )
