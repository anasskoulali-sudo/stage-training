"""Seed catalog, reviews, comments, and support tickets."""

from full_stack_python.models import Game, GameComment, GameReview, SupportTicket

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


SAMPLE_REVIEWS: list[GameReview] = [
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


SAMPLE_COMMENTS: list[GameComment] = [
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


SAMPLE_SUPPORT_TICKETS: list[SupportTicket] = [
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
        message="The game crashes on launch on my PC. I'd like a refund within the 14-day window.",
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
