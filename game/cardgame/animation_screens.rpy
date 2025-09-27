transform cardgame_player_play_action:
    pos (0.5, 1.0)
    anchor (0.5, 0)
    zoom 0.3
    easein 0.5 pos (0.5, 0.5) anchor (0.5, 0.5) zoom 1.0
    on hide:
        easeout 0.5 pos (int(1920/3), 0.5) zoom 0.1 alpha 0
transform cardgame_player_play_stance(x_pos):
    pos (0.5, 1.0)
    anchor (0.5, 0)
    zoom 0.3
    easein 0.5 pos (0.5, 0.5) anchor (0.5, 0.5) zoom 1.0
    on hide:
        easeout 0.5 pos (x_pos, 635) anchor(0, 0.5) zoom 0.3
transform cardgame_enemy_play_action:
    pos (0.5, 0.0)
    anchor (0.5, 1)
    zoom 0.3
    easein 0.5 pos (0.5, 0.5) anchor (0.5, 0.5) zoom 1.0
    on hide:
        easeout 0.5 pos (int(1920/3*2), 0.5) zoom 0.1 alpha 0
transform cardgame_enemy_play_stance(x_pos):
    pos (0.5, 0)
    anchor (0.5, 1.0)
    zoom 0.3
    easein 0.5 pos (0.5, 0.5) anchor (0.5, 0.5) zoom 1.0
    on hide:
        easeout 0.5 pos (x_pos, 445) anchor(1.0, 0.5) zoom 0.3
screen play_card(card, is_player, is_stance):
    modal True
    zorder 10

    button:
        xfill True
        yfill True
        action Return()
    timer (1 if is_player else 1.5) action Return()

    if is_player:
        if is_stance:
            $ stance_xpos = int(20 + len(cardgame.player.stances) * 130)
            add card.image at cardgame_player_play_stance(stance_xpos)
        else:
            add card.image at cardgame_player_play_action
    else:
        if is_stance:
            $ stance_xpos = int(1900 - len(cardgame.enemy.stances) * 130)
            add card.image at cardgame_enemy_play_stance(stance_xpos)
        else:
            add card.image at cardgame_enemy_play_action

image cardgame_new_round_frame = Frame("gui/cardgame/Frame1.png", 35, 26)
transform cardgame_new_round_transform:
    pos (0.5, 0) anchor (0.5, 1.0) alpha 0.0
    easein 0.5 pos (0.5, 0.33) anchor (0.5, 0.5) alpha 1.0
    on hide:
        easeout 0.5 pos (0.5, 0) anchor (0.5, 1.0)
screen cardgame_new_round(round_number):
    modal True
    zorder 5

    button:
        xfill True
        yfill True
        action Return()
    timer (1.5 if round_number > 1 else 2) action Return()

    frame:
        at truecenter, cardgame_new_round_transform
        padding (60, 30)
        background "cardgame_new_round_frame"
        text "Round [round_number]":
            size 140
            color "#000"
            xalign 0.5
            yalign 0.5


transform cardgame_vs_left():
    pos (0, 0.5)
    anchor (1.0, 0.5)
    easein 0.75 anchor (0, 0.5)
    on hide:
        easeout 0.5 anchor (1.0, 0.5)
transform cardgame_vs_right():
    pos (1.0, 0.5)
    anchor (0, 0.5)
    easein 0.75 anchor (1.0, 0.5)
    on hide:
        easeout 0.5 anchor (0, 0.5)
transform cardgame_vs_chibi_left():
    pos (0.333, 0)
    anchor (0.5, 1.0)
    easein 0.75 pos(0.25, 0.5) anchor (0.5, 0.75)
    on hide:
        easeout 0.5 pos(-0.5, 0.5) anchor (1.0, 0.5)
transform cardgame_vs_chibi_right():
    pos (0.666, 1.0)
    anchor (0.5, 0)
    easein 0.75 pos(0.75, 0.5) anchor (0.5, 0.25)
    on hide:
        easeout 0.5 pos(1.5, 0.5) anchor (0, 0.5)

screen cardgame_intro():
    modal True
    zorder 10

    button:
        xfill True
        yfill True
        action Hide()
    timer 1 action Hide()

    add "gui/cardgame/vs left.png" at cardgame_vs_left
    add "gui/cardgame/vs right.png" at cardgame_vs_right
    add "gui/cardgame/chibi base.png" at cardgame_vs_chibi_left:
        matrixcolor TintMatrix("#497f49")
    add "gui/cardgame/chibi base.png" at cardgame_vs_chibi_right:
        matrixcolor TintMatrix("#ecc5a1ff")

transform cardgame_player_draws_card(target_x):
    pos (1900, 1060)
    anchor (1.0, 1.0)
    zoom 0.3
    ease 0.5 zoom 0.3 knot 0.5 anchor (0.5, 1.0) pos (target_x, 1200) knot (target_x+300, 800) knot (1600, 800)

transform cardgame_enemy_draws_card(target_x):
    pos (20, 20)
    anchor (0, 0)
    zoom 0.3
    ease 0.5 zoom 0.3 knot 0.5 anchor (0.5, 0) pos (target_x, -100) knot (target_x-300, 280) knot (320, 280)

screen player_draws_card(card):
    default x = int(960 + (i - (len(cardgame.player.deck.hand) + 1)/ 2) * 120)
    zorder 7
    timer 0.5 action [Function(cardgame.player.deck.add_to_hand, card), Hide()]
    add card.image at cardgame_player_draws_card(x)

screen enemy_draws_card(card):
    default x = int(960 - (i - (len(cardgame.enemy.deck.hand) + 1) / 2) * 120)
    zorder 6
    text str(x)
    add "gui/cardgame/cardback elf.png" at cardgame_enemy_draws_card(x) #TODO: Actor based cardback
    timer 0.5 action [Function(cardgame.enemy.deck.add_to_hand, card), Hide()]