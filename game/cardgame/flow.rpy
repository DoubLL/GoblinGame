init python in cardgame:
    # temportary setup
    player_stats = CardActorStats(health=30, armor=3)
    enemy_stats = CardActorStats(health=30, armor=3)
    player_deck = Deck(name="Player Deck", wincon=example_card, cards=[example_card, example_stance]*7)
    enemy_deck = Deck(name="Enemy Deck", wincon=example_card, cards=[example_card, example_stance]*7)
    player = CardActor(name="Player", stats=player_stats, deck=player_deck.copy())
    enemy = CardActor(name="Enemy", stats=enemy_stats, deck=enemy_deck.copy())
    player.opponent = enemy
    enemy.opponent = player

default cardgame.round = 0
default cardgame.winner = None
default cardgame.current_actor = None
default cardgame.other_actor = None
default cardgame.ai = None # TODO: AI class
default cardgame.ai_selected_card = None
default cardgame.ai_passed = False
default cardgame.player_selected_card = None
default cardgame.player_passed = False
default cardgame.game_events = []

label cardgame:
    # temporary placeholder
    jump .start
    return

label .start:
    python:
        cardgame.round = 0
        cardgame.winner = None
        cardgame.game_events = []
        cardgame.player.deck = cardgame.player_deck.copy()
        cardgame.player.deck.shuffle()
        cardgame.enemy.deck = cardgame.enemy_deck.copy()
        cardgame.enemy.deck.shuffle()
    show screen cardgame_intro
    $ renpy.pause(0.75, hard=True)
    show screen cardgame_screen("cardgame.loop")
    jump .start_round

label .start_round:
    # TODO: show animation
    python:
        cardgame.round += 1
        cardgame.game_events.append(f"Round {cardgame.round} begins!")
        cardgame.current_actor = cardgame.player
        cardgame.other_actor = cardgame.enemy
        cardgame.player_passed = False
        cardgame.ai_passed = False
    call screen cardgame_new_round(cardgame.round)
    pause 0.25
    call .draw_cards(for_player=(5 if cardgame.round == 1 else 3), for_enemy=(5 if cardgame.round == 1 else 3))
    jump .wait

label .wait:
    $ renpy.pause(hard=True)
label .loop:
    if cardgame.winner:
        jump .end_game

    if cardgame.player_passed and cardgame.ai_passed:
        jump .end_round

    if cardgame.current_actor == cardgame.enemy:
        jump .enemy_turn

    else:
        jump .player_turn

label .end_game:
    if cardgame.winner == cardgame.player:
    # TODO: show victory animation
        "You win the game!"
    else:
        "You lose the game!"
    hide game_screen
    return # TODO: jump back to main game


label .player_turn:
    # TODO: everything
    if cardgame.player_selected_card is None:
        $ cardgame.player_passed = True
        $ cardgame.game_events.append(f"{cardgame.player.name} passes")
        call .pass_turn
    else:
        call .play_card(cardgame.player_selected_card[0], cardgame.player_selected_card[1])
    call .switch_actors
    jump .wait


label .enemy_turn:
    pause 0.5 # TODO: enemy thinking animation
    if cardgame.enemy.deck.hand_size > 3:
        $ cardgame.ai_selected_card = cardgame.enemy.deck.hand[0] # TODO: AI logic to select a card or pass
    else:
        $ cardgame.ai_selected_card = None
    if cardgame.ai_selected_card is None:
        $ cardgame.ai_passed = True
        $ cardgame.game_events.append(f"{cardgame.enemy.name} passes")
        call .pass_turn
    else:
        call .play_card(cardgame.ai_selected_card)
    call .switch_actors
    jump .wait


label .end_round:
    # TODO: call on_end_round hooks
    if cardgame.winner:
        jump .end_game
    jump .start_round

label .draw_cards(for_player=0,for_enemy=0):
    python:
        for i in range(max(for_player, for_enemy)):
            if i < for_player:
                card = cardgame.player.deck.pop_card()
                if card:
                    renpy.show_screen("player_draws_card", card, _tag=f"player_draw_{i}")
            if i < for_enemy:
                card = cardgame.enemy.deck.pop_card()
                if card:
                    renpy.show_screen("enemy_draws_card", card, _tag=f"enemy_draws_{i}")
            if callable(renpy.pause):
                renpy.pause(0.25, hard=True)
    return

label .play_card(card, hand_index=None):
    python:
        for condition, message in card.conditions:
            if not condition[0](cardgame.current_actor, cardgame.other_actor, card):
                renpy.notify(message) # TODO: show error message as animation
                renpy.jump("cardgame.wait")
                
    if hand_index is not None:
        if hand_index < 0 or hand_index >= len(cardgame.current_actor.deck.hand):
            $ raise Exception("Invalid hand index")
        $ cardgame.current_actor.deck.hand.pop(hand_index)
    else:
        $ cardgame.current_actor.deck.hand.remove(card)

    python:
        cardevent = cardgame.CardEvent(card_owner=cardgame.current_actor, opponent=cardgame.other_actor, card=card)
        for c in cardgame.current_actor.persistent_cards:
            c.call_on_other_card_played(cardevent, True)
        for c in cardgame.other_actor.persistent_cards:
            c.call_on_other_card_played(cardevent, False)

    call screen play_card(
        card,
        is_player=(cardgame.current_actor == cardgame.player),
        is_stance=(card.type_ == cardgame.CardType.Stance)
        )
    pause 0.5 # let animation finish
    $ cardgame.game_events.append(card) # TODO: Use cardevent instead to determine actor
    if card.type_ == cardgame.CardType.Stance:
        call .add_stance(card)
    else:
        $ cardgame.current_actor.deck.discard(card)
    
    jump .switch_actors

label .add_stance(card):
    # TODO: add stance animation
    # TODO: play animation for removing old stance if needed
    $ cardgame.current_actor.add_stance(card)
    return

label .pass_turn:
    # TODO: play pass animation
    return

label .switch_actors:
    if cardgame.player_passed and cardgame.ai_passed:
        jump .end_round
    if cardgame.current_actor == cardgame.player:
        if cardgame.ai_passed:
            jump .wait
        $ cardgame.current_actor = cardgame.enemy
        $ cardgame.other_actor = cardgame.player
        jump .loop
    else:
        if cardgame.player_passed:
            jump .loop
        $ cardgame.current_actor = cardgame.player
        $ cardgame.other_actor = cardgame.enemy
        jump .wait
    $ raise Exception("Unreachable")