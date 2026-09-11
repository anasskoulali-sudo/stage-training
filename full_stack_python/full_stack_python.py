"""Nexus Games — a multi-page video game shop built with Reflex."""

import reflex as rx

from backend import models as db_models  # noqa: F401
from backend.db import ensure_schema
from frontend import pages  # noqa: F401

ensure_schema()

app = rx.App()
