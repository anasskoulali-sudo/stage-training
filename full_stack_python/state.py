"""Shared application state for the gaming shop."""

import re
from dataclasses import dataclass, field, replace
from uuid import UUID, uuid4

import reflex as rx

from full_stack_python.data import DEFAULT_GAMES, Game


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "game"


class AuthState(rx.State):
    username: str = ""
    password: str = ""
    logged_in_user: str = ""
    is_admin: bool = False
    login_error: str = ""

    @rx.event
    def set_username(self, value: str):
        self.username = value

    @rx.event
    def set_password(self, value: str):
        self.password = value

    @rx.event
    def login(self):
        user = self.username.strip()
        pwd = self.password.strip()
        if not user or not pwd:
            self.login_error = "Please enter a username and password."
            return
        if user == "admin" and pwd == "admin":
            self.logged_in_user = user
            self.is_admin = True
            self.login_error = ""
            self.password = ""
            return rx.redirect("/admin")
        self.logged_in_user = user
        self.is_admin = False
        self.login_error = ""
        self.password = ""

    @rx.event
    def logout(self):
        self.logged_in_user = ""
        self.is_admin = False
        self.username = ""
        self.password = ""
        self.login_error = ""
        return rx.redirect("/account")

    @rx.event
    def guard_admin(self):
        if not self.is_admin:
            return rx.redirect("/account")

    @rx.event
    def guard_customer(self):
        if not self.is_logged_in or self.is_admin:
            return rx.redirect("/account")

    @rx.var
    def is_logged_in(self) -> bool:
        return self.logged_in_user != ""

    @rx.var
    def is_customer(self) -> bool:
        return self.is_logged_in and not self.is_admin


@dataclass
class CartItem:
    game_id: str
    title: str
    price: float
    image: str
    quantity: int = 1
    id: UUID = field(default_factory=uuid4)


@dataclass
class GameReview:
    game_id: str
    author: str
    rating: int
    text: str
    id: UUID = field(default_factory=uuid4)


@dataclass
class GameComment:
    game_id: str
    author: str
    text: str
    id: UUID = field(default_factory=uuid4)


def _sample_reviews() -> list[GameReview]:
    return [
        GameReview(
            game_id="elden-ring",
            author="Alex",
            rating=5,
            text="An incredible open world. Combat feels tight and the exploration never gets old.",
        ),
        GameReview(
            game_id="elden-ring",
            author="Sam",
            rating=4,
            text="Challenging but fair. Took me 80 hours and I loved every minute.",
        ),
        GameReview(
            game_id="baldurs-gate-3",
            author="Jordan",
            rating=5,
            text="Best RPG in years. The story branches are amazing.",
        ),
        GameReview(
            game_id="hades-2",
            author="Riley",
            rating=5,
            text="Even better than the first. The art and music are top tier.",
        ),
    ]


def _sample_comments() -> list[GameComment]:
    return [
        GameComment(
            game_id="elden-ring",
            author="Chris",
            text="Pro tip: explore Limgrave thoroughly before heading north.",
        ),
        GameComment(
            game_id="elden-ring",
            author="Morgan",
            text="Does this run well on Steam Deck for anyone?",
        ),
        GameComment(
            game_id="zelda-totk",
            author="Taylor",
            text="The building mechanics alone are worth the price.",
        ),
        GameComment(
            game_id="baldurs-gate-3",
            author="Casey",
            text="Playing co-op with friends makes this a whole different game.",
        ),
        GameComment(
            game_id="hades-2",
            author="Jamie",
            text="Melinoë's dash attack combo is so satisfying.",
        ),
    ]


@dataclass
class SupportTicket:
    author: str
    subject: str
    message: str
    category: str
    status: str
    created_at: str
    id: UUID = field(default_factory=uuid4)


