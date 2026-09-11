"""Shopping cart kept in session memory; checkout writes MySQL orders."""

from uuid import UUID

import reflex as rx

from backend.services.orders import place_order
from full_stack_python.models import CartItem
from full_stack_python.state.auth import AuthState
from full_stack_python.state.catalog import CatalogState
from full_stack_python.state.site import SiteState


class CartState(rx.State):
    cart_items: list[CartItem] = []
    checkout_message: str = ""

    @rx.event
    async def add_to_cart(self, game_id: str):
        catalog = await self.get_state(CatalogState)
        game = catalog.find_game(game_id)
        if not game or not game.visible:
            return
        current = 0
        for item in self.cart_items:
            if item.game_id == game_id:
                current = item.quantity
                break
        if game.stock and game.stock <= current:
            return
        for item in self.cart_items:
            if item.game_id == game_id:
                item.quantity += 1
                return
        self.cart_items = [
            *self.cart_items,
            CartItem(
                game_id=game.id,
                title=game.title,
                price=game.price,
                image=game.image,
            ),
        ]

    @rx.event
    def remove_from_cart(self, item_id: UUID):
        self.cart_items = [item for item in self.cart_items if item.id != item_id]

    @rx.event
    def increase_quantity(self, item_id: UUID):
        for item in self.cart_items:
            if item.id == item_id:
                item.quantity += 1
                return

    @rx.event
    def decrease_quantity(self, item_id: UUID):
        for item in self.cart_items:
            if item.id == item_id:
                if item.quantity > 1:
                    item.quantity -= 1
                else:
                    self.cart_items = [
                        cart_item for cart_item in self.cart_items if cart_item.id != item_id
                    ]
                return

    @rx.event
    def clear_cart(self):
        self.cart_items = []
        self.checkout_message = ""

    @rx.event
    async def checkout(self):
        if not self.cart_items:
            self.checkout_message = "Your cart is empty."
            return
        auth = await self.get_state(AuthState)
        if not auth.is_customer:
            self.checkout_message = "Sign in with a customer account to checkout."
            return
        try:
            order_id, total = place_order(
                user_id=auth.user_id,
                items=[
                    {
                        "game_id": item.game_id,
                        "quantity": item.quantity,
                        "price": item.price,
                    }
                    for item in self.cart_items
                ],
            )
        except ValueError as exc:
            self.checkout_message = str(exc)
            return
        site = await self.get_state(SiteState)
        catalog = await self.get_state(CatalogState)
        catalog.load_catalog()
        self.cart_items = []
        self.checkout_message = (
            f"Order #{order_id} placed! Total: ${total:.2f}. Thanks for shopping at {site.store_name}!"
        )

    @rx.var
    def cart_count(self) -> int:
        return sum(item.quantity for item in self.cart_items)

    @rx.var
    def cart_total(self) -> float:
        return sum(item.price * item.quantity for item in self.cart_items)
