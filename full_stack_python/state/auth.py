"""Authentication against the MySQL users table."""

import reflex as rx

from backend.services.auth import ROLE_ADMIN, ROLE_SUPERADMIN, ROLE_USER, authenticate, register_client


class AuthState(rx.State):
    username: str = ""
    password: str = ""
    logged_in_user: str = ""
    user_id: int = 0
    id_role: int = -1
    account_type: str = ""
    login_error: str = ""
    show_signup: bool = False
    register_first_name: str = ""
    register_last_name: str = ""
    register_username: str = ""
    register_email: str = ""
    register_phone: str = ""
    register_password: str = ""
    register_confirm: str = ""
    register_error: str = ""

    @rx.event
    def set_username(self, value: str):
        self.username = value

    @rx.event
    def set_password(self, value: str):
        self.password = value

    @rx.event
    def set_register_first_name(self, value: str):
        self.register_first_name = value

    @rx.event
    def set_register_last_name(self, value: str):
        self.register_last_name = value

    @rx.event
    def set_register_username(self, value: str):
        self.register_username = value

    @rx.event
    def set_register_email(self, value: str):
        self.register_email = value

    @rx.event
    def set_register_phone(self, value: str):
        self.register_phone = value

    @rx.event
    def set_register_password(self, value: str):
        self.register_password = value

    @rx.event
    def set_register_confirm(self, value: str):
        self.register_confirm = value

    @rx.event
    def show_register_form(self):
        self.show_signup = True
        self.login_error = ""
        self.register_error = ""

    @rx.event
    def show_login_form(self):
        self.show_signup = False
        self.login_error = ""
        self.register_error = ""
        self.register_password = ""
        self.register_confirm = ""

    def _clear_register_form(self):
        self.register_first_name = ""
        self.register_last_name = ""
        self.register_username = ""
        self.register_email = ""
        self.register_phone = ""
        self.register_password = ""
        self.register_confirm = ""
        self.register_error = ""
        self.show_signup = False

    def _accept_account(self, account):
        self.logged_in_user = account.username
        self.user_id = account.user_id
        self.id_role = account.id_role
        self.account_type = account.account_type
        self.login_error = ""
        self.password = ""

    @rx.event
    def login(self):
        user = self.username.strip()
        pwd = self.password.strip()
        if not user or not pwd:
            self.login_error = "Please enter a username and password."
            return
        account = authenticate(user, pwd)
        self.password = ""
        if not account:
            self.login_error = "Invalid username or password."
            return
        self._accept_account(account)
        if account.id_role in (ROLE_SUPERADMIN, ROLE_ADMIN):
            return rx.redirect("/admin")

    @rx.event
    def register(self):
        if self.register_password != self.register_confirm:
            self.register_error = "Passwords do not match."
            return
        try:
            account = register_client(
                username=self.register_username,
                password=self.register_password,
                first_name=self.register_first_name,
                last_name=self.register_last_name,
                email=self.register_email,
                phone=self.register_phone,
            )
        except ValueError as exc:
            self.register_password = ""
            self.register_confirm = ""
            self.register_error = str(exc)
            return
        self._clear_register_form()
        self._accept_account(account)

    @rx.event
    def logout(self):
        self.logged_in_user = ""
        self.user_id = 0
        self.id_role = -1
        self.account_type = ""
        self.username = ""
        self.password = ""
        self.login_error = ""
        self._clear_register_form()
        return rx.redirect("/account")

    @rx.event
    def guard_admin(self):
        if self.id_role not in (ROLE_SUPERADMIN, ROLE_ADMIN):
            return rx.redirect("/account")

    @rx.event
    def guard_customer(self):
        if self.id_role != ROLE_USER:
            return rx.redirect("/account")

    @rx.var
    def is_logged_in(self) -> bool:
        return self.logged_in_user != ""

    @rx.var
    def is_admin(self) -> bool:
        return self.id_role in (ROLE_SUPERADMIN, ROLE_ADMIN)

    @rx.var
    def is_superadmin(self) -> bool:
        return self.id_role == ROLE_SUPERADMIN

    @rx.var
    def is_customer(self) -> bool:
        return self.id_role == ROLE_USER
