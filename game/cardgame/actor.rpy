init -890 python in cardgame:
    import random

    class CardActorStats:
        def __init__(self, health: int, armor: int):
            self.health = health
            self.armor = armor
            self.max_health = health
            self.max_armor = armor
        
        def copy(self) -> 'CardActorStats':
            stats = CardActorStats(
                health=self.max_health,
                armor=self.max_armor
            )
            stats.health = self.health
            stats.armor = self.armor
            return stats

    class Deck:
        def __init__(self, name: str, wincon: Card = None, cards: list[Card] = []):
            self.name = name
            self.wincon = wincon
            self.cards = cards.copy() if cards else []
            self.discard_pile: list[Card] = []
            self.hand: list[Card] = []

        def copy(self) -> 'Deck':
            deck = Deck(
                name=self.name,
                wincon=self.wincon.copy() if self.wincon else None,
                cards=[c.copy() for c in self.cards]
            )
            deck.discard_pile = [c.copy() for c in self.discard_pile]
            deck.hand = [c.copy() for c in self.hand]
            return deck

        def shuffle(self, card_to_add: Card = None) -> None:
            if card_to_add:
                self.cards.append(card_to_add)
            random.shuffle(self.cards)

        def draw(self, amount: int = 1) -> list[Card]:
            drawn = self.cards[:amount]
            self.cards = self.cards[amount:]
            self.hand.extend(drawn)
            return drawn
            
        def discard(self, card: Card) -> None:
            self.discard_pile.append(card)

        @property
        def deck_size(self) -> int:
            return len(self.cards)
        @property
        def hand_size(self) -> int:
            return len(self.hand)
        @property
        def discard_size(self) -> int:
            return len(self.discard_pile)
        def __repr__(self):
            return f"Deck({self.name}, {self.deck_size} cards, Wincon: {self.wincon.name if self.wincon else 'None'})"

    class CardActor:
        game: 'CardGame' = None
        opponent: 'CardActor' = None
        _stances: list['Card'] = []
        _player_effects: list['Card'] = []
    
        def __init__(self, name: str, stats: CardActorStats, deck: 'Deck'):
            renpy.log(f"Creating CardActor: {name}")
            self.name = name
            self.stats = stats
            self.deck = deck

        def copy(self) -> 'CardActor':
            renpy.log(f"Copying CardActor: {self.name}")
            actor = CardActor(
                name=self.name,
                stats=self.stats.copy() if self.stats else None,
                deck=self.deck.copy() if self.deck else None
            )
            actor.game = self.game
            actor.opponent = self.opponent
            actor._stances = [s.copy() for s in self._stances]
            actor._player_effects = [e.copy() for e in self._player_effects]
            return actor

        @property
        def stances(self) -> list['Card']:
            return self._stances

        def add_stance(self, card: 'Card'):
            renpy.log(f"Adding stance to {self.name}: {card}")
            if card.type_ != CardType.Stance:
                raise ValueError("Can only add stances with add_stance()")
            # Remove any conflicting stances and call hooks
            removed_stances = [s for s in self._stances if s.keywords and s.keywords.intersection(card.keywords)]
            card_event = CardEvent(self, self.opponent, card)
            for s in removed_stances:
                for c in self.persistent_cards:
                    c.call_on_lose_stance(card_event, s)
                for c in self.opponent.persistent_cards:
                    c.call_on_enemy_lose_stance(card_event, s)
            # Add the new stance and call hooks
            self._stances = [s for s in self._stances if not s.keywords or not s.keywords.intersection(card.keywords)]
            for c in self.persistent_cards + self.opponent.persistent_cards:
                c.call_on_gain_stance(card_event, self, True)
            self._stances.append(card)

        @property
        def player_effects(self) -> list['Card']:
            return self._player_effects

        @property
        def persistent_cards(self) -> list['Card']:
            return self.stances + self.player_effects + [self.deck.wincon] if self.deck.wincon else []

        def reduce_health(self, amount: int, card: 'Card', event: 'CardEvent', ignore_armor: bool = False):
            renpy.log(f"Reducing health for {self.name}: {amount}")
            # Call my own hooks
            for c in self.persistent_cards:
                amount = c.call_on_lose_health(event, amount)
            # Call opponent's hooks
            for c in self.opponent.persistent_cards:
                amount = c.call_on_enemy_lose_health(event, amount)
            if ignore_armor:
                event.game.announce(f"{self.name}’s armor is ignored!")
            else:
                amount = amount - self.armor if not ignore_armor else amount
            # Resist if armor completely negates the damage
            if amount <= 0:
                self.game.announce(f"{self.name}’s armor absorbs the damage!")
                return
            # Apply the damage
            self.health = max(0, self.health - amount)
            renpy.notify(f"{self.name} loses {amount} health!")
            # Call health adjusted hooks
            for c in self.persistent_cards:
                c.call_on_health_adjusted(event)
            for c in self.opponent.persistent_cards:
                c.call_on_enemy_health_adjusted(event)

        def reduce_armor(self, amount: int, card: 'Card', event: 'CardEvent'):
            renpy.log(f"Reducing armor for {self.name}: {amount}")
            # Call hooks
            for c in self.persistent_cards:
                amount = c.call_on_lose_armor(event, amount)
            for c in self.opponent.persistent_cards:
                amount = c.call_on_enemy_lose_armor(event, amount)
            # Apply the damage
            self.armor = max(0, self.armor - amount)
            renpy.notify(f"{self.name} loses {amount} armor!")

        def gain_health(self, amount: int, card: 'Card', event: 'CardEvent'):
            renpy.log(f"Gaining health for {self.name}: {amount}")
            # Call hooks
            for c in self.persistent_cards:
                amount = c.call_on_gain_health(event, amount)
            for c in self.opponent.persistent_cards:
                amount = c.call_on_enemy_gain_health(event, amount)
            # Apply the gain
            self.health = min(self.max_health, self.health + amount)
            renpy.notify(f"{self.name} gains {amount} health!")

        def gain_armor(self, amount: int, card: 'Card', event: 'CardEvent'):
            renpy.log(f"Gaining armor for {self.name}: {amount}")
            # Call hooks
            for c in self.persistent_cards:
                amount = c.call_on_gain_armor(event, amount)
            for c in self.opponent.persistent_cards:
                amount = c.call_on_enemy_gain_armor(event, amount)
            # Apply the gain
            self.armor = min(self.max_armor, self.armor + amount)
            renpy.notify(f"{self.name} gains {amount} armor!")

        def draw(self, num_cards: int = 1) -> list['Card']:
            return self.deck.draw(num_cards)

        def shuffle_card_into_deck(self, card: 'Card'):
            self.deck.shuffle(card)