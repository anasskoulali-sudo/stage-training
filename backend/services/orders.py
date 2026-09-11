"""Checkout writes commande, ligne_commande, and paiement."""

from datetime import datetime

from backend.db import get_session
from backend.models import Commande, LigneCommande, Paiement, Produit, User


def place_order(*, user_id: int, items: list[dict]) -> tuple[int, float]:
    if not items:
        raise ValueError("Your cart is empty.")
    with get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("Sign in to checkout.")
        lines: list[tuple[Produit, int, float]] = []
        total = 0.0
        for item in items:
            product = session.get(Produit, int(item["game_id"]))
            quantity = int(item["quantity"])
            if not product or quantity < 1:
                raise ValueError("A game in your cart is no longer available.")
            if product.stock < quantity:
                raise ValueError(f"{product.titre} does not have enough stock.")
            price = round(float(item["price"]), 2)
            total = round(total + price * quantity, 2)
            lines.append((product, quantity, price))
        order = Commande(
            id_user=user_id,
            date_commande=datetime.now(),
            statut="payee",
            montant_total_ttc=total,
        )
        session.add(order)
        session.flush()
        recipient = f"{user.prenom or ''} {user.nom or ''}".strip() or user.nom_de_compte
        for product, quantity, price in lines:
            session.add(
                LigneCommande(
                    id_commande=order.id_commande or 0,
                    id_produit=product.id_produit or 0,
                    quantite=quantity,
                    prix_unitaire_ttc=price,
                    nom_destinataire=recipient,
                    pays_livraison="France",
                )
            )
            product.stock -= quantity
        session.add(
            Paiement(
                id_commande=order.id_commande or 0,
                mode_paiement="carte_bancaire",
                statut_paiement="valide",
                reference_transaction=f"PAY-{order.id_commande}",
                montant=total,
                date_paiement=datetime.now(),
            )
        )
        return order.id_commande or 0, total