def _sample_support_tickets() -> list[SupportTicket]:
    return [
        SupportTicket(
            author="Alex",
            subject="Order not received",
            message=(
                "I ordered Elden Ring three days ago but still haven't received my download code. "
                "Can you check my order status?"
            ),
            category="Order",
            status="Open",
            created_at="Aug 7, 2026",
        ),
        SupportTicket(
            author="Jordan",
            subject="Refund request — Cyberpunk 2077",
            message=(
                "The game crashes on launch on my PC. I'd like a refund within the 14-day window."
            ),
            category="Refund",
            status="In Progress",
            created_at="Aug 6, 2026",
        ),
        SupportTicket(
            author="Sam",
            subject="Can't sign in to my account",
            message="Password reset emails never arrive. I've checked spam folders twice.",
            category="Technical",
            status="Resolved",
            created_at="Aug 4, 2026",
        ),
        SupportTicket(
            author="Taylor",
            subject="Wrong region game key",
            message="I received a US key but I need an EU key for Nintendo Switch. Please swap it.",
            category="Order",
            status="Open",
            created_at="Aug 8, 2026",
        ),
        SupportTicket(
            author="Riley",
            subject="Double charge on checkout",
            message="My card was charged twice for the same order (#4821). Please refund one payment.",
            category="Billing",
            status="In Progress",
            created_at="Aug 5, 2026",
        ),
    ]


