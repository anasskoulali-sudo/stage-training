"""Catalog loaded from MySQL produit and categorie tables."""

import reflex as rx

from backend.services.catalog import list_category_records, list_games
from full_stack_python.models import Category, Game


class CatalogState(rx.State):
    games: list[Game] = []
    category_names: list[str] = []
    category_records: list[Category] = []
    search_query: str = ""
    selected_category: str = "All"

    @rx.event
    def load_catalog(self):
        self.games = list_games()
        self.category_records = list_category_records()
        self.category_names = [row.name for row in self.category_records]

    @rx.event
    def set_search(self, value: str):
        self.search_query = value

    @rx.event
    def set_category(self, category: str):
        self.selected_category = category

    @rx.event
    def on_load_shop(self):
        self.load_catalog()
        category = self.router.url.query_parameters.get("category", "All")
        if category == "All" or category in self.categories:
            self.selected_category = category

    def find_game(self, game_id: str) -> Game | None:
        for game in self.games:
            if game.id == game_id:
                return game
        return None

    def find_category(self, category_id: str) -> Category | None:
        for category in self.category_records:
            if category.id == category_id:
                return category
        return None

    @rx.var
    def visible_games(self) -> list[Game]:
        return [game for game in self.games if game.visible]

    @rx.var
    def featured_games(self) -> list[Game]:
        return [game for game in self.visible_games if game.featured]

    @rx.var
    def categories(self) -> list[str]:
        if self.category_names:
            return self.category_names
        return sorted({game.category for game in self.visible_games})

    @rx.var
    def filtered_games(self) -> list[Game]:
        query = self.search_query.strip().lower()
        results: list[Game] = []
        for game in self.visible_games:
            if self.selected_category != "All" and game.category != self.selected_category:
                continue
            if query and query not in game.title.lower() and query not in game.category.lower():
                continue
            results.append(game)
        return results

    @rx.var
    def current_game(self) -> Game | None:
        game = self.find_game(self.game_id)
        if game and game.visible:
            return game
        return None

    @rx.var
    def related_games(self) -> list[Game]:
        game = self.find_game(self.game_id)
        if not game:
            return []
        return [
            other
            for other in self.visible_games
            if other.category == game.category and other.id != game.id
        ][:3]

    @rx.var
    def game_count(self) -> int:
        return len(self.games)

    @rx.var
    def visible_game_count(self) -> int:
        return len(self.visible_games)

    @rx.var
    def featured_game_count(self) -> int:
        return len(self.featured_games)

    @rx.var
    def category_count(self) -> int:
        return len(self.categories)
