"""Contact customer support widget for logged-in users."""

import reflex as rx

from full_stack_python.state import AuthState, ShopState, SupportTicket


SUPPORT_CATEGORIES = ["Order", "Refund", "Technical", "Billing", "Other"]


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.match(
        status,
        ("Open", rx.badge("Open", color_scheme="red", variant="soft")),
        ("In Progress", rx.badge("In Progress", color_scheme="amber", variant="soft")),
        ("Resolved", rx.badge("Resolved", color_scheme="green", variant="soft")),
        rx.badge(status, variant="soft"),
    )


def user_ticket_row(ticket: rx.Var[SupportTicket]) -> rx.Component:
    is_owner = AuthState.logged_in_user == ticket.author
    is_editing = ShopState.editing_ticket_id == ticket.id.to(str)

    return rx.cond(
        is_owner,
        rx.box(
            rx.cond(
                is_editing,
                rx.vstack(
                    rx.input(
                        value=ShopState.edit_ticket_subject,
                        on_change=ShopState.set_edit_ticket_subject,
                        placeholder="Subject",
                        width="100%",
                        size="2",
                    ),
                    rx.select(
                        SUPPORT_CATEGORIES,
                        value=ShopState.edit_ticket_category,
                        on_change=ShopState.set_edit_ticket_category,
                        size="2",
                    ),
                    rx.text_area(
                        value=ShopState.edit_ticket_message,
                        on_change=ShopState.set_edit_ticket_message,
                        width="100%",
                        rows="3",
                    ),
                    rx.hstack(
                        rx.button(
                            "Save",
                            size="2",
                            color_scheme="purple",
                            on_click=ShopState.save_ticket_edit(ticket.id),
                        ),
                        rx.button(
                            "Cancel",
                            size="2",
                            variant="outline",
                            on_click=ShopState.cancel_ticket_edit,
                        ),
                        spacing="2",
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(ticket.subject, weight="bold", size="3"),
                        rx.spacer(),
                        status_badge(ticket.status),
                        width="100%",
                        align="center",
                    ),
                    rx.hstack(
                        rx.badge(ticket.category, color_scheme="purple", variant="soft"),
                        rx.text(ticket.created_at, size="1", color=rx.color("gray", 10)),
                        spacing="2",
                        align="center",
                    ),
                    rx.text(ticket.message, size="2", color=rx.color("gray", 11)),
                    rx.hstack(
                        rx.button(
                            rx.icon("pencil", size=12),
                            "Edit",
                            size="1",
                            variant="soft",
                            on_click=ShopState.start_edit_ticket(ticket.id),
                        ),
                        rx.button(
                            rx.icon("trash-2", size=12),
                            "Delete",
                            size="1",
                            variant="soft",
                            color_scheme="red",
                            on_click=ShopState.delete_support_ticket(ticket.id),
                        ),
                        spacing="2",
                    ),
                    spacing="2",
                    align="start",
                    width="100%",
                ),
            ),
            padding="1rem",
            bg=rx.color("gray", 3),
            border=f"1px solid {rx.color('gray', 6)}",
            border_radius="0.75rem",
            width="100%",
        ),
    )


def contact_us_widget() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon("headphones", size=24, color="#a78bfa"),
                    bg=rx.color("gray", 3),
                    padding="0.65rem",
                    border_radius="0.5rem",
                ),
                rx.vstack(
                    rx.heading("Contact Us", size="5", weight="bold"),
                    rx.text(
                        "Reach customer support — we typically reply within 24 hours.",
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    spacing="1",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
            rx.cond(
                ShopState.support_form_message != "",
                rx.callout(
                    ShopState.support_form_message,
                    icon="info",
                    color_scheme="purple",
                    width="100%",
                ),
            ),
            rx.vstack(
                rx.text("Subject", size="2", weight="medium"),
                rx.input(
                    placeholder="Brief summary of your issue",
                    value=ShopState.support_subject,
                    on_change=ShopState.set_support_subject,
                    width="100%",
                    size="2",
                ),
                rx.text("Category", size="2", weight="medium"),
                rx.select(
                    SUPPORT_CATEGORIES,
                    value=ShopState.support_category,
                    on_change=ShopState.set_support_category,
                    size="2",
                ),
                rx.text("Message", size="2", weight="medium"),
                rx.text_area(
                    placeholder="Describe your issue in detail...",
                    value=ShopState.support_message,
                    on_change=ShopState.set_support_message,
                    width="100%",
                    rows="4",
                ),
                rx.button(
                    rx.icon("send", size=16),
                    "Send to Support",
                    color_scheme="purple",
                    width="100%",
                    on_click=ShopState.submit_support_ticket,
                ),
                spacing="2",
                width="100%",
                align="start",
            ),
            rx.divider(),
            rx.vstack(
                rx.heading("Your Requests", size="4", weight="bold"),
                rx.foreach(ShopState.support_tickets, user_ticket_row),
                rx.text(
                    "Only your own support messages are shown here.",
                    size="1",
                    color=rx.color("gray", 10),
                ),
                spacing="3",
                align="start",
                width="100%",
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
