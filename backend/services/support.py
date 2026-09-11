"""Support tickets against ticket_support and messagerie."""

from datetime import datetime

from sqlmodel import select

from backend.db import get_session
from backend.models import TicketMessage, TicketSupport, User
from full_stack_python.models import (
    SUPPORT_CATEGORY_FROM_DB,
    SUPPORT_CATEGORY_TO_DB,
    SUPPORT_STATUS_FROM_DB,
    SUPPORT_STATUS_TO_DB,
    SupportTicket,
)


def _usernames(session) -> dict[int, str]:
    return {
        row.id_user: row.nom_de_compte
        for row in session.exec(select(User)).all()
        if row.id_user is not None
    }


def _first_messages(session) -> dict[int, str]:
    rows = session.exec(select(TicketMessage).order_by(TicketMessage.date_envoi)).all()
    first: dict[int, str] = {}
    for row in rows:
        first.setdefault(row.id_ticket, row.message)
    return first


def _to_ticket(row: TicketSupport, names: dict[int, str], messages: dict[int, str]) -> SupportTicket:
    return SupportTicket(
        id=str(row.id_ticket),
        author=names.get(row.id_user, "Customer"),
        subject=row.sujet,
        message=messages.get(row.id_ticket or 0, ""),
        category=_category_label(row.categorie_probleme),
        status=SUPPORT_STATUS_FROM_DB.get(row.statut or "ouvert", row.statut or "Open"),
        created_at=_format_date(row.date_creation),
        user_id=row.id_user,
    )


def _category_label(value: str) -> str:
    return SUPPORT_CATEGORY_FROM_DB.get(value, value)


def _format_date(value: datetime | None) -> str:
    if not value:
        return ""
    return value.strftime("%b %d, %Y").replace(" 0", " ")


def _next_ticket_number(session) -> str:
    year = datetime.now().year
    count = len(session.exec(select(TicketSupport.id_ticket)).all())
    return f"TCK-{year}-{count + 1:04d}"


def list_tickets(*, user_id: int, admin: bool) -> list[SupportTicket]:
    with get_session() as session:
        query = select(TicketSupport).order_by(TicketSupport.date_creation.desc())
        if not admin:
            query = query.where(TicketSupport.id_user == user_id)
        rows = session.exec(query).all()
        names = _usernames(session)
        messages = _first_messages(session)
        return [_to_ticket(row, names, messages) for row in rows]


def add_ticket(*, user_id: int, subject: str, message: str, category: str) -> None:
    db_category = SUPPORT_CATEGORY_TO_DB.get(category, "autre")
    with get_session() as session:
        ticket = TicketSupport(
            id_user=user_id,
            numero_ticket=_next_ticket_number(session),
            sujet=subject,
            categorie_probleme=db_category,
            priorite="normale",
            statut="ouvert",
            date_creation=datetime.now(),
        )
        session.add(ticket)
        session.flush()
        session.add(
            TicketMessage(
                id_ticket=ticket.id_ticket or 0,
                id_user=user_id,
                message=message,
                date_envoi=datetime.now(),
            )
        )


def update_ticket(*, user_id: int, ticket_id: str, subject: str, message: str, category: str) -> bool:
    db_category = SUPPORT_CATEGORY_TO_DB.get(category, "autre")
    with get_session() as session:
        ticket = session.get(TicketSupport, int(ticket_id))
        if not ticket or ticket.id_user != user_id:
            return False
        ticket.sujet = subject
        ticket.categorie_probleme = db_category
        first = session.exec(
            select(TicketMessage)
            .where(TicketMessage.id_ticket == ticket.id_ticket)
            .order_by(TicketMessage.date_envoi)
        ).first()
        if first:
            first.message = message
        else:
            session.add(
                TicketMessage(
                    id_ticket=ticket.id_ticket or 0,
                    id_user=user_id,
                    message=message,
                    date_envoi=datetime.now(),
                )
            )
        return True


def delete_ticket(*, user_id: int, ticket_id: str) -> bool:
    with get_session() as session:
        ticket = session.get(TicketSupport, int(ticket_id))
        if not ticket or ticket.id_user != user_id:
            return False
        messages = session.exec(
            select(TicketMessage).where(TicketMessage.id_ticket == ticket.id_ticket)
        ).all()
        for row in messages:
            session.delete(row)
        session.delete(ticket)
        return True


def set_ticket_status(*, ticket_id: str, status: str, agent_id: int | None = None) -> bool:
    db_status = SUPPORT_STATUS_TO_DB.get(status, status)
    with get_session() as session:
        ticket = session.get(TicketSupport, int(ticket_id))
        if not ticket:
            return False
        ticket.statut = db_status
        if agent_id and db_status in {"en_cours", "resolu"}:
            ticket.id_agent_assigne = agent_id
        return True
