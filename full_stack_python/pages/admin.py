"""Admin dashboard for store and site content management."""

import reflex as rx

from full_stack_python.components.layout import page_layout
from full_stack_python.data import Game
from full_stack_python.state import AuthState, ShopState, SupportTicket


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


def site_content_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Site Content", size="6", weight="bold"),
        rx.text(
            "Changes apply instantly across the public site.",
            size="2",
            color=rx.color("gray", 11),
        ),
        rx.grid(
            rx.box(
                rx.vstack(
                    rx.heading("Store Branding", size="4", weight="bold"),
                    admin_field("Store Name", ShopState.store_name, ShopState.set_store_name),
                    admin_field("Tagline", ShopState.store_tagline, ShopState.set_store_tagline),
                    admin_textarea(
                        "Footer Description",
                        ShopState.footer_description,
                        ShopState.set_footer_description,
                    ),
                    admin_field(
                        "Copyright Text",
                        ShopState.copyright_text,
                        ShopState.set_copyright_text,
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            rx.box(
                rx.vstack(
                    rx.heading("Home Page Hero", size="4", weight="bold"),
                    admin_field("Badge Text", ShopState.hero_badge, ShopState.set_hero_badge),
                    admin_field("Hero Title", ShopState.hero_title, ShopState.set_hero_title),
                    admin_textarea(
                        "Hero Subtitle",
                        ShopState.hero_subtitle,
                        ShopState.set_hero_subtitle,
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            rx.box(
                rx.vstack(
                    rx.heading("Shop Page", size="4", weight="bold"),
                    admin_field("Shop Title", ShopState.shop_title, ShopState.set_shop_title),
                    admin_textarea(
                        "Shop Subtitle",
                        ShopState.shop_subtitle,
                        ShopState.set_shop_subtitle,
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            rx.box(
                rx.vstack(
                    rx.heading("About Page", size="4", weight="bold"),
                    admin_field("About Title", ShopState.about_title, ShopState.set_about_title),
                    admin_textarea(
                        "About Description",
                        ShopState.about_description,
                        ShopState.set_about_description,
                    ),
                    admin_field(
                        "Feature 1 Title",
                        ShopState.about_feature_1_title,
                        ShopState.set_about_feature_1_title,
                    ),
                    admin_textarea(
                        "Feature 1 Text",
                        ShopState.about_feature_1_text,
                        ShopState.set_about_feature_1_text,
                    ),
                    admin_field(
                        "Feature 2 Title",
                        ShopState.about_feature_2_title,
                        ShopState.set_about_feature_2_title,
                    ),
                    admin_textarea(
                        "Feature 2 Text",
                        ShopState.about_feature_2_text,
                        ShopState.set_about_feature_2_text,
                    ),
                    admin_field(
                        "Feature 3 Title",
                        ShopState.about_feature_3_title,
                        ShopState.set_about_feature_3_title,
                    ),
                    admin_textarea(
                        "Feature 3 Text",
                        ShopState.about_feature_3_text,
                        ShopState.set_about_feature_3_text,
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            columns="1",
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


def game_form_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    rx.cond(ShopState.is_editing_game, "Edit Game", "Add New Game"),
                    size="5",
                    weight="bold",
                ),
                rx.spacer(),
                rx.button(
                    "New Game",
                    variant="soft",
                    size="2",
                    on_click=ShopState.start_new_game,
                ),
                width="100%",
                align="center",
            ),
            rx.grid(
                admin_field("Title", ShopState.form_title, ShopState.set_form_title, "Game title"),
                admin_field("Price", ShopState.form_price, ShopState.set_form_price, "59.99"),
                admin_field("Category", ShopState.form_category, ShopState.set_form_category, "RPG"),
                admin_field(
                    "Platform",
                    ShopState.form_platform,
                    ShopState.set_form_platform,
                    "PC / PlayStation / Xbox",
                ),
                admin_field("Rating", ShopState.form_rating, ShopState.set_form_rating, "4.5"),
                admin_field(
                    "Image URL",
                    ShopState.form_image,
                    ShopState.set_form_image,
                    "https://...",
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="3",
                width="100%",
            ),
            admin_textarea(
                "Description",
                ShopState.form_description,
                ShopState.set_form_description,
                "Game description...",
            ),
            rx.hstack(
                rx.checkbox(
                    "Featured on home page",
                    checked=ShopState.form_featured,
                    on_change=ShopState.set_form_featured,
                ),
                rx.checkbox(
                    "Visible on site",
                    checked=ShopState.form_visible,
                    on_change=ShopState.set_form_visible,
                ),
                spacing="4",
                flex_wrap="wrap",
            ),
            rx.button(
                rx.icon("save", size=16),
                rx.cond(ShopState.is_editing_game, "Save Changes", "Add Game"),
                color_scheme="purple",
                on_click=ShopState.save_game,
            ),
            spacing="4",
            width="100%",
        ),
        padding="1.25rem",
        bg=rx.color("gray", 2),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="0.75rem",
        width="100%",
    )


def admin_game_row(game: rx.Var[Game]) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.vstack(
                rx.text(game.title, weight="medium"),
                rx.text(game.id, size="1", color=rx.color("gray", 10)),
                spacing="0",
                align="start",
            ),
        ),
        rx.table.cell(game.category),
        rx.table.cell(rx.text("$", game.price)),
        rx.table.cell(
            rx.cond(
                game.featured,
                rx.badge("Featured", color_scheme="amber"),
                rx.badge("Standard", variant="soft"),
            ),
        ),
        rx.table.cell(
            rx.cond(
                game.visible,
                rx.badge("Visible", color_scheme="green"),
                rx.badge("Hidden", color_scheme="red"),
            ),
        ),
        rx.table.cell(
            rx.hstack(
                rx.icon_button(
                    rx.icon("pencil", size=14),
                    size="1",
                    variant="soft",
                    on_click=ShopState.load_game_for_edit(game.id),
                ),
                rx.icon_button(
                    rx.icon("star", size=14),
                    size="1",
                    variant="soft",
                    on_click=ShopState.toggle_featured(game.id),
                ),
                rx.icon_button(
                    rx.icon("eye", size=14),
                    size="1",
                    variant="soft",
                    on_click=ShopState.toggle_visible(game.id),
                ),
                rx.icon_button(
                    rx.icon("trash-2", size=14),
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=ShopState.delete_game(game.id),
                ),
                spacing="1",
            ),
        ),
    )


def games_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Games Catalog", size="6", weight="bold"),
            rx.spacer(),
            rx.button(
                rx.icon("plus", size=16),
                "Add Game",
                color_scheme="purple",
                on_click=ShopState.start_new_game,
            ),
            width="100%",
            align="center",
        ),
        game_form_panel(),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Title"),
                        rx.table.column_header_cell("Category"),
                        rx.table.column_header_cell("Price"),
                        rx.table.column_header_cell("Featured"),
                        rx.table.column_header_cell("Status"),
                        rx.table.column_header_cell("Actions"),
                    ),
                ),
                rx.table.body(rx.foreach(ShopState.games, admin_game_row)),
                width="100%",
            ),
            padding="1rem",
            bg=rx.color("gray", 2),
            border=f"1px solid {rx.color('gray', 6)}",
            border_radius="0.75rem",
            width="100%",
            overflow_x="auto",
        ),
        spacing="4",
        width="100%",
    )


def admin_support_row(ticket: rx.Var[SupportTicket]) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.vstack(
                rx.text(ticket.author, weight="medium"),
                rx.text(ticket.created_at, size="1", color=rx.color("gray", 10)),
                spacing="0",
                align="start",
            ),
        ),
        rx.table.cell(ticket.subject),
        rx.table.cell(rx.badge(ticket.category, color_scheme="purple", variant="soft")),
        rx.table.cell(
            rx.match(
                ticket.status,
                ("Open", rx.badge("Open", color_scheme="red")),
                ("In Progress", rx.badge("In Progress", color_scheme="amber")),
                ("Resolved", rx.badge("Resolved", color_scheme="green")),
                rx.badge(ticket.status),
            ),
        ),
        rx.table.cell(
            rx.text(
                ticket.message,
                size="2",
                color=rx.color("gray", 11),
                max_width="20rem",
            ),
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "Open",
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=ShopState.set_ticket_status(ticket.id, "Open"),
                ),
                rx.button(
                    "Progress",
                    size="1",
                    variant="soft",
                    color_scheme="amber",
                    on_click=ShopState.set_ticket_status(ticket.id, "In Progress"),
                ),
                rx.button(
                    "Resolved",
                    size="1",
                    variant="soft",
                    color_scheme="green",
                    on_click=ShopState.set_ticket_status(ticket.id, "Resolved"),
                ),
                spacing="1",
                flex_wrap="wrap",
            ),
        ),
    )


