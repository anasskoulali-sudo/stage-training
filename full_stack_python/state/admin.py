"""Admin catalog editing persisted to MySQL categorie and produit."""

import reflex as rx

from backend.services.catalog import delete_category, delete_product, save_category, save_product
from full_stack_python.state.auth import AuthState
from full_stack_python.state.cart import CartState
from full_stack_python.state.catalog import CatalogState


class AdminState(rx.State):
    admin_message: str = ""
    admin_tab: str = "site"
    editing_game_id: str = ""
    form_title: str = ""
    form_price: str = ""
    form_category: str = ""
    form_platform: str = ""
    form_description: str = ""
    form_editor: str = ""
    form_format: str = "dematerialise"
    form_tva: str = "20"
    form_stock: str = "0"
    editing_category_id: str = ""
    category_name: str = ""
    category_description: str = ""

    async def _require_superadmin(self) -> bool:
        auth = await self.get_state(AuthState)
        if auth.is_superadmin:
            return True
        self.admin_message = "Only the superadmin can manage categories and products."
        return False

    @rx.event
    def set_form_title(self, value: str):
        self.form_title = value

    @rx.event
    def set_form_price(self, value: str):
        self.form_price = value

    @rx.event
    def set_form_category(self, value: str):
        self.form_category = value

    @rx.event
    def set_form_platform(self, value: str):
        self.form_platform = value

    @rx.event
    def set_form_description(self, value: str):
        self.form_description = value

    @rx.event
    def set_form_editor(self, value: str):
        self.form_editor = value

    @rx.event
    def set_form_format(self, value: str):
        self.form_format = value

    @rx.event
    def set_form_tva(self, value: str):
        self.form_tva = value

    @rx.event
    def set_form_stock(self, value: str):
        self.form_stock = value

    @rx.event
    def set_category_name(self, value: str):
        self.category_name = value

    @rx.event
    def set_category_description(self, value: str):
        self.category_description = value

    @rx.event
    def set_admin_tab(self, tab: str):
        self.admin_tab = tab

    @rx.event
    async def start_new_game(self):
        if not await self._require_superadmin():
            return
        catalog = await self.get_state(CatalogState)
        self.editing_game_id = ""
        self.form_title = ""
        self.form_price = ""
        self.form_category = catalog.categories[0] if catalog.categories else ""
        self.form_platform = ""
        self.form_description = ""
        self.form_editor = ""
        self.form_format = "dematerialise"
        self.form_tva = "20"
        self.form_stock = "0"
        self.admin_tab = "games"
        self.admin_message = "Fill in the form below to add a new game."

    @rx.event
    async def load_game_for_edit(self, game_id: str):
        if not await self._require_superadmin():
            return
        catalog = await self.get_state(CatalogState)
        game = catalog.find_game(game_id)
        if not game:
            self.admin_message = "Game not found."
            return
        self.editing_game_id = game.id
        self.form_title = game.title
        self.form_price = f"{game.price_ht:.2f}"
        self.form_category = game.category
        self.form_platform = game.platform
        self.form_description = game.description
        self.form_editor = game.editor
        self.form_format = game.format_type
        self.form_tva = f"{game.tva:.2f}"
        self.form_stock = str(game.stock)
        self.admin_tab = "games"
        self.admin_message = f"Editing {game.title}."

    @rx.event
    async def save_game(self):
        if not await self._require_superadmin():
            return
        title = self.form_title.strip()
        if not title:
            self.admin_message = "Title is required."
            return
        try:
            price_ht = float(self.form_price.strip())
            tva = float(self.form_tva.strip() or "20")
            stock = int(self.form_stock.strip() or "0")
        except ValueError:
            self.admin_message = "Price, VAT, and stock must be valid numbers."
            return
        catalog = await self.get_state(CatalogState)
        try:
            product_id = save_product(
                product_id=self.editing_game_id or None,
                title=title,
                price_ht=price_ht,
                category=self.form_category.strip(),
                platform=self.form_platform.strip() or "PC",
                description=self.form_description.strip(),
                editor=self.form_editor.strip(),
                format_type=self.form_format or "dematerialise",
                tva=tva,
                stock=stock,
            )
        except ValueError as exc:
            self.admin_message = str(exc)
            return
        self.editing_game_id = product_id
        catalog.load_catalog()
        self.admin_message = f"Saved {title}."

    @rx.event
    async def delete_game(self, game_id: str):
        if not await self._require_superadmin():
            return
        cart = await self.get_state(CartState)
        catalog = await self.get_state(CatalogState)
        try:
            title = delete_product(game_id)
        except ValueError as exc:
            self.admin_message = str(exc)
            return
        if not title:
            return
        cart.cart_items = [item for item in cart.cart_items if item.game_id != game_id]
        if self.editing_game_id == game_id:
            await self.start_new_game()
        catalog.load_catalog()
        self.admin_message = f"Removed {title} from the catalog."

    @rx.event
    async def start_new_category(self):
        if not await self._require_superadmin():
            return
        self.editing_category_id = ""
        self.category_name = ""
        self.category_description = ""
        self.admin_tab = "categories"
        self.admin_message = "Fill in the form below to add a new category."

    @rx.event
    async def load_category_for_edit(self, category_id: str):
        if not await self._require_superadmin():
            return
        catalog = await self.get_state(CatalogState)
        category = catalog.find_category(category_id)
        if not category:
            self.admin_message = "Category not found."
            return
        self.editing_category_id = category.id
        self.category_name = category.name
        self.category_description = category.description
        self.admin_tab = "categories"
        self.admin_message = f"Editing {category.name}."

    @rx.event
    async def save_category_form(self):
        if not await self._require_superadmin():
            return
        try:
            category_id = save_category(
                category_id=self.editing_category_id or None,
                name=self.category_name,
                description=self.category_description,
            )
        except ValueError as exc:
            self.admin_message = str(exc)
            return
        catalog = await self.get_state(CatalogState)
        self.editing_category_id = category_id
        catalog.load_catalog()
        self.admin_message = f"Saved category {self.category_name.strip()}."

    @rx.event
    async def delete_category_row(self, category_id: str):
        if not await self._require_superadmin():
            return
        catalog = await self.get_state(CatalogState)
        try:
            name = delete_category(category_id)
        except ValueError as exc:
            self.admin_message = str(exc)
            return
        if not name:
            return
        if self.editing_category_id == category_id:
            await self.start_new_category()
        catalog.load_catalog()
        self.admin_message = f"Removed category {name}."

    @rx.var
    def is_editing_game(self) -> bool:
        return self.editing_game_id != ""

    @rx.var
    def is_editing_category(self) -> bool:
        return self.editing_category_id != ""
