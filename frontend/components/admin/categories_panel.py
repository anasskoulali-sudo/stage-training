"""Superadmin panel for creating and editing catalog categories."""

import reflex as rx

from frontend.components.admin.fields import admin_field, admin_textarea
from full_stack_python.models import Category
from full_stack_python.state import AdminState, CatalogState


def category_form_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    rx.cond(AdminState.is_editing_category, "Edit Category", "Add Category"),
                    size="5",
                    weight="bold",
                ),
                rx.spacer(),
                rx.button(
                    "New Category",
                    variant="soft",
                    size="2",
                    on_click=AdminState.start_new_category,
                ),
                width="100%",
                align="center",
            ),
            admin_field(
                "Name",
                AdminState.category_name,
                AdminState.set_category_name,
                "Action / RPG",
            ),
            admin_textarea(
                "Description",
                AdminState.category_description,
                AdminState.set_category_description,
                "Shown on the shop as a filter group.",
            ),
            rx.text(
                "MySQL assigns a new id_categorie automatically. Names and slugs stay unique.",
                size="1",
                color=rx.color("gray", 10),
            ),
            rx.button(
                rx.icon("save", size=16),
                rx.cond(AdminState.is_editing_category, "Save Category", "Add Category"),
                color_scheme="purple",
                on_click=AdminState.save_category_form,
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


def admin_category_row(category: rx.Var[Category]) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.text(category.id, size="2")),
        rx.table.cell(rx.text(category.name, weight="medium")),
        rx.table.cell(rx.text(category.slug, size="2", color=rx.color("gray", 11))),
        rx.table.cell(
            rx.text(category.description, size="2", color=rx.color("gray", 11), max_width="18rem")
        ),
        rx.table.cell(
            rx.hstack(
                rx.icon_button(
                    rx.icon("pencil", size=14),
                    size="1",
                    variant="soft",
                    on_click=AdminState.load_category_for_edit(category.id),
                ),
                rx.icon_button(
                    rx.icon("trash-2", size=14),
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=AdminState.delete_category_row(category.id),
                ),
                spacing="1",
            ),
        ),
    )


def categories_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Categories", size="6", weight="bold"),
                rx.text(
                    "Create shop categories before adding products. Each row gets a unique database ID.",
                    size="2",
                    color=rx.color("gray", 11),
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.icon("plus", size=16),
                "Add Category",
                color_scheme="purple",
                on_click=AdminState.start_new_category,
            ),
            width="100%",
            align="center",
        ),
        category_form_panel(),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("Name"),
                        rx.table.column_header_cell("Slug"),
                        rx.table.column_header_cell("Description"),
                        rx.table.column_header_cell("Actions"),
                    ),
                ),
                rx.table.body(rx.foreach(CatalogState.category_records, admin_category_row)),
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