def support_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Customer Support", size="6", weight="bold"),
                rx.text(
                    "View and manage support requests from customers.",
                    size="2",
                    color=rx.color("gray", 11),
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.badge(
                ShopState.open_support_count,
                " open",
                color_scheme="red",
                variant="soft",
                size="2",
            ),
            width="100%",
            align="center",
        ),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Customer"),
                        rx.table.column_header_cell("Subject"),
                        rx.table.column_header_cell("Category"),
                        rx.table.column_header_cell("Status"),
                        rx.table.column_header_cell("Message"),
                        rx.table.column_header_cell("Actions"),
                    ),
                ),
                rx.table.body(rx.foreach(ShopState.support_tickets, admin_support_row)),
                width="100%",
            ),
            padding="1rem",
            bg=rx.color("gray", 2),
            border=f"1px solid {rx.color('gray', 6)}",
            border_radius="0.75rem",
            width="100%",
            overflow_x="auto",
        ),
        spacing="4",
        width="100%",
    )


@rx.page(route="/admin", title="Nexus Games | Admin Dashboard", on_load=AuthState.guard_admin)
def admin_dashboard() -> rx.Component:
    return page_layout(
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.badge("Admin", color_scheme="purple"),
                        rx.heading("Site Control Panel", size="8", weight="bold"),
                        rx.text(
                            "Edit site text, manage the catalog, and control what visitors see.",
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
                        rx.text(ShopState.game_count, size="6", weight="bold"),
                        padding="1rem",
                        bg=rx.color("gray", 2),
                        border_radius="0.75rem",
                    ),
                    rx.box(
                        rx.text("Visible", size="2", color=rx.color("gray", 11)),
                        rx.text(ShopState.visible_game_count, size="6", weight="bold"),
                        padding="1rem",
                        bg=rx.color("gray", 2),
                        border_radius="0.75rem",
                    ),
                    rx.box(
                        rx.text("Featured", size="2", color=rx.color("gray", 11)),
                        rx.text(ShopState.featured_game_count, size="6", weight="bold"),
                        padding="1rem",
                        bg=rx.color("gray", 2),
                        border_radius="0.75rem",
                    ),
                    rx.box(
                        rx.text("Categories", size="2", color=rx.color("gray", 11)),
                        rx.text(ShopState.category_count, size="6", weight="bold"),
                        padding="1rem",
                        bg=rx.color("gray", 2),
                        border_radius="0.75rem",
                    ),
                    rx.box(
                        rx.text("Open Tickets", size="2", color=rx.color("gray", 11)),
                        rx.text(ShopState.open_support_count, size="6", weight="bold"),
                        padding="1rem",
                        bg=rx.color("gray", 2),
                        border_radius="0.75rem",
                    ),
                    columns=rx.breakpoints(initial="2", md="5"),
                    spacing="4",
                    width="100%",
                ),
                rx.cond(
                    ShopState.admin_message != "",
                    rx.callout(
                        ShopState.admin_message,
                        icon="info",
                        color_scheme="purple",
                        width="100%",
                    ),
                ),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Site Content", value="site"),
                        rx.tabs.trigger("Games Catalog", value="games"),
                        rx.tabs.trigger(
                            "Customer Support",
                            value="support",
                        ),
                    ),
                    rx.tabs.content(site_content_panel(), value="site"),
                    rx.tabs.content(games_panel(), value="games"),
                    rx.tabs.content(support_panel(), value="support"),
                    default_value="site",
                    width="100%",
                ),
                spacing="6",
                padding_y="2rem",
            ),
            size="4",
        ),
    )
