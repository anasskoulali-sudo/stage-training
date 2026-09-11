"""UI dataclasses used by pages and components."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Category:
    id: str
    name: str
    slug: str
    description: str = ""


@dataclass
class Game:
    id: str
    title: str
    price: float
    category: str
    platform: str
    image: str
    description: str
    rating: float
    featured: bool = False
    visible: bool = True
    stock: int = 0
    price_ht: float = 0.0
    tva: float = 20.0
    editor: str = ""
    format_type: str = "dematerialise"


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
    id: str = ""
    user_id: int = 0


@dataclass
class GameComment:
    game_id: str
    author: str
    text: str
    id: str = ""
    user_id: int = 0


@dataclass
class SupportTicket:
    author: str
    subject: str
    message: str
    category: str
    status: str
    created_at: str
    id: str = ""
    user_id: int = 0


SUPPORT_CATEGORY_TO_DB = {
    "Invalid key": "cle_invalide",
    "Delivery": "probleme_livraison",
    "Refund": "remboursement",
    "Account": "compte",
    "Other": "autre",
}
SUPPORT_CATEGORY_FROM_DB = {value: key for key, value in SUPPORT_CATEGORY_TO_DB.items()}
SUPPORT_CATEGORIES = list(SUPPORT_CATEGORY_TO_DB)

SUPPORT_STATUS_TO_DB = {
    "Open": "ouvert",
    "In Progress": "en_cours",
    "Waiting": "en_attente_client",
    "Resolved": "resolu",
    "Closed": "ferme",
}
SUPPORT_STATUS_FROM_DB = {value: key for key, value in SUPPORT_STATUS_TO_DB.items()}
DEFAULT_GAME_IMAGE = (
    "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600&h=340&fit=crop"
)
