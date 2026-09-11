"""Admin panel for customer support tickets."""

import reflex as rx

from full_stack_python.models import SupportTicket
from full_stack_python.state import SupportState


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
                    on_click=SupportState.set_ticket_status(ticket.id, "Open"),
                ),
                rx.button(
                    "Progress",
                    size="1",
                    variant="soft",
                    color_scheme="amber",
                    on_click=SupportState.set_ticket_status(ticket.id, "In Progress"),
                ),
                rx.button(
                    "Resolved",
                    size="1",
                    variant="soft",
                    color_scheme="green",
                    on_click=SupportState.set_ticket_status(ticket.id, "Resolved"),
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
                SupportState.open_support_count,
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
                rx.table.body(rx.foreach(SupportState.support_tickets, admin_support_row)),
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
