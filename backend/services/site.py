"""Site copy stored in stage_parametrage.parametres_site."""

from sqlmodel import select

from backend.db import get_session
from backend.models import ParametreSite

SITE_KEYS = (
    "nom_boutique",
    "store_tagline",
    "footer_description",
    "copyright_text",
    "currency",
    "support_email",
    "hero_badge",
    "hero_title",
    "hero_subtitle",
    "shop_title",
    "shop_subtitle",
    "about_title",
    "about_description",
    "about_feature_1_title",
    "about_feature_1_text",
    "about_feature_2_title",
    "about_feature_2_text",
    "about_feature_3_title",
    "about_feature_3_text",
)


def load_params() -> dict[str, str]:
    with get_session() as session:
        rows = session.exec(select(ParametreSite)).all()
        return {row.cle: row.valeur for row in rows}


def upsert_param(key: str, value: str, description: str | None = None) -> None:
    with get_session() as session:
        row = session.exec(select(ParametreSite).where(ParametreSite.cle == key)).first()
        if row:
            row.valeur = value
            if description:
                row.description = description
            return
        session.add(ParametreSite(cle=key, valeur=value, description=description))


def save_params(values: dict[str, str]) -> None:
    with get_session() as session:
        existing = {
            row.cle: row for row in session.exec(select(ParametreSite)).all()
        }
        for key, value in values.items():
            row = existing.get(key)
            if row:
                row.valeur = value
            else:
                session.add(ParametreSite(cle=key, valeur=value))
