"""Reviews and comments section for game detail pages."""

import reflex as rx

from full_stack_python.state import AuthState, GameComment, GameReview, ShopState


def review_row(review: rx.Var[GameReview]) -> rx.Component:
    is_owner = AuthState.logged_in_user == review.author
    is_editing = ShopState.editing_review_id == review.id.to(str)

    return rx.box(
        rx.cond(
            is_editing,
            rx.vstack(
                rx.hstack(
                    rx.text("Rating (1-5)", size="2"),
                    rx.input(
                        value=ShopState.edit_review_rating,
                        on_change=ShopState.set_edit_review_rating,
                        width="4rem",
                        size="2",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.text_area(
                    value=ShopState.edit_review_text,
                    on_change=ShopState.set_edit_review_text,
                    width="100%",
                    rows="3",
                ),
                rx.hstack(
                    rx.button(
                        "Save",
                        size="2",
                        color_scheme="purple",
                        on_click=ShopState.save_review_edit(review.id),
                    ),
                    rx.button(
                        "Cancel",
                        size="2",
                        variant="outline",
                        on_click=ShopState.cancel_review_edit,
                    ),
                    spacing="2",
                ),
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.icon("user", size=14),
                        rx.text(review.author, weight="bold", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.icon("star", size=14, color="#fbbf24"),
                        rx.text(review.rating, size="2", weight="medium"),
                        spacing="1",
                        align="center",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.text(review.text, size="3", color=rx.color("gray", 11)),
                rx.cond(
                    is_owner,
                    rx.hstack(
                        rx.button(
                            rx.icon("pencil", size=12),
                            "Edit",
                            size="1",
                            variant="soft",
                            on_click=ShopState.start_edit_review(review.id),
                        ),
                        rx.button(
                            rx.icon("trash-2", size=12),
                            "Delete",
                            size="1",
                            variant="soft",
                            color_scheme="red",
                            on_click=ShopState.delete_review(review.id),
                        ),
                        spacing="2",
                    ),
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
        ),
        padding="1rem",
        bg=rx.color("gray", 2),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="0.75rem",
        width="100%",
    )


def comment_row(comment: rx.Var[GameComment]) -> rx.Component:
    is_owner = AuthState.logged_in_user == comment.author
    is_editing = ShopState.editing_comment_id == comment.id.to(str)

    return rx.box(
        rx.cond(
            is_editing,
            rx.vstack(
                rx.text_area(
                    value=ShopState.edit_comment_text,
                    on_change=ShopState.set_edit_comment_text,
                    width="100%",
                    rows="2",
                ),
                rx.hstack(
                    rx.button(
                        "Save",
                        size="2",
                        color_scheme="purple",
                        on_click=ShopState.save_comment_edit(comment.id),
                    ),
                    rx.button(
                        "Cancel",
                        size="2",
                        variant="outline",
                        on_click=ShopState.cancel_comment_edit,
                    ),
                    spacing="2",
                ),
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.icon("message-circle", size=14, color="#a78bfa"),
                        rx.text(comment.author, weight="bold", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.cond(
                        is_owner,
                        rx.hstack(
                            rx.icon_button(
                                rx.icon("pencil", size=12),
                                size="1",
                                variant="ghost",
                                on_click=ShopState.start_edit_comment(comment.id),
                            ),
                            rx.icon_button(
                                rx.icon("trash-2", size=12),
                                size="1",
                                variant="ghost",
                                color_scheme="red",
                                on_click=ShopState.delete_comment(comment.id),
                            ),
                            spacing="1",
                        ),
                    ),
                    width="100%",
                    align="center",
                ),
                rx.text(comment.text, size="3", color=rx.color("gray", 11)),
                spacing="2",
                align="start",
                width="100%",
            ),
        ),
        padding="1rem",
        bg=rx.color("gray", 2),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="0.75rem",
        width="100%",
    )


def review_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Write a Review", size="4", weight="bold"),
            rx.cond(
                AuthState.is_logged_in,
                rx.vstack(
                    rx.hstack(
                        rx.text("Your rating", size="2", weight="medium"),
                        rx.select(
                            ["1", "2", "3", "4", "5"],
                            value=ShopState.new_review_rating,
                            on_change=ShopState.set_new_review_rating,
                            size="2",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.text_area(
                        placeholder="Share your thoughts about this game...",
                        value=ShopState.new_review_text,
                        on_change=ShopState.set_new_review_text,
                        width="100%",
                        rows="3",
                    ),
                    rx.button(
                        rx.icon("star", size=16),
                        "Post Review",
                        color_scheme="purple",
                        on_click=ShopState.submit_review,
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.callout(
                    "Sign in from your account page to leave a review.",
                    icon="user",
                    color_scheme="purple",
                    width="100%",
                ),
            ),
            spacing="3",
            width="100%",
        ),
        padding="1.25rem",
        bg=rx.color("gray", 2),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="0.75rem",
        width="100%",
    )


def comment_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Join the Discussion", size="4", weight="bold"),
            rx.cond(
                AuthState.is_logged_in,
                rx.vstack(
                    rx.text_area(
                        placeholder="Ask a question or share a tip...",
                        value=ShopState.new_comment_text,
                        on_change=ShopState.set_new_comment_text,
                        width="100%",
                        rows="2",
                    ),
                    rx.button(
                        rx.icon("send", size=16),
                        "Post Comment",
                        color_scheme="purple",
                        on_click=ShopState.submit_comment,
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.callout(
                    "Sign in to post a comment.",
                    icon="message-circle",
                    color_scheme="purple",
                    width="100%",
                ),
            ),
            spacing="3",
            width="100%",
        ),
        padding="1.25rem",
        bg=rx.color("gray", 2),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="0.75rem",
        width="100%",
    )


def game_reviews_section() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Player Reviews", size="6", weight="bold"),
            rx.spacer(),
            rx.badge(
                ShopState.current_game_review_count,
                " reviews",
                color_scheme="purple",
                variant="soft",
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            ShopState.review_message != "",
            rx.callout(
                ShopState.review_message,
                icon="info",
                color_scheme="green",
                width="100%",
            ),
        ),
        review_form(),
        rx.cond(
            ShopState.current_game_reviews.length() > 0,
            rx.vstack(
                rx.foreach(ShopState.current_game_reviews, review_row),
                spacing="3",
                width="100%",
            ),
            rx.center(
                rx.text(
                    "No reviews yet. Be the first to share your opinion!",
                    size="3",
                    color=rx.color("gray", 11),
                ),
                padding_y="1rem",
            ),
        ),
        spacing="4",
        width="100%",
    )


def game_comments_section() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Comments", size="6", weight="bold"),
            rx.spacer(),
            rx.badge(
                ShopState.current_game_comment_count,
                " comments",
                color_scheme="purple",
                variant="soft",
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            ShopState.comment_message != "",
            rx.callout(
                ShopState.comment_message,
                icon="info",
                color_scheme="green",
                width="100%",
            ),
        ),
        comment_form(),
        rx.cond(
            ShopState.current_game_comments.length() > 0,
            rx.vstack(
                rx.foreach(ShopState.current_game_comments, comment_row),
                spacing="3",
                width="100%",
            ),
            rx.center(
                rx.text(
                    "No comments yet. Start the conversation!",
                    size="3",
                    color=rx.color("gray", 11),
                ),
                padding_y="1rem",
            ),
        ),
        spacing="4",
        width="100%",
    )


def game_community_section() -> rx.Component:
    return rx.vstack(
        game_reviews_section(),
        rx.divider(),
        game_comments_section(),
        spacing="6",
        width="100%",
        padding="1.5rem",
        bg=rx.color("gray", 1),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="1rem",
    )
