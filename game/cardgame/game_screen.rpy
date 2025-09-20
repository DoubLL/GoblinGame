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
transform card_size(z):
    zoom z
transform cardgame_tooltip(x1, x2, y1, y2, z1, z2, time=0.25):
    xpos x1 ypos y1 zoom z1
    ease time xpos x2 ypos y2 zoom z2

screen cardgame_intro():
    modal True
    zorder 10
    add "gui/cardgame/vs left.png" at cardgame_vs_left
    add "gui/cardgame/vs right.png" at cardgame_vs_right
    add "gui/cardgame/chibi base.png" at cardgame_vs_chibi_left
    add "gui/cardgame/chibi base.png" at cardgame_vs_chibi_right
    timer 1.25 action Hide()

screen cardgame_screen(eval_label):

    default tooltip = None

    modal True
    add "gui/cardgame/battlefield.png":
        xsize 1.0
        ysize 1.0
    button:
        xfill True
        yfill True
        action Jump(eval_label)

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
        imagebutton at card_size(z1):
            idle card.image
            hover card.image
            action [SetVariable("cardgame.player_selected_card", card), Jump(eval_label)]
            xpos x1
            ypos y1
            xanchor 0.5
            yanchor 1.0
            tooltip (card.image, x1, x2, y1, y2, z1, z2, xanchor, yanchor)


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