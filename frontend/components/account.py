"""Sign-in, sign-up, and signed-in profile widgets."""

import reflex as rx

from full_stack_python.state import AuthState
from frontend.styles import ACCENT


def _auth_card(*children: rx.Component) -> rx.Component:
    return rx.box(
        rx.vstack(
            *children,
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


def _field(label: str, **input_kwargs) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", weight="medium"),
        rx.input(width="100%", size="3", **input_kwargs),
        spacing="1",
        width="100%",
        align="start",
    )


def account_widget() -> rx.Component:
    return rx.cond(AuthState.show_signup, register_widget(), login_widget())


def login_widget() -> rx.Component:
    return _auth_card(
        rx.box(
            rx.icon("circle-user", size=40, color=ACCENT),
            bg=rx.color("gray", 3),
            padding="1rem",
            border_radius="full",
        ),
        rx.heading("Sign In", size="6", weight="bold"),
        rx.text(
            "Sign in with your shop username or email. Admins are redirected to the dashboard.",
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
            _field(
                "Username",
                placeholder="Enter username",
                value=AuthState.username,
                on_change=AuthState.set_username,
            ),
            _field(
                "Password",
                placeholder="Enter password",
                type="password",
                value=AuthState.password,
                on_change=AuthState.set_password,
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
        rx.text(
            "New here? ",
            rx.text(
                "Create an account",
                as_="span",
                color=ACCENT,
                cursor="pointer",
                on_click=AuthState.show_register_form,
            ),
            size="2",
            color=rx.color("gray", 11),
        ),
    )


def register_widget() -> rx.Component:
    return _auth_card(
        rx.box(
            rx.icon("user-plus", size=40, color=ACCENT),
            bg=rx.color("gray", 3),
            padding="1rem",
            border_radius="full",
        ),
        rx.heading("Create Account", size="6", weight="bold"),
        rx.text(
            "Join the shop. Your profile is saved to the client database.",
            size="2",
            color=rx.color("gray", 11),
            text_align="center",
        ),
        rx.cond(
            AuthState.register_error != "",
            rx.callout(
                AuthState.register_error,
                icon="triangle-alert",
                color_scheme="red",
                width="100%",
            ),
        ),
        rx.vstack(
            rx.hstack(
                _field(
                    "First name",
                    placeholder="Alex",
                    value=AuthState.register_first_name,
                    on_change=AuthState.set_register_first_name,
                ),
                _field(
                    "Last name",
                    placeholder="Martin",
                    value=AuthState.register_last_name,
                    on_change=AuthState.set_register_last_name,
                ),
                spacing="2",
                width="100%",
            ),
            _field(
                "Username",
                placeholder="Choose a username",
                value=AuthState.register_username,
                on_change=AuthState.set_register_username,
            ),
            _field(
                "Email",
                placeholder="you@email.com",
                type="email",
                value=AuthState.register_email,
                on_change=AuthState.set_register_email,
            ),
            _field(
                "Phone (optional)",
                placeholder="06 12 34 56 78",
                value=AuthState.register_phone,
                on_change=AuthState.set_register_phone,
            ),
            _field(
                "Password",
                placeholder="At least 8 characters",
                type="password",
                value=AuthState.register_password,
                on_change=AuthState.set_register_password,
            ),
            _field(
                "Confirm password",
                placeholder="Repeat password",
                type="password",
                value=AuthState.register_confirm,
                on_change=AuthState.set_register_confirm,
            ),
            spacing="2",
            width="100%",
            align="start",
        ),
        rx.button(
            rx.icon("user-plus", size=18),
            "Create Account",
            size="3",
            color_scheme="purple",
            width="100%",
            on_click=AuthState.register,
        ),
        rx.text(
            "Already have an account? ",
            rx.text(
                "Sign in",
                as_="span",
                color=ACCENT,
                cursor="pointer",
                on_click=AuthState.show_login_form,
            ),
            size="2",
            color=rx.color("gray", 11),
        ),
    )


def profile_widget() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon("circle-user", size=40, color=ACCENT),
                bg=rx.color("gray", 3),
                padding="1rem",
                border_radius="full",
            ),
            rx.heading("Welcome!", size="5", weight="bold"),
            rx.text(
                "Signed in as ",
                rx.text(AuthState.logged_in_user, weight="bold", as_="span"),
                size="2",
                color=rx.color("gray", 11),
                text_align="center",
            ),
            rx.cond(
                AuthState.is_admin,
                rx.link(
                    rx.button(
                        rx.icon("layout-dashboard", size=16),
                        "Admin Dashboard",
                        width="100%",
                        color_scheme="purple",
                    ),
                    href="/admin",
                    width="100%",
                ),
                rx.vstack(
                    rx.link(
                        rx.button("Browse Shop", variant="soft", color_scheme="purple", width="100%"),
                        href="/shop",
                        width="100%",
                    ),
                    rx.link(
                        rx.button("View Cart", variant="outline", color_scheme="purple", width="100%"),
                        href="/cart",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
            ),
            rx.button(
                rx.icon("log-out", size=16),
                "Sign Out",
                variant="outline",
                color_scheme="red",
                width="100%",
                on_click=AuthState.logout,
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        max_width="22rem",
        width="100%",
        padding="2rem",
        bg=rx.color("gray", 2),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="1rem",
    )
