"""Individual game detail page."""

import reflex as rx

from full_stack_python.components.game_card import game_card_var
from full_stack_python.components.layout import page_layout
from full_stack_python.components.reviews_section import game_community_section
from full_stack_python.state import ShopState


@rx.page(route="/game/[game_id]", title="Nexus Games | Game Details")
def game_detail() -> rx.Component:
    return page_layout(
        rx.container(
            rx.cond(
                ShopState.current_game,
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
                                src=ShopState.current_game.image,
                                alt=ShopState.current_game.title,
                                width="100%",
                                height=rx.breakpoints(initial="220px", md="360px"),
                                object_fit="cover",
                                border_radius="1rem",
                            ),
                            rx.vstack(
                                rx.badge(
                                    ShopState.current_game.category,
                                    color_scheme="purple",
                                    size="2",
                                ),
                                rx.heading(
                                    ShopState.current_game.title,
                                    size="8",
                                    weight="bold",
                                ),
                                rx.hstack(
                                    rx.icon("star", size=18, color="#fbbf24"),
                                    rx.text(
                                        ShopState.current_game.rating,
                                        size="4",
                                        weight="medium",
                                    ),
                                    rx.text("·", color=rx.color("gray", 9)),
                                    rx.text(
                                        ShopState.current_game.platform,
                                        size="3",
                                        color=rx.color("gray", 11),
                                    ),
                                    spacing="2",
                                    align="center",
                                ),
                                rx.text(
                                    ShopState.current_game.description,
                                    size="4",
                                    color=rx.color("gray", 11),
                                    line_height="1.7",
                                ),
                                rx.hstack(
                                    rx.text("$", size="8", weight="bold", color="#a78bfa"),
                                    rx.text(
                                        ShopState.current_game.price,
                                        size="8",
                                        weight="bold",
                                        color="#a78bfa",
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
                                        on_click=ShopState.add_to_cart(ShopState.game_id),
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
                        ShopState.related_games.length() > 0,
                        rx.vstack(
                            rx.heading("You may also like", size="6", weight="bold"),
                            rx.grid(
                                rx.foreach(ShopState.related_games, game_card_var),
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
        ),
    )
