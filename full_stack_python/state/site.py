"""Editable site-wide copy loaded from MySQL parametres_site."""

import reflex as rx

from backend.services.site import load_params, save_params, upsert_param


class SiteState(rx.State):
    store_name: str = "Nexus Games"
    store_tagline: str = "Your gaming destination"
    footer_description: str = "The best place to discover and buy video games."
    copyright_text: str = "© 2026 Nexus Games. Built with Reflex."
    currency: str = "EUR"
    support_email: str = ""

    hero_badge: str = "New releases every week"
    hero_title: str = "Level Up Your Game Library"
    hero_subtitle: str = (
        "Discover blockbuster titles, indie gems, and everything in between. "
        "One shop, every platform."
    )

    shop_title: str = "Game Shop"
    shop_subtitle: str = (
        "Browse our full catalog. Use search and filters to find your next adventure."
    )

    about_title: str = "About Nexus Games"
    about_description: str = (
        "Nexus Games is a demo gaming shop built with Reflex — a full-stack Python "
        "framework for modern web apps. Browse titles, add them to your cart, and "
        "explore linked pages across the store."
    )
    about_feature_1_title: str = "Curated Catalog"
    about_feature_1_text: str = "Hand-picked games across RPG, action, sports, and more."
    about_feature_2_title: str = "Smart Cart"
    about_feature_2_text: str = "Add games from any page and manage quantities in your cart."
    about_feature_3_title: str = "Connected Pages"
    about_feature_3_text: str = "Home, shop, game details, cart, and about — all linked together."

    def _snapshot(self) -> dict[str, str]:
        return {
            "nom_boutique": self.store_name,
            "store_tagline": self.store_tagline,
            "footer_description": self.footer_description,
            "copyright_text": self.copyright_text,
            "currency": self.currency,
            "support_email": self.support_email,
            "hero_badge": self.hero_badge,
            "hero_title": self.hero_title,
            "hero_subtitle": self.hero_subtitle,
            "shop_title": self.shop_title,
            "shop_subtitle": self.shop_subtitle,
            "about_title": self.about_title,
            "about_description": self.about_description,
            "about_feature_1_title": self.about_feature_1_title,
            "about_feature_1_text": self.about_feature_1_text,
            "about_feature_2_title": self.about_feature_2_title,
            "about_feature_2_text": self.about_feature_2_text,
            "about_feature_3_title": self.about_feature_3_title,
            "about_feature_3_text": self.about_feature_3_text,
        }

    @rx.event
    def load_site(self):
        params = load_params()
        self.store_name = params.get("nom_boutique", self.store_name)
        self.store_tagline = params.get("store_tagline", self.store_tagline)
        self.footer_description = params.get("footer_description", self.footer_description)
        self.copyright_text = params.get("copyright_text", self.copyright_text)
        self.currency = params.get("currency", self.currency)
        self.support_email = params.get("support_email", self.support_email)
        self.hero_badge = params.get("hero_badge", self.hero_badge)
        self.hero_title = params.get("hero_title", self.hero_title)
        self.hero_subtitle = params.get("hero_subtitle", self.hero_subtitle)
        self.shop_title = params.get("shop_title", self.shop_title)
        self.shop_subtitle = params.get("shop_subtitle", self.shop_subtitle)
        self.about_title = params.get("about_title", self.about_title)
        self.about_description = params.get("about_description", self.about_description)
        self.about_feature_1_title = params.get("about_feature_1_title", self.about_feature_1_title)
        self.about_feature_1_text = params.get("about_feature_1_text", self.about_feature_1_text)
        self.about_feature_2_title = params.get("about_feature_2_title", self.about_feature_2_title)
        self.about_feature_2_text = params.get("about_feature_2_text", self.about_feature_2_text)
        self.about_feature_3_title = params.get("about_feature_3_title", self.about_feature_3_title)
        self.about_feature_3_text = params.get("about_feature_3_text", self.about_feature_3_text)

    @rx.event
    def save_site(self):
        save_params(self._snapshot())

    def _set_param(self, key: str, value: str):
        upsert_param(key, value)

    @rx.event
    def set_store_name(self, value: str):
        self.store_name = value
        self._set_param("nom_boutique", value)

    @rx.event
    def set_store_tagline(self, value: str):
        self.store_tagline = value
        self._set_param("store_tagline", value)

    @rx.event
    def set_footer_description(self, value: str):
        self.footer_description = value
        self._set_param("footer_description", value)

    @rx.event
    def set_copyright_text(self, value: str):
        self.copyright_text = value
        self._set_param("copyright_text", value)

    @rx.event
    def set_currency(self, value: str):
        self.currency = value
        self._set_param("currency", value)

    @rx.event
    def set_support_email(self, value: str):
        self.support_email = value
        self._set_param("support_email", value)

    @rx.event
    def set_hero_badge(self, value: str):
        self.hero_badge = value
        self._set_param("hero_badge", value)

    @rx.event
    def set_hero_title(self, value: str):
        self.hero_title = value
        self._set_param("hero_title", value)

    @rx.event
    def set_hero_subtitle(self, value: str):
        self.hero_subtitle = value
        self._set_param("hero_subtitle", value)

    @rx.event
    def set_shop_title(self, value: str):
        self.shop_title = value
        self._set_param("shop_title", value)

    @rx.event
    def set_shop_subtitle(self, value: str):
        self.shop_subtitle = value
        self._set_param("shop_subtitle", value)

    @rx.event
    def set_about_title(self, value: str):
        self.about_title = value
        self._set_param("about_title", value)

    @rx.event
    def set_about_description(self, value: str):
        self.about_description = value
        self._set_param("about_description", value)

    @rx.event
    def set_about_feature_1_title(self, value: str):
        self.about_feature_1_title = value
        self._set_param("about_feature_1_title", value)

    @rx.event
    def set_about_feature_1_text(self, value: str):
        self.about_feature_1_text = value
        self._set_param("about_feature_1_text", value)

    @rx.event
    def set_about_feature_2_title(self, value: str):
        self.about_feature_2_title = value
        self._set_param("about_feature_2_title", value)

    @rx.event
    def set_about_feature_2_text(self, value: str):
        self.about_feature_2_text = value
        self._set_param("about_feature_2_text", value)

    @rx.event
    def set_about_feature_3_title(self, value: str):
        self.about_feature_3_title = value
        self._set_param("about_feature_3_title", value)

    @rx.event
    def set_about_feature_3_text(self, value: str):
        self.about_feature_3_text = value
        self._set_param("about_feature_3_text", value)
