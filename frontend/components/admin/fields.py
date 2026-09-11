"""Shared form fields for the admin dashboard."""

import reflex as rx


def admin_field(label: str, value, on_change, placeholder: str = "") -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", weight="medium"),
        rx.input(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            width="100%",
            size="2",
        ),
        spacing="1",
        width="100%",
        align="start",
    )


def admin_textarea(label: str, value, on_change, placeholder: str = "") -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", weight="medium"),
        rx.text_area(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            width="100%",
            rows="3",
        ),
        spacing="1",
        width="100%",
        align="start",
    )
