"""Account login widget."""

import reflex as rx

from full_stack_python.state import AuthState


def account_widget() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon("user-circle", size=40, color="#a78bfa"),
                bg=rx.color("gray", 3),
                padding="1rem",
                border_radius="full",
            ),
            rx.heading("Sign In", size="6", weight="bold"),
            rx.text(
                "Use admin / admin for the admin dashboard, or any other credentials for a normal account.",
                size="2",
                color=rx.color("gray", 11),
                text_align="center",
            ),
            rx.cond(
                AuthState.login_error != "",
                rx.callout(
                    AuthState.login_error,
                    icon="triangle-alert",
                    color_scheme="red",
                    width="100%",
                ),
            ),
            rx.vstack(
                rx.text("Username", size="2", weight="medium"),
                rx.input(
                    placeholder="Enter username",
                    value=AuthState.username,
                    on_change=AuthState.set_username,
                    width="100%",
                    size="3",
                ),
                rx.text("Password", size="2", weight="medium"),
                rx.input(
                    placeholder="Enter password",
                    type="password",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                    width="100%",
                    size="3",
                ),
                spacing="2",
                width="100%",
                align="start",
            ),
            rx.button(
                rx.icon("log-in", size=18),
                "Sign In",
                size="3",
                color_scheme="purple",
                width="100%",
                on_click=AuthState.login,
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        max_width="24rem",
        width="100%",
        padding="2rem",
        bg=rx.color("gray", 2),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="1rem",
    )
