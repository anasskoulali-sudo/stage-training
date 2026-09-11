"""Reviews and comments against avis_produit and commentaire_produit."""

from datetime import datetime

from sqlmodel import select

from backend.db import get_session
from backend.models import AvisProduit, Commande, CommentaireProduit, LigneCommande, User
from full_stack_python.models import GameComment, GameReview


def _usernames(session) -> dict[int, str]:
    return {
        row.id_user: row.nom_de_compte
        for row in session.exec(select(User)).all()
        if row.id_user is not None
    }


def _has_purchased(session, user_id: int, product_id: int) -> bool:
    order_ids = session.exec(
        select(Commande.id_commande)
        .where(Commande.id_user == user_id)
        .where(Commande.statut != "annulee")
    ).all()
    if not order_ids:
        return False
    row = session.exec(
        select(LigneCommande.id_ligne)
        .where(LigneCommande.id_produit == product_id)
        .where(LigneCommande.id_commande.in_(order_ids))
    ).first()
    return row is not None


def list_reviews() -> list[GameReview]:
    with get_session() as session:
        names = _usernames(session)
        rows = session.exec(
            select(AvisProduit)
            .where(AvisProduit.statut_moderation == "publie")
            .order_by(AvisProduit.date_publication)
        ).all()
        return [
            GameReview(
                id=str(row.id_avis),
                game_id=str(row.id_produit),
                author=names.get(row.id_user, "Player"),
                rating=int(row.note),
                text=row.commentaire,
                user_id=row.id_user,
            )
            for row in rows
        ]


def list_comments() -> list[GameComment]:
    with get_session() as session:
        names = _usernames(session)
        rows = session.exec(
            select(CommentaireProduit)
            .where(CommentaireProduit.statut_moderation == "publie")
            .order_by(CommentaireProduit.date_creation)
        ).all()
        return [
            GameComment(
                id=str(row.id_commentaire),
                game_id=str(row.id_produit),
                author=names.get(row.id_user, "Player"),
                text=row.contenu,
                user_id=row.id_user,
            )
            for row in rows
        ]


def add_review(*, user_id: int, game_id: str, rating: int, text: str) -> None:
    product_id = int(game_id)
    with get_session() as session:
        verified = _has_purchased(session, user_id, product_id)
        session.add(
            AvisProduit(
                id_produit=product_id,
                id_user=user_id,
                note=rating,
                titre_avis=(text[:150] or None),
                commentaire=text,
                achat_verifie=1 if verified else 0,
                statut_moderation="publie",
                date_publication=datetime.now(),
            )
        )


def update_review(*, user_id: int, review_id: str, rating: int, text: str) -> bool:
    with get_session() as session:
        row = session.get(AvisProduit, int(review_id))
        if not row or row.id_user != user_id:
            return False
        row.note = rating
        row.titre_avis = text[:150] or None
        row.commentaire = text
        return True


def delete_review(*, user_id: int, review_id: str) -> bool:
    with get_session() as session:
        row = session.get(AvisProduit, int(review_id))
        if not row or row.id_user != user_id:
            return False
        session.delete(row)
        return True


def add_comment(*, user_id: int, game_id: str, text: str) -> None:
    with get_session() as session:
        session.add(
            CommentaireProduit(
                id_produit=int(game_id),
                id_user=user_id,
                contenu=text,
                statut_moderation="publie",
                date_creation=datetime.now(),
            )
        )


def update_comment(*, user_id: int, comment_id: str, text: str) -> bool:
    with get_session() as session:
        row = session.get(CommentaireProduit, int(comment_id))
        if not row or row.id_user != user_id:
            return False
        row.contenu = text
        return True


def delete_comment(*, user_id: int, comment_id: str) -> bool:
    with get_session() as session:
        row = session.get(CommentaireProduit, int(comment_id))
        if not row or row.id_user != user_id:
            return False
        session.delete(row)
        return True
