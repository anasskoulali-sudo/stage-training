"""Admin panel for editing public site copy."""

import reflex as rx

from frontend.components.admin.fields import admin_field, admin_textarea
from full_stack_python.state import SiteState


def site_content_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Site Content", size="6", weight="bold"),
        rx.text(
            "Changes apply instantly across the public site.",
            size="2",
            color=rx.color("gray", 11),
        ),
        rx.grid(
            rx.box(
                rx.vstack(
                    rx.heading("Store Branding", size="4", weight="bold"),
                    admin_field("Store Name", SiteState.store_name, SiteState.set_store_name),
                    admin_field("Tagline", SiteState.store_tagline, SiteState.set_store_tagline),
                    admin_field("Currency", SiteState.currency, SiteState.set_currency),
                    admin_field(
                        "Support Email",
                        SiteState.support_email,
                        SiteState.set_support_email,
                    ),
                    admin_textarea(
                        "Footer Description",
                        SiteState.footer_description,
                        SiteState.set_footer_description,
                    ),
                    admin_field(
                        "Copyright Text",
                        SiteState.copyright_text,
                        SiteState.set_copyright_text,
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            rx.box(
                rx.vstack(
                    rx.heading("Home Page Hero", size="4", weight="bold"),
                    admin_field("Badge Text", SiteState.hero_badge, SiteState.set_hero_badge),
                    admin_field("Hero Title", SiteState.hero_title, SiteState.set_hero_title),
                    admin_textarea(
                        "Hero Subtitle",
                        SiteState.hero_subtitle,
                        SiteState.set_hero_subtitle,
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            rx.box(
                rx.vstack(
                    rx.heading("Shop Page", size="4", weight="bold"),
                    admin_field("Shop Title", SiteState.shop_title, SiteState.set_shop_title),
                    admin_textarea(
                        "Shop Subtitle",
                        SiteState.shop_subtitle,
                        SiteState.set_shop_subtitle,
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            rx.box(
                rx.vstack(
                    rx.heading("About Page", size="4", weight="bold"),
                    admin_field("About Title", SiteState.about_title, SiteState.set_about_title),
                    admin_textarea(
                        "About Description",
                        SiteState.about_description,
                        SiteState.set_about_description,
                    ),
                    admin_field(
                        "Feature 1 Title",
                        SiteState.about_feature_1_title,
                        SiteState.set_about_feature_1_title,
                    ),
                    admin_textarea(
                        "Feature 1 Text",
                        SiteState.about_feature_1_text,
                        SiteState.set_about_feature_1_text,
                    ),
                    admin_field(
                        "Feature 2 Title",
                        SiteState.about_feature_2_title,
                        SiteState.set_about_feature_2_title,
                    ),
                    admin_textarea(
                        "Feature 2 Text",
                        SiteState.about_feature_2_text,
                        SiteState.set_about_feature_2_text,
                    ),
                    admin_field(
                        "Feature 3 Title",
                        SiteState.about_feature_3_title,
                        SiteState.set_about_feature_3_title,
                    ),
                    admin_textarea(
                        "Feature 3 Text",
                        SiteState.about_feature_3_text,
                        SiteState.set_about_feature_3_text,
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="1.25rem",
                bg=rx.color("gray", 2),
                border_radius="0.75rem",
            ),
            columns="1",
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )
