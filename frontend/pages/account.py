"""Account page with login widget and customer profile."""

import reflex as rx

from frontend.components.account import account_widget, profile_widget
from frontend.components.community import comment_row, review_row
from full_stack_python.models import GameComment, GameReview
from full_stack_python.state import AuthState, CartState, CatalogState, CommunityState, SiteState
from frontend.styles import ACCENT
from frontend.template import template


def account_sidebar_info() -> rx.Component:
    return rx.vstack(
        rx.heading("Your Account", size="8", weight="bold"),
        rx.text(
            "Create an account or sign in to access your cart, leave reviews, and join game discussions.",
            size="4",
            color=rx.color("gray", 11),
            line_height="1.7",
        ),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("star", size=20, color=ACCENT),
                    rx.text("Rate games you've played", size="3"),
                    spacing="2",
                    align="center",
                ),
                rx.hstack(
                    rx.icon("message-circle", size=20, color=ACCENT),
                    rx.text("Comment on game pages", size="3"),
                    spacing="2",
                    align="center",
                ),
                rx.hstack(
                    rx.icon("pencil", size=20, color=ACCENT),
                    rx.text("Edit or delete your own posts", size="3"),
                    spacing="2",
                    align="center",
                ),
                spacing="3",
                align="start",
            ),
            padding="1.25rem",
            bg=rx.color("gray", 2),
            border=f"1px solid {rx.color('gray', 6)}",
            border_radius="0.75rem",
            width="100%",
        ),
        spacing="5",
        align="start",
        flex="1",
        min_width="0",
    )


def user_review_summary(review: rx.Var[GameReview]) -> rx.Component:
    return rx.cond(
        AuthState.logged_in_user == review.author,
        review_row(review),
    )


def user_comment_summary(comment: rx.Var[GameComment]) -> rx.Component:
    return rx.cond(
        AuthState.logged_in_user == comment.author,
        comment_row(comment),
    )


def user_main_content() -> rx.Component:
    return rx.vstack(
        rx.grid(
            rx.box(
                rx.icon("shopping-cart", size=24, color=ACCENT),
                rx.text("Cart Items", size="2", color=rx.color("gray", 11)),
                rx.text(CartState.cart_count, size="6", weight="bold"),
                spacing="2",
                align="start",
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            rx.box(
                rx.icon("wallet", size=24, color=ACCENT),
                rx.text("Cart Total", size="2", color=rx.color("gray", 11)),
                rx.text("$", CartState.cart_total, size="6", weight="bold"),
                spacing="2",
                align="start",
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
        rx.box(
            rx.vstack(
                rx.heading("Your Reviews", size="5", weight="bold"),
                rx.foreach(CommunityState.reviews, user_review_summary),
                rx.text(
                    "Visit any game page to write a new review.",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                spacing="3",
                align="start",
                width="100%",
            ),
            padding="1.25rem",
            bg=rx.color("gray", 2),
            border=f"1px solid {rx.color('gray', 6)}",
            border_radius="0.75rem",
            width="100%",
        ),
        rx.box(
            rx.vstack(
                rx.heading("Your Comments", size="5", weight="bold"),
                rx.foreach(CommunityState.comments, user_comment_summary),
                rx.text(
                    "Open a game page to join the discussion.",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                spacing="3",
                align="start",
                width="100%",
            ),
            padding="1.25rem",
            bg=rx.color("gray", 2),
            border=f"1px solid {rx.color('gray', 6)}",
            border_radius="0.75rem",
            width="100%",
        ),
        spacing="5",
        width="100%",
        flex="1",
        min_width="0",
    )


def account_right_panel() -> rx.Component:
    return rx.box(
        rx.cond(
            AuthState.is_logged_in,
            profile_widget(),
            account_widget(),
        ),
        width=rx.breakpoints(initial="100%", md="22rem"),
        min_width="18rem",
        flex_shrink="0",
        margin_left=rx.breakpoints(initial="0", md="auto"),
        position=rx.breakpoints(initial="relative", md="sticky"),
        top="6rem",
        align_self="flex-start",
    )


@rx.page(
    route="/account",
    title="Nexus Games | Account",
    on_load=[CatalogState.load_catalog, SiteState.load_site, CommunityState.load_community],
)
@template
def account() -> rx.Component:
    return rx.container(
        rx.hstack(
            rx.cond(
                AuthState.is_logged_in,
                rx.cond(
                    AuthState.is_admin,
                    rx.vstack(
                        rx.heading("Admin Account", size="8", weight="bold"),
                        rx.text(
                            "Manage the store from the dashboard. Your account panel is on the right.",
                            size="4",
                            color=rx.color("gray", 11),
                        ),
                        spacing="4",
                        align="start",
                        flex="1",
                        min_width="0",
                    ),
                    user_main_content(),
                ),
                account_sidebar_info(),
            ),
            account_right_panel(),
            spacing="8",
            align="start",
            width="100%",
            flex_wrap=rx.breakpoints(initial="wrap", md="nowrap"),
            justify="between",
        ),
        padding_y="3rem",
        size="4",
    )
