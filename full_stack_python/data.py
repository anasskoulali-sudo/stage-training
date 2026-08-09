"""Default catalog and site content for the gaming shop."""

from dataclasses import dataclass


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


DEFAULT_GAMES: list[Game] = [
    Game(
        id="elden-ring",
        title="Elden Ring",
        price=59.99,
        category="RPG",
        platform="PC / PlayStation / Xbox",
        image="https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600&h=340&fit=crop",
        description=(
            "A vast open-world action RPG from FromSoftware. Explore the Lands Between, "
            "forge your path, and become the Elden Lord."
        ),
        rating=4.9,
        featured=True,
    ),
    Game(
        id="god-of-war-ragnarok",
        title="God of War Ragnarök",
        price=49.99,
        category="Action",
        platform="PlayStation / PC",
        image="https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600&h=340&fit=crop",
        description=(
            "Kratos and Atreus must journey through the Nine Realms to prevent Ragnarök. "
            "Epic combat and a gripping Norse saga await."
        ),
        rating=4.8,
        featured=True,
    ),
    Game(
        id="zelda-totk",
        title="The Legend of Zelda: Tears of the Kingdom",
        price=69.99,
        category="Adventure",
        platform="Nintendo Switch",
        image="https://images.unsplash.com/photo-1552820728-8b8384996998?w=600&h=340&fit=crop",
        description=(
            "Link explores the skies and depths of Hyrule in this sprawling adventure "
            "packed with puzzles, dungeons, and discovery."
        ),
        rating=4.9,
        featured=True,
    ),
    Game(
        id="cyberpunk-2077",
        title="Cyberpunk 2077",
        price=39.99,
        category="RPG",
        platform="PC / PlayStation / Xbox",
        image="https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600&h=340&fit=crop",
        description=(
            "Become V, a mercenary in Night City. Customize your cyberware, build your legend, "
            "and survive the deadliest metropolis of the future."
        ),
        rating=4.5,
        featured=False,
    ),
    Game(
        id="hades-2",
        title="Hades II",
        price=29.99,
        category="Roguelike",
        platform="PC",
        image="https://images.unsplash.com/photo-1493711664972-763691281972?w=600&h=340&fit=crop",
        description=(
            "Battle through the Underworld as Melinoë, wielding dark sorcery and Olympian might "
            "in this acclaimed roguelike sequel."
        ),
        rating=4.8,
        featured=True,
    ),
    Game(
        id="street-fighter-6",
        title="Street Fighter 6",
        price=59.99,
        category="Fighting",
        platform="PC / PlayStation / Xbox",
        image="https://images.unsplash.com/photo-1538488886559-10f3850cc65c?w=600&h=340&fit=crop",
        description=(
            "The next evolution of the legendary fighting franchise. Master the Drive System "
            "and dominate in World Tour and Fighting Ground modes."
        ),
        rating=4.7,
        featured=False,
    ),
    Game(
        id="fc-26",
        title="EA Sports FC 26",
        price=69.99,
        category="Sports",
        platform="PC / PlayStation / Xbox",
        image="https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=600&h=340&fit=crop",
        description=(
            "Build your dream squad and compete in the world's most popular football simulation "
            "with updated leagues, modes, and realism."
        ),
        rating=4.2,
        featured=False,
    ),
    Game(
        id="silksong",
        title="Hollow Knight: Silksong",
        price=34.99,
        category="Metroidvania",
        platform="PC / Nintendo Switch",
        image="https://images.unsplash.com/photo-1612287230202-1ff1d85c1fff?w=600&h=340&fit=crop",
        description=(
            "Play as Hornet in Pharloom, a kingdom of silk and song. Precision platforming "
            "and challenging boss fights define this sequel."
        ),
        rating=4.9,
        featured=True,
    ),
    Game(
        id="baldurs-gate-3",
        title="Baldur's Gate 3",
        price=59.99,
        category="RPG",
        platform="PC / PlayStation / Xbox",
        image="https://images.unsplash.com/photo-1511884642898-4c92249e20b6?w=600&h=340&fit=crop",
        description=(
            "Gather your party and return to the Forgotten Realms in a story-rich CRPG "
            "where your choices shape a tale of fellowship and betrayal."
        ),
        rating=5.0,
        featured=True,
    ),
    Game(
        id="mario-kart-world",
        title="Mario Kart World",
        price=59.99,
        category="Racing",
        platform="Nintendo Switch",
        image="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=340&fit=crop",
        description=(
            "Race across iconic tracks with Mario and friends. Drift, boost, and unleash "
            "items in the ultimate kart racing party game."
        ),
        rating=4.6,
        featured=False,
    ),
    Game(
        id="call-of-duty",
        title="Call of Duty: Black Ops",
        price=69.99,
        category="FPS",
        platform="PC / PlayStation / Xbox",
        image="https://images.unsplash.com/photo-1552820728-8b8384996998?w=600&h=340&fit=crop",
        description=(
            "Intense multiplayer combat and a cinematic campaign. Deploy with your squad "
            "and dominate the battlefield."
        ),
        rating=4.3,
        featured=False,
    ),
    Game(
        id="stardew-valley",
        title="Stardew Valley",
        price=14.99,
        category="Simulation",
        platform="PC / Nintendo Switch",
        image="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&h=340&fit=crop",
        description=(
            "Restore your grandfather's farm, befriend villagers, explore caves, and build "
            "the cozy rural life you've always wanted."
        ),
        rating=4.8,
        featured=False,
    ),
]
