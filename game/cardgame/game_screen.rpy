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

transform cardgame_card_size(z):
    zoom z
transform cardgame_tooltip(x1, x2, y1, y2, z1, z2, time=0.25):
    xpos x1 ypos y1 zoom z1
    ease time xpos x2 ypos y2 zoom z2
transform cardgame_rotate_card:
    rotate 180

transform cardgame_player_chibi:
    xpos int(1920 / 3)
    ypos 540
    xanchor 0.5
    yanchor 0.5
transform cardgame_enemy_chibi:
    xpos int(1920 * 2 / 3)
    ypos 540
    xanchor 0.5
    yanchor 0.5
transform cardgame_crop_armor(armor, max_armor):
    crop (0.0, 1.0 - armor / max_armor, 1.0, 1.0)
    


screen cardgame_intro():
    modal True
    zorder 10
    add "gui/cardgame/vs left.png" at cardgame_vs_left
    add "gui/cardgame/vs right.png" at cardgame_vs_right
    add "gui/cardgame/chibi base.png" at cardgame_vs_chibi_left:
        matrixcolor TintMatrix("#497f49")
    add "gui/cardgame/chibi base.png" at cardgame_vs_chibi_right:
        matrixcolor TintMatrix("#ecc5a1ff")
    timer 1.25 action Hide()

screen cardgame_screen(eval_label):

    default tooltip = None

    modal True
    add "gui/cardgame/battlefield.png":
        xsize 1.0
        ysize 1.0

    # Player hand
    for i, card in enumerate(cardgame.player.deck.hand):
        python:
            x1 = int(960 + (i - (len(cardgame.player.deck.hand) - 1) / 2) * 120) # Centered horizontally
            x2 = x1
            y1 = 1200
            y2 = 1070
            z1 = 0.3
            z2 = 0.5
            xanchor = 0.5
            yanchor = 1.0
        imagebutton at cardgame_card_size(z1):
            idle card.image
            hover card.image
            action (
                [SetVariable("cardgame.player_selected_card", (card, i)), Jump(eval_label)]
                if cardgame.current_actor == cardgame.player and not cardgame.player_passed
                else NullAction())
            xpos x1
            ypos y1
            xanchor 0.5
            yanchor 1.0
            tooltip (card.image, x1, x2, y1, y2, z1, z2, xanchor, yanchor)

    # Player Wincondition
    if cardgame.player.deck.wincon:
        imagebutton at cardgame_card_size(z1):
            idle cardgame.player.deck.wincon.image
            hover cardgame.player.deck.wincon.image
            action NullAction()
            xpos 20
            ypos 1060
            xanchor 0
            yanchor 1.0
            tooltip (cardgame.player.deck.wincon.image, 20, 10, 1060, 1070, 0.3, 0.5, 0, 1.0)

    # Player Stances
    for i, card in enumerate(cardgame.player.stances):
        $ x = int(20 + i * 130)
        imagebutton at cardgame_card_size(0.3):
            idle card.image
            hover card.image
            action NullAction()
            xpos x
            ypos 635
            xanchor 0.0
            yanchor 0.5
            tooltip (card.image, x, x-10, 635, 635, 0.3, 0.5, 0.0, 0.5)

    # Player Deck
    for i in range(len(cardgame.player.deck.cards)):
        $ x = int(1900 - i * 3)
        $ y = int(1060 - i * 1)
        add "gui/cardgame/cardback goblin.png":
            xpos x
            ypos y
            xanchor 1.0
            yanchor 1.0
            zoom 0.3
    
    # Pass Button
    if cardgame.current_actor == cardgame.player and not cardgame.player_passed:
        textbutton "Pass":
            action (
                [SetVariable("cardgame.player_selected_card", None), Jump(eval_label)]
            )
            xpos 1900
            ypos 700
            xanchor 1.0
            yanchor 1.0

    # Enemy hand
    for i, card in enumerate(cardgame.enemy.deck.hand):
        $ x = int(960 + (i - (len(cardgame.enemy.deck.hand) - 1) / 2) * 120)
        $ card = card
        imagebutton at cardgame_card_size(0.3), cardgame_rotate_card:
            idle "gui/cardgame/cardback elf.png" # TODO: Actor based cardback
            hover "gui/cardgame/cardback elf.png"
            action NullAction()
            xpos x
            ypos -100
            xanchor 0.5
            yanchor 0.0

    # Enemy Wincondition
    if cardgame.enemy.deck.wincon:
        imagebutton at cardgame_card_size(0.3):
            idle cardgame.enemy.deck.wincon.image
            hover cardgame.enemy.deck.wincon.image
            action NullAction()
            xpos 1900
            ypos 20
            xanchor 1.0
            yanchor 0.0
            tooltip (cardgame.enemy.deck.wincon.image, 1900, 1910, 20, 10, 0.3, 0.5, 1.0, 0.0)

    # Enemy Stances
    for i, card in enumerate(cardgame.enemy.stances):
        $ x = int(1900 - i * 130) 
        imagebutton at cardgame_card_size(0.3):
            idle card.image
            hover card.image
            action NullAction()
            xpos x
            ypos 445
            yanchor 0.5
            xanchor 1.0
            tooltip (card.image, x, x+10, 445, 445, 0.3, 0.5, 1.0, 0.5)

    # Enemy Deck
    for i in range(len(cardgame.enemy.deck.cards)):
        $ x = int(110 + i * 3)
        $ y = int(155 + i * 1)
        add "gui/cardgame/cardback elf.png" at cardgame_rotate_card:
            xpos x
            ypos y
            xanchor 0.5
            yanchor 0.5
            zoom 0.3

    # Player Chibi
    add "gui/cardgame/chibi base.png" at cardgame_player_chibi:
        matrixcolor TintMatrix("#497f49")
    bar at cardgame_player_chibi:
        yoffset -250
        xoffset -10
        value cardgame.player.stats.health
        range cardgame.player.stats.max_health
        xsize 200
        ysize 20
    text "[cardgame.player.stats.health]/[cardgame.player.stats.max_health]":
        at cardgame_player_chibi
        yoffset -250
        size 18
    add "gui/cardgame/armor empty.png":
        at cardgame_player_chibi
        yoffset -250
        xoffset 90
        xsize 40
        ysize 40
    add "gui/cardgame/armor full.png":
        at cardgame_player_chibi, cardgame_crop_armor(cardgame.player.stats.armor, cardgame.player.stats.max_armor)
        yoffset -250
        xoffset 90
        xsize 40
        ysize 40
    text "[cardgame.player.stats.armor]/[cardgame.player.stats.max_armor]" at cardgame_player_chibi:
        yoffset -250
        xoffset 90
        size 18

    # Opponent Chibi
    add "gui/cardgame/chibi base.png" at cardgame_enemy_chibi:
        matrixcolor TintMatrix("#ecc5a1")
    bar at cardgame_enemy_chibi:
        yoffset -250
        xoffset -10
        value cardgame.enemy.stats.health
        range cardgame.enemy.stats.max_health
        xsize 200
        ysize 20
    text "[cardgame.enemy.stats.health]/[cardgame.enemy.stats.max_health]":
        at cardgame_enemy_chibi
        yoffset -250
        size 18
    add "gui/cardgame/armor empty.png":
        at cardgame_enemy_chibi
        yoffset -250
        xoffset 90
        xsize 40
        ysize 40
    add "gui/cardgame/armor full.png":
        at cardgame_enemy_chibi, cardgame_crop_armor(cardgame.enemy.stats.armor, cardgame.enemy.stats.max_armor)
        yoffset -250
        xoffset 90
        xsize 40
        ysize 40
    text "[cardgame.enemy.stats.armor]/[cardgame.enemy.stats.max_armor]":
        at cardgame_enemy_chibi
        yoffset -250
        xoffset 90
        size 18

    # Handle hover tooltip
    $ tmptip = GetTooltip() # (0: image, 1: x1, 2: x2, 3: y1, 4: y2, 5: z1, 6: z2, 7: xanchor, 8: yanchor)
    if tooltip: # If there is an old tooltip, play the hide animation 
        add tooltip[0] at cardgame_tooltip(tooltip[2], tooltip[1], tooltip[4], tooltip[3], tooltip[6], tooltip[5], 0.15):
            xanchor tooltip[7]
            yanchor tooltip[8]
    if tmptip:
        $ tooltip = tmptip
        add tooltip[0] at cardgame_tooltip(tooltip[1], tooltip[2], tooltip[3], tooltip[4], tooltip[5], tooltip[6]):
            xanchor tooltip[7]
            yanchor tooltip[8]
    else:
        $ tooltip = None

    use cardgame_debug
    use cardgame_eventlog

