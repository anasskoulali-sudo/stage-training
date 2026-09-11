import os
from pathlib import Path

from dotenv import load_dotenv
import reflex as rx

load_dotenv(Path(__file__).resolve().parent / ".env")

config = rx.Config(
    app_name="full_stack_python",
    db_url=os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root@127.0.0.1:3306/stage_site",
    ),
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",
                accent_color="purple",
                radius="medium",
            ),
        ),
    ],
)
