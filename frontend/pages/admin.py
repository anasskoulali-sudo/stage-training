"""Admin dashboard for store and site content management."""

import reflex as rx

from frontend.components.admin import categories_panel, games_panel, site_content_panel, support_panel
from full_stack_python.state import AdminState, AuthState, CatalogState, SiteState, SupportState
from frontend.template import template


@rx.page(
    route="/admin",
    title="Nexus Games | Admin Dashboard",
    on_load=[AuthState.guard_admin, CatalogState.load_catalog, SiteState.load_site, SupportState.load_tickets],
)
@template
def admin_dashboard() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.badge(
                        rx.cond(AuthState.is_superadmin, "Superadmin", "Admin"),
                        color_scheme="purple",
                    ),
                    rx.heading("Site Control Panel", size="8", weight="bold"),
                    rx.text(
                        rx.cond(
                            AuthState.is_superadmin,
                            "Edit site text, create categories and products, and manage support.",
                            "Edit site text and manage customer support.",
                        ),
                        size="3",
                        color=rx.color("gray", 11),
                    ),
                    spacing="2",
                    align="start",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.link(
                        rx.button("Preview Site", variant="soft", color_scheme="purple"),
                        href="/",
                    ),
                    rx.button(
                        rx.icon("log-out", size=16),
                        "Sign Out",
                        variant="outline",
                        color_scheme="red",
                        on_click=AuthState.logout,
                    ),
                    spacing="3",
                ),
                width="100%",
                align="center",
                flex_wrap="wrap",
            ),
            rx.grid(
                rx.box(
                    rx.text("Total Games", size="2", color=rx.color("gray", 11)),
                    rx.text(CatalogState.game_count, size="6", weight="bold"),
                    padding="1rem",
                    bg=rx.color("gray", 2),
                    border_radius="0.75rem",
                ),
                rx.box(
                    rx.text("Visible", size="2", color=rx.color("gray", 11)),
                    rx.text(CatalogState.visible_game_count, size="6", weight="bold"),
                    padding="1rem",
                    bg=rx.color("gray", 2),
                    border_radius="0.75rem",
                ),
                rx.box(
                    rx.text("Featured", size="2", color=rx.color("gray", 11)),
                    rx.text(CatalogState.featured_game_count, size="6", weight="bold"),
                    padding="1rem",
                    bg=rx.color("gray", 2),
                    border_radius="0.75rem",
                ),
                rx.box(
                    rx.text("Categories", size="2", color=rx.color("gray", 11)),
                    rx.text(CatalogState.category_count, size="6", weight="bold"),
                    padding="1rem",
                    bg=rx.color("gray", 2),
                    border_radius="0.75rem",
                ),
                rx.box(
                    rx.text("Open Tickets", size="2", color=rx.color("gray", 11)),
                    rx.text(SupportState.open_support_count, size="6", weight="bold"),
                    padding="1rem",
                    bg=rx.color("gray", 2),
                    border_radius="0.75rem",
                ),
                columns=rx.breakpoints(initial="2", md="5"),
                spacing="4",
                width="100%",
            ),
            rx.cond(
                AdminState.admin_message != "",
                rx.callout(
                    AdminState.admin_message,
                    icon="info",
                    color_scheme="purple",
                    width="100%",
                ),
            ),
            rx.cond(
                SupportState.admin_message != "",
                rx.callout(
                    SupportState.admin_message,
                    icon="info",
                    color_scheme="purple",
                    width="100%",
                ),
            ),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Site Content", value="site"),
                    rx.cond(
                        AuthState.is_superadmin,
                        rx.tabs.trigger("Categories", value="categories"),
                        rx.fragment(),
                    ),
                    rx.cond(
                        AuthState.is_superadmin,
                        rx.tabs.trigger("Games Catalog", value="games"),
                        rx.fragment(),
                    ),
                    rx.tabs.trigger("Customer Support", value="support"),
                ),
                rx.tabs.content(site_content_panel(), value="site"),
                rx.cond(
                    AuthState.is_superadmin,
                    rx.tabs.content(categories_panel(), value="categories"),
                    rx.fragment(),
                ),
                rx.cond(
                    AuthState.is_superadmin,
                    rx.tabs.content(games_panel(), value="games"),
                    rx.fragment(),
                ),
                rx.tabs.content(support_panel(), value="support"),
                default_value="site",
                width="100%",
            ),
            spacing="6",
            padding_y="2rem",
        ),
        size="4",
    )
