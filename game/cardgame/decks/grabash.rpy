init -880 python in cardgame:

    def brute_force_on_enemy_health_adjusted(self: 'Card', event: 'CardEvent'):
        if cardgame.game.opponent.health <= 0:
            cardgame.game.announce(f"{cardgame.game.player.name} wins the game with Brute Force!")
            cardgame.game.winner = cardgame.game.player
    wincon = Card(
        name="Brute Force",
        type_=CardType.WinCon,
        description="If the opponent has 0 HP, you win the game.",
        flavor="When in doubt, bash them over the head.",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_ENEMY_HEALTH_ADJUSTED: brute_force_on_enemy_health_adjusted},
        keywords=Keywords.Attack
    )
    def burn_it_on_round_end(self: 'Card', event: 'CardEvent'):
        event.opponent.reduce_health(2, self, event, ignore_armor=True)
    burn_it = Card(
        name="Burn It!",
        type_=CardType.Stance,
        description="At the end of every round, deal 2 Unmodifiable Damage to your opponent.",
        flavor="Sometimes you just have to burn it all down.",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_END_ROUND: burn_it_on_round_end},
        keywords=Keywords.Attack
    )
    def goblin_mode_on_other_card_played(self: 'Card', event: 'CardEvent', is_mine: bool):
        if is_mine and event.card.keywords & Keywords.Attack:
            event.opponent.reduce_health(1, self, event, ignore_armor=True)
        elif is_mine and event.card.keywords & Keywords.Defense:
            event.card_owner.remove_stance(self)
    goblin_mode = Card(
        name="Goblin Mode",
        type_=CardType.Stance,
        description="Whenever you play an Attack card, deal 1 Unmodifiable Damage to your opponent. If you play a Defense card, remove this Stance.",
        flavor="Once you go-blin, you always go in.",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_OTHER_CARD_PLAYED: goblin_mode_on_other_card_played},
        keywords=Keywords.Attack
    )
    def cling_on_other_card_played(self: 'Card', event: 'CardEvent', is_mine: bool):
        if event.card.keywords & Keywords.Attack:
            event.card_owner.reduce_health(1, self, event, ignore_armor=True)
            event.opponent.reduce_health(2, self, event, ignore_armor=True)
    cling = Card(
        name="Cling",
        type_=CardType.Stance,
        description="Whenever an Attack card is played, you take 1 Unmodifiable Damage and your opponent takes 2 Unmodifiable Damage.",
        flavor="Close Quarters Combat",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_OTHER_CARD_PLAYED: cling_on_other_card_played},
        keywords=Keywords.Grapple
    )
    def rip_and_tear_on_play(self: 'Card', event: 'CardEvent'):
        event.opponent.reduce_armor(2, self, event)
        event.card_owner.reduce_health(event.opponent.armor, self, event, ignore_armor=True)
    rip_and_tear = Card(
        name="Rip and Tear",
        type_=CardType.Action,
        description="Reduce your opponent's Armor by 2. Then, deal Unmodifiable Damage to yourself equal to their remaining Armor.",
        flavor="Rip and tear, until it is done.",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_PLAY: rip_and_tear_on_play},
        keywords=Keywords.Grapple
    )
    def ankle_bite_on_play(self: 'Card', event: 'CardEvent'):
        event.opponent.reduce_health(5, self, event)
    ankle_bite = Card(
        name="Ankle Bite",
        type_=CardType.Action,
        description="Deal 5 Damage to your opponent.",
        flavor="Ankles are vulnerable to small creatures.",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_PLAY: ankle_bite_on_play},
        keywords=Keywords.Attack
    )
    def iron_fist_on_play(self: 'Card', event: 'CardEvent'):
        event.opponent.reduce_health(event.card_owner.armor * 2, self, event)
    iron_fist = Card(
        name="Iron Fist",
        type_=CardType.Action,
        description="Deal 2 Damage to your opponent for each point of Armor you have.",
        flavor="All this metal has to be good for something.",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_PLAY: iron_fist_on_play},
        keywords=Keywords.Attack | Keywords.Defense
    )
    def retaliate_on_play(self: 'Card', event: 'CardEvent'):
        event.opponent.reduce_health(int((event.card_owner.max_health - event.card_owner.health) / 2), self, event)
    retaliate = Card(
        name="Retaliate",
        type_=CardType.Action,
        description="Deal 1 Damage to your opponent for every 2 Health you are missing.",
        flavor="You will pay for that!",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_PLAY: retaliate_on_play},
        keywords=Keywords.Attack
    )
    def rampage_on_play(self: 'Card', event: 'CardEvent'):
        event.opponent.reduce_health(3, self, event)
        event.card_owner.deck.draw(1)
    rampage = Card(
        name="Rampage",
        type_=CardType.Action,
        description="Deal 3 Damage to your opponent and draw a card.",
        flavor="Seize the initiative and crush everything!",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_PLAY: rampage_on_play},
        keywords=Keywords.Attack
    )
    def flail_wildly_on_play(self: 'Card', event: 'CardEvent'):
        event.opponent.stances.clear()
        event.card_owner.stances.clear()
        event.card_owner.add_stance(goblin_mode)
    flail_wildly = Card(
        name="Flail Wildly",
        type_=CardType.Action,
        description="Remove all Stances in play. Equip Goblin Mode.",
        flavor="No plan, no strategy, just pure chaos.",
        image="gui/cardgame/images/default image.png",
        hooks={HookType.ON_PLAY: flail_wildly_on_play},
        keywords=Keywords.Grapple
    )

    grabash_deck = Deck(
        name="Grabash's Deck",
        cards=[
            burn_it,
            goblin_mode,
            cling, cling,
            rip_and_tear, rip_and_tear, rip_and_tear,
            ankle_bite, ankle_bite, ankle_bite,
            iron_fist, iron_fist, iron_fist,
            retaliate, retaliate, retaliate,
            rampage, rampage,
            flail_wildly, flail_wildly,
        ],
        wincon=wincon,
    )
    grabash_stats = CardActorStats(20, 3)
    grabash = CardActor(name="Grabash", stats=grabash_stats, deck=grabash_deck)
