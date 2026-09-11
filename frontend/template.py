"""Shared page shell wrapping navbar, content, and footer."""

from collections.abc import Callable

import reflex as rx

from frontend.components.footer import footer
from frontend.components.navbar import navbar


def template(page: Callable[[], rx.Component]) -> Callable[[], rx.Component]:
    def wrapped() -> rx.Component:
        return rx.box(
            navbar(),
            rx.box(page(), flex="1", width="100%"),
            footer(),
            min_height="100vh",
            display="flex",
            flex_direction="column",
            bg=rx.color("gray", 1),
        )

    wrapped.__name__ = page.__name__
    wrapped.__module__ = page.__module__
    wrapped.__doc__ = page.__doc__
    return wrapped
