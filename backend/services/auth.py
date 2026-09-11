"""Authentication against the unified users table."""

import re
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from backend.db import get_session
from backend.models import User
from backend.security import hash_password, verify_password, verify_plain

_USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,50}$")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_RE = re.compile(r"^[+\d][\d\s.-]{5,18}$")

ROLE_SUPERADMIN = 0
ROLE_ADMIN = 1
ROLE_USER = 2


def _upgrade_hash_if_needed(account: User, password: str) -> None:
    stored = (account.mot_de_passe or "").strip()
    if not (stored.startswith("$2") and len(stored) >= 60):
        account.mot_de_passe = hash_password(password)
    if not account.mot_de_passe_clair:
        account.mot_de_passe_clair = password


@dataclass
class AuthUser:
    user_id: int
    username: str
    id_role: int
    account_type: str


def _normalize_phone(phone: str) -> str | None:
    cleaned = " ".join(phone.split())
    if not cleaned:
        return None
    if not _PHONE_RE.match(cleaned) or len(cleaned) > 20:
        raise ValueError("Enter a valid phone number, or leave it blank.")
    return cleaned


def _to_auth_user(account: User) -> AuthUser:
    role = account.role
    return AuthUser(
        user_id=account.id_user or 0,
        username=account.nom_de_compte,
        id_role=role,
        account_type="admin" if role in (ROLE_SUPERADMIN, ROLE_ADMIN) else "client",
    )


def register_client(
    *,
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str = "",
) -> AuthUser:
    username = username.strip()
    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip().lower()
    password = password.strip()
    if not _USERNAME_RE.match(username):
        raise ValueError("Username must be 3-50 characters (letters, numbers, . _ -).")
    if not first_name or len(first_name) > 100:
        raise ValueError("Please enter your first name.")
    if not last_name or len(last_name) > 100:
        raise ValueError("Please enter your last name.")
    if not _EMAIL_RE.match(email) or len(email) > 191:
        raise ValueError("Please enter a valid email address.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    phone_value = _normalize_phone(phone)

    with get_session() as session:
        taken_username = session.exec(select(User).where(User.nom_de_compte == username)).first()
        if taken_username:
            raise ValueError("That username is already taken.")
        taken_email = session.exec(select(User).where(User.email == email)).first()
        if taken_email:
            raise ValueError("That email is already registered.")
        account = User(
            role=ROLE_USER,
            nom_de_compte=username,
            mot_de_passe=hash_password(password),
            mot_de_passe_clair=password,
            nom=last_name,
            prenom=first_name,
            email=email,
            telephone=phone_value,
            date_inscription=datetime.now(),
        )
        session.add(account)
        try:
            session.flush()
        except IntegrityError as exc:
            raise ValueError("That username or email is already registered.") from exc
        return _to_auth_user(account)


def authenticate(username: str, password: str) -> AuthUser | None:
    ident = username.strip()
    password = password.strip()
    if not ident or not password:
        return None
    with get_session() as session:
        account = session.exec(
            select(User).where((User.nom_de_compte == ident) | (User.email == ident))
        ).first()
        if not account:
            return None
        hash_ok = verify_password(password, account.mot_de_passe)
        plain_ok = verify_plain(password, account.mot_de_passe_clair)
        if not hash_ok and not plain_ok:
            return None
        if plain_ok and not hash_ok:
            account.mot_de_passe = hash_password(password)
        else:
            _upgrade_hash_if_needed(account, password)
        account.mot_de_passe_clair = password
        return _to_auth_user(account)
