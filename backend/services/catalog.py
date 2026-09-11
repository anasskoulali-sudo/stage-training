"""Catalog reads and writes against categorie and produit."""

from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select

from backend.db import get_session
from backend.models import AvisProduit, Categorie, Produit
from full_stack_python.models import DEFAULT_GAME_IMAGE, Category, Game
from full_stack_python.utils import slugify


def _ttc(price_ht: float, tva: float | None) -> float:
    rate = float(tva or 0)
    return round(float(price_ht) * (1 + rate / 100), 2)


def _to_game(produit: Produit, category_name: str, rating: float) -> Game:
    return Game(
        id=str(produit.id_produit),
        title=produit.titre,
        price=_ttc(produit.prix_unitaire_ht, produit.taux_tva),
        price_ht=float(produit.prix_unitaire_ht),
        tva=float(produit.taux_tva or 20),
        category=category_name or "Other",
        platform=produit.plateforme,
        image=DEFAULT_GAME_IMAGE,
        description=produit.description or "",
        rating=round(rating, 1),
        featured=True,
        visible=True,
        stock=produit.stock,
        editor=produit.editeur or "",
        format_type=produit.type_format or "dematerialise",
    )


def list_categories() -> list[str]:
    return [row.name for row in list_category_records()]


def list_category_records() -> list[Category]:
    with get_session() as session:
        rows = session.exec(select(Categorie).order_by(Categorie.nom)).all()
        return [
            Category(
                id=str(row.id_categorie),
                name=row.nom,
                slug=row.slug,
                description=row.description or "",
            )
            for row in rows
            if row.id_categorie is not None
        ]


def _unique_slug(session, name: str, exclude_id: int | None = None) -> str:
    base = slugify(name)
    slug = base
    suffix = 2
    while True:
        row = session.exec(select(Categorie).where(Categorie.slug == slug)).first()
        if row is None or row.id_categorie == exclude_id:
            return slug
        slug = f"{base}-{suffix}"
        suffix += 1


def save_category(*, category_id: str | None, name: str, description: str) -> str:
    name = name.strip()
    description = description.strip()
    if not name:
        raise ValueError("Category name is required.")
    if len(name) > 100:
        raise ValueError("Category name is too long.")
    with get_session() as session:
        exclude_id = int(category_id) if category_id else None
        duplicate = session.exec(select(Categorie).where(Categorie.nom == name)).first()
        if duplicate and duplicate.id_categorie != exclude_id:
            raise ValueError("A category with that name already exists.")
        slug = _unique_slug(session, name, exclude_id)
        if exclude_id is not None:
            row = session.get(Categorie, exclude_id)
            if not row:
                raise ValueError("Category not found.")
            row.nom = name
            row.slug = slug
            row.description = description or None
            return str(row.id_categorie)
        row = Categorie(nom=name, slug=slug, description=description or None)
        session.add(row)
        try:
            session.flush()
        except IntegrityError as exc:
            raise ValueError("Could not save category because that name or slug is already used.") from exc
        return str(row.id_categorie)


def delete_category(category_id: str) -> str | None:
    with get_session() as session:
        row = session.get(Categorie, int(category_id))
        if not row:
            return None
        used = session.exec(
            select(Produit.id_produit).where(Produit.id_categorie == row.id_categorie)
        ).first()
        if used:
            raise ValueError("This category still has products. Move or delete them first.")
        name = row.nom
        session.delete(row)
        return name


def _category_map(session) -> dict[int, str]:
    return {
        row.id_categorie: row.nom
        for row in session.exec(select(Categorie)).all()
        if row.id_categorie is not None
    }


def _category_id_by_name(session, name: str) -> int:
    row = session.exec(select(Categorie).where(Categorie.nom == name)).first()
    if not row or row.id_categorie is None:
        raise ValueError("Choose an existing category. Create categories in the Categories tab first.")
    return row.id_categorie


def _rating_map(session) -> dict[int, float]:
    rows = session.exec(
        select(AvisProduit.id_produit, func.avg(AvisProduit.note))
        .where(AvisProduit.statut_moderation == "publie")
        .group_by(AvisProduit.id_produit)
    ).all()
    return {int(product_id): float(avg or 0) for product_id, avg in rows}


def list_games() -> list[Game]:
    with get_session() as session:
        products = session.exec(select(Produit).order_by(Produit.titre)).all()
        names = _category_map(session)
        ratings = _rating_map(session)
        return [
            _to_game(
                product,
                names.get(product.id_categorie or 0, "Other"),
                ratings.get(product.id_produit or 0, 0.0),
            )
            for product in products
        ]


def save_product(
    *,
    product_id: str | None,
    title: str,
    price_ht: float,
    category: str,
    platform: str,
    description: str,
    editor: str,
    format_type: str,
    tva: float,
    stock: int,
) -> str:
    with get_session() as session:
        if not category.strip():
            raise ValueError("Choose an existing category. Create categories in the Categories tab first.")
        category_id = _category_id_by_name(session, category.strip())
        if product_id:
            product = session.get(Produit, int(product_id))
            if not product:
                raise ValueError("Game not found.")
            product.titre = title
            product.prix_unitaire_ht = price_ht
            product.id_categorie = category_id
            product.plateforme = platform
            product.description = description
            product.editeur = editor or None
            product.type_format = format_type or "dematerialise"
            product.taux_tva = tva
            product.stock = stock
            return str(product.id_produit)
        product = Produit(
            titre=title,
            prix_unitaire_ht=price_ht,
            id_categorie=category_id,
            plateforme=platform,
            description=description or None,
            editeur=editor or None,
            type_format=format_type or "dematerialise",
            taux_tva=tva,
            stock=stock,
        )
        session.add(product)
        try:
            session.flush()
        except IntegrityError as exc:
            raise ValueError("Could not save the product. Check that the category still exists.") from exc
        return str(product.id_produit)


def delete_product(product_id: str) -> str | None:
    with get_session() as session:
        product = session.get(Produit, int(product_id))
        if not product:
            return None
        title = product.titre
        session.delete(product)
        try:
            session.flush()
        except IntegrityError as exc:
            raise ValueError(
                "This game cannot be deleted while it has orders, reviews, or comments."
            ) from exc
        return title