screen cardgame_eventlog():
    vbox:
        xpos 1900
        ypos 20
        xanchor 1.0
        yanchor 0.0
        spacing 5
        text "Event Log"
        for event in cardgame.game_events[-5:]:
            if isinstance(event, str):
                text event
            else: # is card
                text event.name

screen cardgame_debug():
    vbox:
        xpos 10
        ypos 10
        spacing 5
        text "Debug Info"
        text "Round: [cardgame.round]"
        text "Current Actor: [cardgame.current_actor.name if cardgame.current_actor else 'None']"
        text "Other Actor: [cardgame.other_actor.name if cardgame.other_actor else 'None']"
        text "Player Hand Size: [cardgame.player.deck.hand_size]"
        text "Enemy Hand Size: [cardgame.enemy.deck.hand_size]"
        text "Player Deck Size: [cardgame.player.deck.deck_size]"
        text "Enemy Deck Size: [cardgame.enemy.deck.deck_size]"
        text "Player Discard Size: [cardgame.player.deck.discard_size]"
        text "Enemy Discard Size: [cardgame.enemy.deck.discard_size]"
        text "Player Selected Card: [cardgame.player_selected_card[0].name if cardgame.player_selected_card else 'None'] (at index [cardgame.player_selected_card[1] if cardgame.player_selected_card else 'None'])"
        text "AI Selected Card: [cardgame.ai_selected_card.name if cardgame.ai_selected_card else 'None']"
        text "Player Passed: [cardgame.player_passed]"
        text "AI Passed: [cardgame.ai_passed]"