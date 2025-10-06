init -880 python in cardgame:

    example_card = Card(
        name="Example Card",
        type_=CardType.Action,
        description="This is an example card.",
        flavor="A well crafted example card is a marvel to behold.",
        image="gui/cardgame/images/default image.png",
    )

    example_stance = Card(
        name="Example Stance",
        type_=CardType.Stance,
        description="This is an example stance.",
        flavor="A well crafted example stance is a marvel to behold.",
        image="gui/cardgame/images/default image.png",
        keywords=Keywords.Defense
    )
    another_stance = Card(
        name="Another Stance",
        type_=CardType.Stance,
        description="This is another example stance.",
        flavor="A well crafted example stance is a marvel to behold.",
        image="gui/cardgame/images/default image.png",
        keywords=Keywords.Attack
    )