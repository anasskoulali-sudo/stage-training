"""Shared application state for the gaming shop."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4

import reflex as rx

from full_stack_python.data import CATEGORIES, GAMES, Game, get_game_by_id


@dataclass
class CartItem:
    game_id: str
    title: str
    price: float
    image: str
    quantity: int = 1
    id: UUID = field(default_factory=uuid4)


class ShopState(rx.State):
    search_query: str = ""
    selected_category: str = "All"
    cart_items: list[CartItem] = []
    checkout_message: str = ""

    @rx.event
    def set_search(self, value: str):
        self.search_query = value

    @rx.event
    def set_category(self, category: str):
        self.selected_category = category

    @rx.event
    def on_load_shop(self):
        category = self.router.url.query_parameters.get("category", "All")
        if category == "All" or category in CATEGORIES:
            self.selected_category = category

    @rx.event
    def add_to_cart(self, game_id: str):
        game = get_game_by_id(game_id)
        if not game:
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
    def checkout(self):
        if not self.cart_items:
            self.checkout_message = "Your cart is empty."
            return
        total = self.cart_total
        self.cart_items = []
        self.checkout_message = f"Order placed! Total: ${total:.2f}. Thanks for shopping at Nexus Games!"

    @rx.var
    def cart_count(self) -> int:
        return sum(item.quantity for item in self.cart_items)

    @rx.var
    def cart_total(self) -> float:
        return sum(item.price * item.quantity for item in self.cart_items)

    @rx.var
    def filtered_games(self) -> list[Game]:
        query = self.search_query.strip().lower()
        results: list[Game] = []
        for game in GAMES:
            if self.selected_category != "All" and game.category != self.selected_category:
                continue
            if query and query not in game.title.lower() and query not in game.category.lower():
                continue
            results.append(game)
        return results

    @rx.var
    def current_game(self) -> Game | None:
        return get_game_by_id(self.game_id)

    @rx.var
    def related_games(self) -> list[Game]:
        game = get_game_by_id(self.game_id)
        if not game:
            return []
        return [
            other
            for other in GAMES
            if other.category == game.category and other.id != game.id
        ][:3]
