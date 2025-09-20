init -880 python in cardgame:

    from threading import Timer
    import random

    class Turn(Enum):
        Player = "Player"
        Opponent = "Opponent"

    class CardGame:
        winner = None
        player_passed = False
        opponent_passed = False

        def __init__(self, player: CardActor, opponent: CardActor):
            self.cards_played: list[str] = []
            self.cards_played_this_round: list[str] = []
            self.player = player.copy() if player else None
            self.opponent = opponent.copy() if opponent else None
            self.round = 0
            self.turn = Turn.Player
            if self.player:
                self.player.game = self
                self.player.opponent = self.opponent
            if self.opponent:
                self.opponent.game = self
                self.opponent.opponent = self.player


        def start_round(self):
            renpy.notify(f"Round {self.round} begins!")
            self.round += 1
            self.turn = Turn.Player
            self.cards_played_this_round = []
            self.player_passed = False
            self.opponent_passed = False
            self.announce(f"Round {self.round} begins!")
            for card in (self.player.stances + self.player.player_effects + [self.player.wincon]):
                card.call_on_start_round(CardEvent(self.player, self.opponent, self, None))
            for card in (self.opponent.stances + self.opponent.player_effects + [self.opponent.wincon]):
                card.call_on_start_round(CardEvent(self.opponent, self.player, self, None))
            # Draw 3 cards for player and opponent here, up to a maximum hand size of 7.
            # This should be affected by actor's stats
            self.player.draw_cards(3, max_hand_size=7)
            self.opponent.draw_cards(3, max_hand_size=7)
            renpy.notify(f"Player hand: {[card.name for card in self.player.hand]}")
        
        def end_round(self):
            self.announce(f"{self.turn.value}'s turn ended!")
            for cardName in (self.player.stances + self.player.player_effects + [self.player.wincon]):
                card.call_on_end_round(CardEvent(self.player, self.opponent, self, None))
            for cardName in (self.opponent.stances + self.opponent.player_effects + [self.opponent.wincon] + [self.opponent.wincon]):
                card.call_on_end_round(CardEvent(self.opponent, self.player, self, None))
            self.turn = Turn.Player
            if self.winner is None:
                self.start_round()
        
        def play_card(self, card: 'Card', hand_index: int = None) -> bool:
            # Determine actors
            actor = self.player if self.turn == Turn.Player else self.opponent
            opponent = self.opponent if self.turn == Turn.Player else self.player
            # Check conditions
            for cond, message in card.condition:
                if not cond(actor, opponent, self):
                    game.announce(message)
                    return False
#           # Remove card from hand
            if hand_index is not None:
                actor.hand.pop(hand_index)
            else:
                actor.hand.remove(card)
            # Trigger effects of cards already in play
            for c in (actor.stances + actor.player_effects):
                card = c.call_on_other_card_played(
                    CardEvent(actor, opponent, self, card),
                    self.turn == Turn.Player
                    )
            for c in (opponent.stances + opponent.player_effects):
                card = c.call_on_other_card_played(
                    CardEvent(actor, opponent, self, card),
                    self.turn == Turn.Opponent
                    )
            # Trigger the card's effect
            card = card.call_on_play(CardEvent(actor, opponent, self, card))
            # Show animation
            renpy.log(f"{actor.name} plays {card.name}")
            if self.turn == Turn.Player:
                renpy.log("Call in new context")
                renpy.call_in_new_context("cardgame_playcard_player", card=card, _clear_layers=False)
                renpy.log("Returned from new context")
            else:
                renpy.log("Call in new context")
                renpy.call_in_new_context("cardgame_playcard_opponent", card=card, _clear_layers=False)
                renpy.log("Returned from new context")
            # Add stances to list
            if card.type_ == CardType.Stance:
                actor.add_stance(card)
            # Shuffle actions back into the deck
            elif card.type_ == CardType.Action:
                renpy.log(f"Shuffle action back into deck {actor.name}")
                actor.shuffle_card_into_deck(card)
            renpy.log("Next turn")
            self.next_turn()
            return True

        def next_turn(self):
            if self.turn == Turn.Player:
                if self.opponent_passed:
                    return
                else:
                    self.turn = Turn.Opponent
            else:
                if self.player_passed:
                    return
                else:
                    self.turn = Turn.Player
            renpy.restart_interaction()
        
        def pass_turn(self, turn: Turn):
            if turn == Turn.Player:
                self.player_passed = True
                self.announce(f"{self.player.name} passes!")
            else:
                self.opponent_passed = True
                self.announce(f"{self.opponent.name} passes!")
            if self.player_passed and self.opponent_passed:
                self.end_round()
            else:
                self.next_turn()
        
        def do_opponent_turn(self):
            while self.turn == Turn.Opponent:
                if self.winner is not None:
                    return
                if not self.opponent.hand:
                    self.pass_turn(Turn.Opponent)
                    return False
                playable_cards = [
                    card for card in self.opponent.hand
                        if card.condition == []
                            or all(cond(self.opponent, self.player, self) for cond, msg in card.condition)
                    ]
                if not playable_cards:
                    self.pass_turn(Turn.Opponent)
                    return False
                self.play_card(renpy.random.choice(playable_cards))
                return True

        def announce(self, message: str):
            renpy.notify(message) # TODO: Better message display

        def attempt_win(self, actor: 'CardActor', trigger: 'Card', event: 'CardEvent'):
            renpy.log(f"{actor.name} attempts to win the game!")
            self.announce(f"{actor.name} wins the game!")
            self.winner = actor
            renpy.log(f"Game over! {actor.name} is the winner!")