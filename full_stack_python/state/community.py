"""Reviews and comments loaded from MySQL."""

import reflex as rx

from backend.services.community import (
    add_comment,
    add_review,
    delete_comment,
    delete_review,
    list_comments,
    list_reviews,
    update_comment,
    update_review,
)
from full_stack_python.models import GameComment, GameReview
from full_stack_python.state.auth import AuthState
from full_stack_python.state.catalog import CatalogState


class CommunityState(rx.State):
    reviews: list[GameReview] = []
    comments: list[GameComment] = []
    new_review_rating: str = "5"
    new_review_text: str = ""
    new_comment_text: str = ""
    editing_review_id: str = ""
    editing_comment_id: str = ""
    edit_review_rating: str = "5"
    edit_review_text: str = ""
    edit_comment_text: str = ""
    review_message: str = ""
    comment_message: str = ""

    @rx.event
    def load_community(self):
        self.reviews = list_reviews()
        self.comments = list_comments()

    @rx.event
    def set_new_review_rating(self, value: str):
        self.new_review_rating = value

    @rx.event
    def set_new_review_text(self, value: str):
        self.new_review_text = value

    @rx.event
    def set_new_comment_text(self, value: str):
        self.new_comment_text = value

    @rx.event
    def set_edit_review_rating(self, value: str):
        self.edit_review_rating = value

    @rx.event
    def set_edit_review_text(self, value: str):
        self.edit_review_text = value

    @rx.event
    def set_edit_comment_text(self, value: str):
        self.edit_comment_text = value

    def _find_review(self, review_id: str) -> GameReview | None:
        for review in self.reviews:
            if review.id == review_id:
                return review
        return None

    def _find_comment(self, comment_id: str) -> GameComment | None:
        for comment in self.comments:
            if comment.id == comment_id:
                return comment
        return None

    @rx.event
    async def submit_review(self):
        auth = await self.get_state(AuthState)
        if not auth.is_logged_in or not auth.is_customer:
            self.review_message = "Sign in with a customer account to leave a review."
            return
        text = self.new_review_text.strip()
        if not text:
            self.review_message = "Write something for your review."
            return
        try:
            rating = max(1, min(5, int(self.new_review_rating)))
        except ValueError:
            rating = 5
        add_review(user_id=auth.user_id, game_id=self.game_id, rating=rating, text=text)
        self.new_review_text = ""
        self.new_review_rating = "5"
        self.review_message = "Review posted!"
        self.load_community()
        catalog = await self.get_state(CatalogState)
        catalog.load_catalog()

    @rx.event
    async def submit_comment(self):
        auth = await self.get_state(AuthState)
        if not auth.is_logged_in or not auth.is_customer:
            self.comment_message = "Sign in with a customer account to post a comment."
            return
        text = self.new_comment_text.strip()
        if not text:
            self.comment_message = "Write a comment first."
            return
        add_comment(user_id=auth.user_id, game_id=self.game_id, text=text)
        self.new_comment_text = ""
        self.comment_message = "Comment posted!"
        self.load_community()

    @rx.event
    async def start_edit_review(self, review_id: str):
        auth = await self.get_state(AuthState)
        review = self._find_review(review_id)
        if not review or review.user_id != auth.user_id:
            return
        self.editing_review_id = review_id
        self.edit_review_rating = str(review.rating)
        self.edit_review_text = review.text

    @rx.event
    async def save_review_edit(self, review_id: str):
        auth = await self.get_state(AuthState)
        text = self.edit_review_text.strip()
        if not text:
            return
        try:
            rating = max(1, min(5, int(self.edit_review_rating)))
        except ValueError:
            rating = 5
        if not update_review(user_id=auth.user_id, review_id=review_id, rating=rating, text=text):
            return
        self.editing_review_id = ""
        self.review_message = "Review updated."
        self.load_community()
        catalog = await self.get_state(CatalogState)
        catalog.load_catalog()

    @rx.event
    async def cancel_review_edit(self):
        self.editing_review_id = ""
        self.edit_review_text = ""
        self.edit_review_rating = "5"

    @rx.event
    async def delete_review(self, review_id: str):
        auth = await self.get_state(AuthState)
        if not delete_review(user_id=auth.user_id, review_id=review_id):
            return
        if self.editing_review_id == review_id:
            self.editing_review_id = ""
        self.review_message = "Review removed."
        self.load_community()
        catalog = await self.get_state(CatalogState)
        catalog.load_catalog()

    @rx.event
    async def start_edit_comment(self, comment_id: str):
        auth = await self.get_state(AuthState)
        comment = self._find_comment(comment_id)
        if not comment or comment.user_id != auth.user_id:
            return
        self.editing_comment_id = comment_id
        self.edit_comment_text = comment.text

    @rx.event
    async def save_comment_edit(self, comment_id: str):
        auth = await self.get_state(AuthState)
        text = self.edit_comment_text.strip()
        if not text:
            return
        if not update_comment(user_id=auth.user_id, comment_id=comment_id, text=text):
            return
        self.editing_comment_id = ""
        self.comment_message = "Comment updated."
        self.load_community()

    @rx.event
    async def cancel_comment_edit(self):
        self.editing_comment_id = ""
        self.edit_comment_text = ""

    @rx.event
    async def delete_comment(self, comment_id: str):
        auth = await self.get_state(AuthState)
        if not delete_comment(user_id=auth.user_id, comment_id=comment_id):
            return
        if self.editing_comment_id == comment_id:
            self.editing_comment_id = ""
        self.comment_message = "Comment removed."
        self.load_community()

    @rx.event
    def clear_review_messages(self):
        self.review_message = ""
        self.comment_message = ""

    @rx.var
    def current_game_reviews(self) -> list[GameReview]:
        return [review for review in self.reviews if review.game_id == self.game_id]

    @rx.var
    def current_game_comments(self) -> list[GameComment]:
        return [comment for comment in self.comments if comment.game_id == self.game_id]

    @rx.var
    def current_game_review_count(self) -> int:
        return len(self.current_game_reviews)

    @rx.var
    def current_game_comment_count(self) -> int:
        return len(self.current_game_comments)
