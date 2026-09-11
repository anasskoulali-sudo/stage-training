"""Shared application state split by domain."""

from full_stack_python.state.admin import AdminState
from full_stack_python.state.auth import AuthState
from full_stack_python.state.cart import CartState
from full_stack_python.state.catalog import CatalogState
from full_stack_python.state.community import CommunityState
from full_stack_python.state.site import SiteState
from full_stack_python.state.support import SupportState

__all__ = [
    "AdminState",
    "AuthState",
    "CartState",
    "CatalogState",
    "CommunityState",
    "SiteState",
    "SupportState",
]
