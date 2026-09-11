"""SQLModel mappings for the live MySQL schema. Tables are not created or dropped."""

from datetime import date, datetime

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id_user: int | None = Field(default=None, primary_key=True)
    role: int = 2
    nom_de_compte: str
    email: str
    mot_de_passe: str
    mot_de_passe_clair: str | None = None
    nom: str | None = None
    prenom: str | None = None
    telephone: str | None = None
    date_inscription: datetime | None = None


class Categorie(SQLModel, table=True):
    __tablename__ = "categorie"

    id_categorie: int | None = Field(default=None, primary_key=True)
    nom: str
    slug: str
    description: str | None = Field(default=None, sa_column=Column(Text))


class Produit(SQLModel, table=True):
    __tablename__ = "produit"

    id_produit: int | None = Field(default=None, primary_key=True)
    id_categorie: int | None = None
    titre: str
    description: str | None = Field(default=None, sa_column=Column(Text))
    editeur: str | None = None
    plateforme: str
    type_format: str | None = "dematerialise"
    prix_unitaire_ht: float
    taux_tva: float | None = 20.0
    stock: int = 0
    cle_activation: str | None = None
    date_sortie: date | None = None
    date_ajout: datetime | None = None


class AvisProduit(SQLModel, table=True):
    __tablename__ = "avis_produit"

    id_avis: int | None = Field(default=None, primary_key=True)
    id_produit: int
    id_user: int
    note: int
    titre_avis: str | None = None
    commentaire: str = Field(sa_column=Column(Text))
    achat_verifie: int | None = 0
    statut_moderation: str | None = "publie"
    date_publication: datetime | None = None


class CommentaireProduit(SQLModel, table=True):
    __tablename__ = "commentaire_produit"

    id_commentaire: int | None = Field(default=None, primary_key=True)
    id_produit: int
    id_user: int
    id_commentaire_parent: int | None = None
    contenu: str = Field(sa_column=Column(Text))
    statut_moderation: str | None = "publie"
    date_creation: datetime | None = None


class Commande(SQLModel, table=True):
    __tablename__ = "commande"

    id_commande: int | None = Field(default=None, primary_key=True)
    id_user: int
    date_commande: datetime | None = None
    statut: str | None = "en_attente"
    montant_total_ttc: float = 0.0


class LigneCommande(SQLModel, table=True):
    __tablename__ = "ligne_commande"

    id_ligne: int | None = Field(default=None, primary_key=True)
    id_commande: int
    id_produit: int
    quantite: int = 1
    prix_unitaire_ttc: float
    nom_destinataire: str | None = None
    rue_livraison: str | None = None
    complement_livraison: str | None = None
    code_postal_livraison: str | None = None
    ville_livraison: str | None = None
    pays_livraison: str | None = "France"
    instructions_livraison: str | None = Field(default=None, sa_column=Column(Text))


class Paiement(SQLModel, table=True):
    __tablename__ = "paiement"

    id_paiement: int | None = Field(default=None, primary_key=True)
    id_commande: int
    mode_paiement: str
    statut_paiement: str | None = "en_attente"
    reference_transaction: str | None = None
    montant: float
    date_paiement: datetime | None = None


class TicketSupport(SQLModel, table=True):
    __tablename__ = "ticket_support"

    id_ticket: int | None = Field(default=None, primary_key=True)
    id_user: int
    id_commande: int | None = None
    id_agent_assigne: int | None = None
    numero_ticket: str
    sujet: str
    categorie_probleme: str
    priorite: str | None = "normale"
    statut: str | None = "ouvert"
    date_creation: datetime | None = None
    date_mise_a_jour: datetime | None = None


class TicketMessage(SQLModel, table=True):
    __tablename__ = "messagerie"

    id_message: int | None = Field(default=None, primary_key=True)
    id_ticket: int
    id_user: int
    message: str = Field(sa_column=Column(Text))
    piece_jointe_url: str | None = None
    date_envoi: datetime | None = None


class ParametreSite(SQLModel, table=True):
    __tablename__ = "parametres_site"
    __table_args__ = {"schema": "stage_parametrage"}

    id_parametre: int | None = Field(default=None, primary_key=True)
    cle: str
    valeur: str = Field(sa_column=Column(Text))
    description: str | None = None
