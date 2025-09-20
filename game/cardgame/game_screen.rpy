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
    add "gui/cardgame/vs left.png" at cardgame_vs_left
    add "gui/cardgame/vs right.png" at cardgame_vs_right
    add "gui/cardgame/chibi base.png" at cardgame_vs_chibi_left
    add "gui/cardgame/chibi base.png" at cardgame_vs_chibi_right
    timer 1.25 action Hide()

screen cardgame_screen(eval_label):
    modal True
    add "gui/cardgame/battlefield.png":
        xsize 1.0
        ysize 1.0
    button:
        xfill True
        yfill True
        action Jump(eval_label)