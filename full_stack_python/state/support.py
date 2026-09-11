"""Customer support tickets loaded from MySQL."""

import reflex as rx

from backend.services.support import add_ticket, delete_ticket, list_tickets, set_ticket_status, update_ticket
from full_stack_python.models import SupportTicket
from full_stack_python.state.auth import AuthState


class SupportState(rx.State):
    support_tickets: list[SupportTicket] = []
    support_subject: str = ""
    support_message: str = ""
    support_category: str = "Other"
    support_form_message: str = ""
    editing_ticket_id: str = ""
    edit_ticket_subject: str = ""
    edit_ticket_message: str = ""
    edit_ticket_category: str = "Other"
    admin_message: str = ""

    @rx.event
    async def load_tickets(self):
        auth = await self.get_state(AuthState)
        if not auth.is_logged_in:
            self.support_tickets = []
            return
        self.support_tickets = list_tickets(user_id=auth.user_id, admin=auth.is_admin)

    @rx.event
    def set_support_subject(self, value: str):
        self.support_subject = value

    @rx.event
    def set_support_message(self, value: str):
        self.support_message = value

    @rx.event
    def set_support_category(self, value: str):
        self.support_category = value

    @rx.event
    def set_edit_ticket_subject(self, value: str):
        self.edit_ticket_subject = value

    @rx.event
    def set_edit_ticket_message(self, value: str):
        self.edit_ticket_message = value

    @rx.event
    def set_edit_ticket_category(self, value: str):
        self.edit_ticket_category = value

    def _find_ticket(self, ticket_id: str) -> SupportTicket | None:
        for ticket in self.support_tickets:
            if ticket.id == ticket_id:
                return ticket
        return None

    @rx.event
    async def submit_support_ticket(self):
        auth = await self.get_state(AuthState)
        if not auth.is_logged_in:
            self.support_form_message = "Sign in to contact customer support."
            return
        if auth.is_admin:
            self.support_form_message = "Admins manage support from the dashboard."
            return
        subject = self.support_subject.strip()
        message = self.support_message.strip()
        if not subject or not message:
            self.support_form_message = "Please fill in the subject and message."
            return
        add_ticket(
            user_id=auth.user_id,
            subject=subject,
            message=message,
            category=self.support_category,
        )
        self.support_subject = ""
        self.support_message = ""
        self.support_category = "Other"
        self.support_form_message = "Your message was sent to customer support!"
        await self.load_tickets()

    @rx.event
    async def start_edit_ticket(self, ticket_id: str):
        auth = await self.get_state(AuthState)
        ticket = self._find_ticket(ticket_id)
        if not ticket or ticket.user_id != auth.user_id:
            return
        self.editing_ticket_id = ticket_id
        self.edit_ticket_subject = ticket.subject
        self.edit_ticket_message = ticket.message
        self.edit_ticket_category = ticket.category

    @rx.event
    async def save_ticket_edit(self, ticket_id: str):
        auth = await self.get_state(AuthState)
        subject = self.edit_ticket_subject.strip()
        message = self.edit_ticket_message.strip()
        if not subject or not message:
            return
        if not update_ticket(
            user_id=auth.user_id,
            ticket_id=ticket_id,
            subject=subject,
            message=message,
            category=self.edit_ticket_category,
        ):
            return
        self.editing_ticket_id = ""
        self.support_form_message = "Support request updated."
        await self.load_tickets()

    @rx.event
    def cancel_ticket_edit(self):
        self.editing_ticket_id = ""
        self.edit_ticket_subject = ""
        self.edit_ticket_message = ""
        self.edit_ticket_category = "Other"

    @rx.event
    async def delete_support_ticket(self, ticket_id: str):
        auth = await self.get_state(AuthState)
        if not delete_ticket(user_id=auth.user_id, ticket_id=ticket_id):
            return
        if self.editing_ticket_id == ticket_id:
            self.cancel_ticket_edit()
        self.support_form_message = "Support request removed."
        await self.load_tickets()

    @rx.event
    async def set_ticket_status(self, ticket_id: str, status: str):
        auth = await self.get_state(AuthState)
        if not auth.is_admin:
            return
        if not set_ticket_status(ticket_id=ticket_id, status=status, agent_id=auth.user_id):
            return
        self.admin_message = f"Ticket marked as {status}."
        await self.load_tickets()

    @rx.var
    def open_support_count(self) -> int:
        return len([ticket for ticket in self.support_tickets if ticket.status == "Open"])

    @rx.var
    def support_ticket_count(self) -> int:
        return len(self.support_tickets)
