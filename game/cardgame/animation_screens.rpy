transform player_play_action:
    pos (0.5, 1.0)
    anchor (0.5, 0)
    zoom 0.3
    easein 0.5 pos (0.5, 0.5) anchor (0.5, 0.5) zoom 1.0
    on hide:
        easeout 0.5 pos (int(1920/3), 0.5) zoom 0.1 alpha 0

transform player_play_stance(x_pos):
    pos (0.5, 1.0)
    anchor (0.5, 0)
    zoom 0.3
    easein 0.5 pos (0.5, 0.5) anchor (0.5, 0.5) zoom 1.0
    on hide:
        easeout 0.5 pos (x_pos, 635) anchor(0, 0.5) zoom 0.3

transform enemy_play_action:
    pos (0.5, 0.0)
    anchor (0.5, 1)
    zoom 0.3
    easein 0.5 pos (0.5, 0.5) anchor (0.5, 0.5) zoom 1.0
    on hide:
        easeout 0.5 pos (int(1920/3*2), 0.5) zoom 0.1 alpha 0

transform enemy_play_stance(x_pos):
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

    if is_player:
        if is_stance:
            $ stance_xpos = int(20 + len(cardgame.player.stances) * 130)
            add card.image at player_play_stance(stance_xpos)
        else:
            add card.image at player_play_action
    else:
        if is_stance:
            $ stance_xpos = int(1900 - len(cardgame.enemy.stances) * 130)
            add card.image at enemy_play_stance(stance_xpos)
        else:
            add card.image at enemy_play_action

    timer (1 if is_player else 1.5) action Return()