class ShopState(rx.State):
    games: list[Game] = [replace(game) for game in DEFAULT_GAMES]

    store_name: str = "Nexus Games"
    store_tagline: str = "Your gaming destination"
    footer_description: str = "The best place to discover and buy video games."
    copyright_text: str = "© 2026 Nexus Games. Built with Reflex."

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

    search_query: str = ""
    selected_category: str = "All"
    cart_items: list[CartItem] = []
    checkout_message: str = ""

    admin_message: str = ""
    admin_tab: str = "site"
    editing_game_id: str = ""
    form_title: str = ""
    form_price: str = ""
    form_category: str = ""
    form_platform: str = ""
    form_image: str = ""
    form_description: str = ""
    form_rating: str = ""
    form_featured: bool = False
    form_visible: bool = True

    reviews: list[GameReview] = _sample_reviews()
    comments: list[GameComment] = _sample_comments()
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

    support_tickets: list[SupportTicket] = _sample_support_tickets()
    support_subject: str = ""
    support_message: str = ""
    support_category: str = "Order"
    support_form_message: str = ""
    editing_ticket_id: str = ""
    edit_ticket_subject: str = ""
    edit_ticket_message: str = ""
    edit_ticket_category: str = "Order"

    @rx.event
    def set_support_subject(self, value: str):
        self.support_subject = value

    @rx.event
    def set_support_message(self, value: str):
        self.support_message = value

    @rx.event
    def set_support_category(self, value: str):
        self.support_category = value

    @rx.event
    def set_edit_ticket_subject(self, value: str):
        self.edit_ticket_subject = value

    @rx.event
    def set_edit_ticket_message(self, value: str):
        self.edit_ticket_message = value

    @rx.event
    def set_edit_ticket_category(self, value: str):
        self.edit_ticket_category = value

    @rx.event
    async def submit_support_ticket(self):
        auth = await self.get_state(AuthState)
        if not auth.is_logged_in:
            self.support_form_message = "Sign in to contact customer support."
            return
        if auth.is_admin:
            self.support_form_message = "Admins manage support from the dashboard."
            return
        subject = self.support_subject.strip()
        message = self.support_message.strip()
        if not subject or not message:
            self.support_form_message = "Please fill in the subject and message."
            return
        self.support_tickets = [
            SupportTicket(
                author=auth.logged_in_user,
                subject=subject,
                message=message,
                category=self.support_category,
                status="Open",
                created_at="Just now",
            ),
            *self.support_tickets,
        ]
        self.support_subject = ""
        self.support_message = ""
        self.support_category = "Order"
        self.support_form_message = "Your message was sent to customer support!"

    @rx.event
    async def start_edit_ticket(self, ticket_id: UUID):
        auth = await self.get_state(AuthState)
        ticket = self._find_ticket(ticket_id)
        if not ticket or ticket.author != auth.logged_in_user:
            return
        self.editing_ticket_id = str(ticket_id)
        self.edit_ticket_subject = ticket.subject
        self.edit_ticket_message = ticket.message
        self.edit_ticket_category = ticket.category

    @rx.event
    async def save_ticket_edit(self, ticket_id: UUID):
        auth = await self.get_state(AuthState)
        ticket = self._find_ticket(ticket_id)
        if not ticket or ticket.author != auth.logged_in_user:
            return
        subject = self.edit_ticket_subject.strip()
        message = self.edit_ticket_message.strip()
        if not subject or not message:
            return
        ticket.subject = subject
        ticket.message = message
        ticket.category = self.edit_ticket_category
        self.editing_ticket_id = ""
        self.support_form_message = "Support request updated."

    @rx.event
    def cancel_ticket_edit(self):
        self.editing_ticket_id = ""
        self.edit_ticket_subject = ""
        self.edit_ticket_message = ""
        self.edit_ticket_category = "Order"

    @rx.event
    async def delete_support_ticket(self, ticket_id: UUID):
        auth = await self.get_state(AuthState)
        ticket = self._find_ticket(ticket_id)
        if not ticket or ticket.author != auth.logged_in_user:
            return
        self.support_tickets = [t for t in self.support_tickets if t.id != ticket_id]
        if self.editing_ticket_id == str(ticket_id):
            self.cancel_ticket_edit()
        self.support_form_message = "Support request removed."

    @rx.event
    def set_ticket_status(self, ticket_id: UUID, status: str):
        ticket = self._find_ticket(ticket_id)
        if ticket:
            ticket.status = status
            self.admin_message = f"Ticket marked as {status}."

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

    @rx.event
    async def submit_review(self):
        auth = await self.get_state(AuthState)
        if not auth.is_logged_in:
            self.review_message = "Sign in to leave a review."
            return
        text = self.new_review_text.strip()
        if not text:
            self.review_message = "Write something for your review."
            return
        try:
            rating = max(1, min(5, int(self.new_review_rating)))
        except ValueError:
            rating = 5
        self.reviews = [
            *self.reviews,
            GameReview(
                game_id=self.game_id,
                author=auth.logged_in_user,
                rating=rating,
                text=text,
            ),
        ]
        self.new_review_text = ""
        self.new_review_rating = "5"
        self.review_message = "Review posted!"

    @rx.event
    async def submit_comment(self):
        auth = await self.get_state(AuthState)
        if not auth.is_logged_in:
            self.comment_message = "Sign in to post a comment."
            return
        text = self.new_comment_text.strip()
        if not text:
            self.comment_message = "Write a comment first."
            return
        self.comments = [
            *self.comments,
            GameComment(
                game_id=self.game_id,
                author=auth.logged_in_user,
                text=text,
            ),
        ]
        self.new_comment_text = ""
        self.comment_message = "Comment posted!"

    @rx.event
    async def start_edit_review(self, review_id: UUID):
        auth = await self.get_state(AuthState)
        review = self._find_review(review_id)
        if not review or review.author != auth.logged_in_user:
            return
        self.editing_review_id = str(review_id)
        self.edit_review_rating = str(review.rating)
        self.edit_review_text = review.text

    @rx.event
    async def save_review_edit(self, review_id: UUID):
        auth = await self.get_state(AuthState)
        review = self._find_review(review_id)
        if not review or review.author != auth.logged_in_user:
            return
        text = self.edit_review_text.strip()
        if not text:
            return
        try:
            review.rating = max(1, min(5, int(self.edit_review_rating)))
        except ValueError:
            pass
        review.text = text
        self.editing_review_id = ""
        self.review_message = "Review updated."

    @rx.event
    async def cancel_review_edit(self):
        self.editing_review_id = ""
        self.edit_review_text = ""
        self.edit_review_rating = "5"

    @rx.event
    async def delete_review(self, review_id: UUID):
        auth = await self.get_state(AuthState)
        review = self._find_review(review_id)
        if not review or review.author != auth.logged_in_user:
            return
        self.reviews = [item for item in self.reviews if item.id != review_id]
        if self.editing_review_id == str(review_id):
            self.editing_review_id = ""
        self.review_message = "Review removed."

    @rx.event
    async def start_edit_comment(self, comment_id: UUID):
        auth = await self.get_state(AuthState)
        comment = self._find_comment(comment_id)
        if not comment or comment.author != auth.logged_in_user:
            return
        self.editing_comment_id = str(comment_id)
        self.edit_comment_text = comment.text

    @rx.event
    async def save_comment_edit(self, comment_id: UUID):
        auth = await self.get_state(AuthState)
        comment = self._find_comment(comment_id)
        if not comment or comment.author != auth.logged_in_user:
            return
        text = self.edit_comment_text.strip()
        if not text:
            return
        comment.text = text
        self.editing_comment_id = ""
        self.comment_message = "Comment updated."

    @rx.event
    async def cancel_comment_edit(self):
        self.editing_comment_id = ""
        self.edit_comment_text = ""

    @rx.event
    async def delete_comment(self, comment_id: UUID):
        auth = await self.get_state(AuthState)
        comment = self._find_comment(comment_id)
        if not comment or comment.author != auth.logged_in_user:
            return
        self.comments = [item for item in self.comments if item.id != comment_id]
        if self.editing_comment_id == str(comment_id):
            self.editing_comment_id = ""
        self.comment_message = "Comment removed."

    @rx.event
    def clear_review_messages(self):
        self.review_message = ""
        self.comment_message = ""

    @rx.event
    def set_search(self, value: str):
        self.search_query = value

    @rx.event
    def set_category(self, category: str):
        self.selected_category = category

    @rx.event
    def set_admin_tab(self, tab: str):
        self.admin_tab = tab

    @rx.event
    def set_store_name(self, value: str):
        self.store_name = value

    @rx.event
    def set_store_tagline(self, value: str):
        self.store_tagline = value

    @rx.event
    def set_footer_description(self, value: str):
        self.footer_description = value

    @rx.event
    def set_copyright_text(self, value: str):
        self.copyright_text = value

    @rx.event
    def set_hero_badge(self, value: str):
        self.hero_badge = value

    @rx.event
    def set_hero_title(self, value: str):
        self.hero_title = value

    @rx.event
    def set_hero_subtitle(self, value: str):
        self.hero_subtitle = value

    @rx.event
    def set_shop_title(self, value: str):
        self.shop_title = value

    @rx.event
    def set_shop_subtitle(self, value: str):
        self.shop_subtitle = value

    @rx.event
    def set_about_title(self, value: str):
        self.about_title = value

    @rx.event
    def set_about_description(self, value: str):
        self.about_description = value

    @rx.event
    def set_about_feature_1_title(self, value: str):
        self.about_feature_1_title = value

    @rx.event
    def set_about_feature_1_text(self, value: str):
        self.about_feature_1_text = value

    @rx.event
    def set_about_feature_2_title(self, value: str):
        self.about_feature_2_title = value

    @rx.event
    def set_about_feature_2_text(self, value: str):
        self.about_feature_2_text = value

    @rx.event
    def set_about_feature_3_title(self, value: str):
        self.about_feature_3_title = value

    @rx.event
    def set_about_feature_3_text(self, value: str):
        self.about_feature_3_text = value

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
    def set_form_image(self, value: str):
        self.form_image = value

    @rx.event
    def set_form_description(self, value: str):
        self.form_description = value

    @rx.event
    def set_form_rating(self, value: str):
        self.form_rating = value

    @rx.event
    def set_form_featured(self, value: bool):
        self.form_featured = value

    @rx.event
    def set_form_visible(self, value: bool):
        self.form_visible = value

    @rx.event
    def on_load_shop(self):
        category = self.router.url.query_parameters.get("category", "All")
        if category == "All" or category in self.categories:
            self.selected_category = category

    @rx.event
    def start_new_game(self):
        self.editing_game_id = ""
        self.form_title = ""
        self.form_price = ""
        self.form_category = ""
        self.form_platform = ""
        self.form_image = ""
        self.form_description = ""
        self.form_rating = "4.5"
        self.form_featured = False
        self.form_visible = True
        self.admin_tab = "games"
        self.admin_message = "Fill in the form below to add a new game."

    @rx.event
    def load_game_for_edit(self, game_id: str):
        game = self._find_game(game_id)
        if not game:
            self.admin_message = "Game not found."
            return
        self.editing_game_id = game.id
        self.form_title = game.title
        self.form_price = f"{game.price:.2f}"
        self.form_category = game.category
        self.form_platform = game.platform
        self.form_image = game.image
        self.form_description = game.description
        self.form_rating = f"{game.rating:.1f}"
        self.form_featured = game.featured
        self.form_visible = game.visible
        self.admin_tab = "games"
        self.admin_message = f"Editing {game.title}."

    @rx.event
    def save_game(self):
        title = self.form_title.strip()
        if not title:
            self.admin_message = "Title is required."
            return
        try:
            price = float(self.form_price.strip())
            rating = float(self.form_rating.strip())
        except ValueError:
            self.admin_message = "Price and rating must be valid numbers."
            return
        category = self.form_category.strip() or "Other"
        platform = self.form_platform.strip() or "Multi-platform"
        image = self.form_image.strip() or "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600&h=340&fit=crop"
        description = self.form_description.strip() or "No description yet."

        if self.editing_game_id:
            game = self._find_game(self.editing_game_id)
            if not game:
                self.admin_message = "Game not found."
                return
            game.title = title
            game.price = price
            game.category = category
            game.platform = platform
            game.image = image
            game.description = description
            game.rating = rating
            game.featured = self.form_featured
            game.visible = self.form_visible
            self.admin_message = f"Updated {title}."
        else:
            base_id = _slugify(title)
            game_id = base_id
            suffix = 1
            while self._find_game(game_id):
                game_id = f"{base_id}-{suffix}"
                suffix += 1
            self.games = [
                *self.games,
                Game(
                    id=game_id,
                    title=title,
                    price=price,
                    category=category,
                    platform=platform,
                    image=image,
                    description=description,
                    rating=rating,
                    featured=self.form_featured,
                    visible=self.form_visible,
                ),
            ]
            self.editing_game_id = game_id
            self.admin_message = f"Added {title} to the catalog."

    @rx.event
    def delete_game(self, game_id: str):
        game = self._find_game(game_id)
        if not game:
            return
        self.games = [item for item in self.games if item.id != game_id]
        self.cart_items = [item for item in self.cart_items if item.game_id != game_id]
        if self.editing_game_id == game_id:
            self.start_new_game()
        self.admin_message = f"Removed {game.title} from the catalog."

    @rx.event
    def toggle_featured(self, game_id: str):
        game = self._find_game(game_id)
        if game:
            game.featured = not game.featured
            self.admin_message = f"{game.title} featured: {game.featured}."

    @rx.event
    def toggle_visible(self, game_id: str):
        game = self._find_game(game_id)
        if game:
            game.visible = not game.visible
            self.admin_message = f"{game.title} visible: {game.visible}."

    @rx.event
    def add_to_cart(self, game_id: str):
        game = self._find_game(game_id)
        if not game or not game.visible:
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
        self.checkout_message = (
            f"Order placed! Total: ${total:.2f}. Thanks for shopping at {self.store_name}!"
        )

    def _find_game(self, game_id: str) -> Game | None:
        for game in self.games:
            if game.id == game_id:
                return game
        return None

    def _find_review(self, review_id: UUID) -> GameReview | None:
        for review in self.reviews:
            if review.id == review_id:
                return review
        return None

    def _find_comment(self, comment_id: UUID) -> GameComment | None:
        for comment in self.comments:
            if comment.id == comment_id:
                return comment
        return None

    def _find_ticket(self, ticket_id: UUID) -> SupportTicket | None:
        for ticket in self.support_tickets:
            if ticket.id == ticket_id:
                return ticket
        return None

    @rx.var
    def cart_count(self) -> int:
        return sum(item.quantity for item in self.cart_items)

    @rx.var
    def cart_total(self) -> float:
        return sum(item.price * item.quantity for item in self.cart_items)

    @rx.var
    def visible_games(self) -> list[Game]:
        return [game for game in self.games if game.visible]

    @rx.var
    def featured_games(self) -> list[Game]:
        return [game for game in self.visible_games if game.featured]

    @rx.var
    def categories(self) -> list[str]:
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
        game = self._find_game(self.game_id)
        if game and game.visible:
            return game
        return None

    @rx.var
    def related_games(self) -> list[Game]:
        game = self._find_game(self.game_id)
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

    @rx.var
    def is_editing_game(self) -> bool:
        return self.editing_game_id != ""

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

    @rx.var
    def open_support_count(self) -> int:
        return len([t for t in self.support_tickets if t.status == "Open"])

    @rx.var
    def support_ticket_count(self) -> int:
        return len(self.support_tickets)
