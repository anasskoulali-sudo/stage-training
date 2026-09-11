"""Admin panel for managing the game catalog."""

import reflex as rx

from frontend.components.admin.fields import admin_field, admin_textarea
from full_stack_python.models import Game
from full_stack_python.state import AdminState, CatalogState


def game_form_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    rx.cond(AdminState.is_editing_game, "Edit Game", "Add New Game"),
                    size="5",
                    weight="bold",
                ),
                rx.spacer(),
                rx.button(
                    "New Game",
                    variant="soft",
                    size="2",
                    on_click=AdminState.start_new_game,
                ),
                width="100%",
                align="center",
            ),
            rx.grid(
                admin_field("Title", AdminState.form_title, AdminState.set_form_title, "Game title"),
                admin_field("Price HT", AdminState.form_price, AdminState.set_form_price, "49.99"),
                rx.vstack(
                    rx.text("Category", size="2", weight="medium"),
                    rx.cond(
                        CatalogState.category_count > 0,
                        rx.select(
                            CatalogState.categories,
                            value=AdminState.form_category,
                            on_change=AdminState.set_form_category,
                            size="2",
                            width="100%",
                        ),
                        rx.text(
                            "Create a category first in the Categories tab.",
                            size="2",
                            color=rx.color("gray", 11),
                        ),
                    ),
                    spacing="1",
                    width="100%",
                    align="start",
                ),
                admin_field(
                    "Platform",
                    AdminState.form_platform,
                    AdminState.set_form_platform,
                    "PC (Steam)",
                ),
                admin_field("VAT %", AdminState.form_tva, AdminState.set_form_tva, "20"),
                admin_field("Stock", AdminState.form_stock, AdminState.set_form_stock, "100"),
                admin_field("Publisher", AdminState.form_editor, AdminState.set_form_editor, "Studio"),
                rx.vstack(
                    rx.text("Format", size="2", weight="medium"),
                    rx.select(
                        ["dematerialise", "physique"],
                        value=AdminState.form_format,
                        on_change=AdminState.set_form_format,
                        size="2",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                    align="start",
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="3",
                width="100%",
            ),
            admin_textarea(
                "Description",
                AdminState.form_description,
                AdminState.set_form_description,
                "Game description...",
            ),
            rx.text(
                "New products get a unique id_produit from MySQL. Updates keep the same ID.",
                size="1",
                color=rx.color("gray", 10),
            ),
            rx.button(
                rx.icon("save", size=16),
                rx.cond(AdminState.is_editing_game, "Save Changes", "Add Game"),
                color_scheme="purple",
                on_click=AdminState.save_game,
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
        rx.table.cell(rx.text(game.price_ht)),
        rx.table.cell(game.stock),
        rx.table.cell(
            rx.hstack(
                rx.icon_button(
                    rx.icon("pencil", size=14),
                    size="1",
                    variant="soft",
                    on_click=AdminState.load_game_for_edit(game.id),
                ),
                rx.icon_button(
                    rx.icon("trash-2", size=14),
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=AdminState.delete_game(game.id),
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
                on_click=AdminState.start_new_game,
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
                        rx.table.column_header_cell("Price HT"),
                        rx.table.column_header_cell("Stock"),
                        rx.table.column_header_cell("Actions"),
                    ),
                ),
                rx.table.body(rx.foreach(CatalogState.games, admin_game_row)),
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
