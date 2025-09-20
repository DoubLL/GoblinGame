init python in cardgame:
    # temportary setup
    player_stats = CardActorStats(health=30, armor=3)
    enemy_stats = CardActorStats(health=30, armor=3)
    player_deck = Deck(name="Player Deck", wincon=None, cards=[example_card]*10)
    enemy_deck = Deck(name="Enemy Deck", wincon=None, cards=[example_card]*10)
    player = CardActor(name="Player", stats=player_stats, deck=player_deck)
    enemy = CardActor(name="Enemy", stats=enemy_stats, deck=enemy_deck)
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
    $ cardgame.round = 0
    $ cardgame.winner = None
    $ cardgame.game_events = []
    show screen cardgame_intro
    $ renpy.pause(0.75, hard=True)
    show screen cardgame_screen("cardgame.evaluate")
    call .draw_cards(for_player=2, for_enemy=2)
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
    # TODO: call on_start_round hooks
    call .draw_cards(for_player=3, for_enemy=3)
    jump .loop

label .loop:
    $ renpy.pause(hard=True)

label .evaluate:
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
        call .pass_turn
    else:
        call .play_card(cardgame.player_selected_card)
    call .switch_actors
    jump .loop


label .enemy_turn:
    $ cardgame.ai_selected_card = None # TODO: AI logic to select a card or pass
    if cardgame.ai_selected_card is None:
        $ cardgame.ai_passed = True
        call .pass_turn
    else:
        call .play_card(cardgame.ai_selected_card)
    call .switch_actors
    jump .loop


label .end_round:
    # TODO: call on_end_round hooks
    if cardgame.winner:
        jump .end_game
    jump .loop

label .draw_cards(for_player=0,for_enemy=0):
    # TODO: play animations
    if for_player > 0:
        $ cardgame.player.draw(for_player)
    if for_enemy > 0:
        $ cardgame.enemy.draw(for_enemy)
    return

label .play_card(card):
    # TODO: validate card can be played
    if not CAN_BE_PLAYED:
        # TODO: show error message
        jump .loop
    # TODO: remove card from hand
    # TODO: call on_other_card_played hooks
    # TODO: call on_play hooks
    # TODO: play card animation. Variations for player/enemy and action/stance
    $ cardgame.game_events.append(card)
    if card.type_ == CardType.Stance:
        call .add_stance(card)
    # TODO: add card to discard pile if action
    jump .loop

label .add_stance(card):
    # TODO: add stance animation
    # TODO: play animation for removing old stance if needed
    $ cardgame.current_actor.add_stance(card)
    return

label .pass_turn:
    # TODO: play pass animation
    return

label .switch_actors:
    if cardgame.current_actor == cardgame.player:
        if cardgame.ai_passed:
            return
        $ cardgame.current_actor = cardgame.enemy
        $ cardgame.other_actor = cardgame.player
    else:
        if cardgame.player_passed:
            return
        $ cardgame.current_actor = cardgame.player
        $ cardgame.other_actor = cardgame.enemy
    return