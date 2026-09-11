"""Site footer with store copy and category links."""

import reflex as rx

from full_stack_python.state import AuthState, CatalogState, SiteState


def footer() -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading(SiteState.store_name, size="5"),
                        rx.text(
                            SiteState.footer_description,
                            size="2",
                            color=rx.color("gray", 11),
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    rx.vstack(
                        rx.text("Quick Links", weight="bold", size="3"),
                        rx.link("Browse Shop", href="/shop", size="2"),
                        rx.link("Your Cart", href="/cart", size="2"),
                        rx.link("Your Account", href="/account", size="2"),
                        rx.cond(
                            AuthState.is_customer,
                            rx.link("Contact Us", href="/contact", size="2"),
                        ),
                        rx.link("About Us", href="/about", size="2"),
                        spacing="2",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Categories", weight="bold", size="3"),
                        rx.foreach(
                            CatalogState.categories,
                            lambda category: rx.link(
                                category + " Games",
                                href="/shop?category=" + category,
                                size="2",
                            ),
                        ),
                        spacing="2",
                        align="start",
                    ),
                    width="100%",
                    align="start",
                    spacing="6",
                    flex_wrap="wrap",
                ),
                rx.divider(),
                rx.text(
                    SiteState.copyright_text,
                    size="2",
                    color=rx.color("gray", 10),
                ),
                spacing="4",
                padding_y="3rem",
            ),
            size="4",
        ),
        bg=rx.color("gray", 2),
        border_top=f"1px solid {rx.color('gray', 6)}",
        margin_top="auto",
    )
