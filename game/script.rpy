define crow = Character("Professor Crow")
default poked_eye_count = 0
default seen_lost_soul_choice = False
default player = "Stranger"

init python:
    import math
    import string
    import datetime

    def pupil_follow_transform(trans, st, at):
        mouse = renpy.get_mouse_pos()
        sub = (mouse[0]-trans.pos[0], mouse[1]-trans.pos[1])
        mag = math.sqrt(sub[0]*sub[0]+sub[1]*sub[1])
        norm = (sub[0]/mag, sub[1]/mag)
        trans.offset = (norm[0]*18, norm[1]*18)
        return 0

image white = "#fff"
image black = "#000"

image exclamation:
    "exclamation_0"
    pause 0.5
    "exclamation_1"
    pause 0.5
    "exclamation_0"
    pause 0.5
    "exclamation_2"
    pause 0.5
    repeat

layeredimage crow:
    always "bird"
    group pupil:
        anchor (0.5, 0.5)
        pos (755, 180)
        attribute look_straight default:
            "pupil"
            offset (0, 0)

        attribute look_right:
            "pupil"
            offset (15, 0)

        attribute look_left:
            "pupil"
            offset (-15, 0)

        attribute look_up:
            "pupil"
            offset (0, -15)

        attribute look_down:
            "pupil"
            offset (0, 15)

        attribute look_down_right:
            "pupil"
            offset (12, 12)

        attribute look_down_left:
            "pupil"
            offset (-12, 12)

        attribute look_up_right:
            "pupil"
            offset (12, -12)

        attribute look_up_left:
            "pupil"
            offset (-12, -12)

    group lid:
        pos (755, 180)
        anchor (0.5, 0.5)
        attribute open default:
            Null()
        attribute top_closed:
            "top_lid"
        attribute bottom_closed:
            "bottom_lid"
        attribute squint:
            "squint"

    attribute exclamation:
        pos (550, 25)
        "exclamation"


transform pupil():
    pos (755, 180)
    anchor (0.5, 0.5)
    offset(0, 0)

transform pupil_follow():
    pos (755, 180)
    anchor (0.5, 0.5)
    function pupil_follow_transform

label start:
    show white
    show crow
    if persistent.pissed_off_crow:
        jump go_away
    elif persistent.name:
        jump hello_again
    else:
        jump meet_crow

label meet_crow:
    crow "Oh. Hey there."
    crow "Uhh, who are you?"
    call choose_name("Uhh, who are you?")
    show crow look_down top_closed
    crow "Anyhow..."
    jump listen_to_crows_problem

label hello_again:
    $ player = persistent.name
    show crow top_closed look_down
    crow "Oh...it's you...what was your name again?"
    show crow open exclamation
    crow "Wait! I remember...I think...oh right!"
    show crow open look_straight -exclamation
    jump listen_to_crows_problem

label go_away:
    show crow top_closed exclamation
    crow "{i}YOU{/i}!"
    show crow bottom_closed -exclamation
    if not persistent.last_seen or persistent.last_seen < datetime.date.today():
        # It's been a day since we've seen crow.
        crow "You have some nerve showing yourself here, {i}[persistent.nam]{/i}..."
    else:
        # We've visiting multiple times in one day.
        crow "You're really going to show up here, {i}yet again{/i}?"
        crow "You were just here a moment ago. And you are {i}still{/i} not welcome here."
    $ persistent.last_seen = datetime.date.today()
    crow "Beat it before I make wormmeal out of you!"
    jump angry_squaking

label listen_to_crows_problem:
    show crow look_straight open
    crow "Hello, {i}[player]{/i}"
    show crow look_down_left
    crow "Don't mind me."
    show crow look_left
    crow "I've been looking for something...."
    show crow look_up_left
    crow "...a worm."
    show crow look_up
    crow "But not just any 'ole worm."
    show crow look_up_right
    crow "A {i}magical{/i} worm."
    show crow look_up_right bottom_closed
    crow "A {b}{i}specific{/i}{/b},{i}magical{/i} worm."
    show crow look_right open
    crow "Been looking for ages..."
    show crow squint look_right
    crow "But they're a pesky one to find."
    show crow look_right open exclamation:
        linear 0.15 yoffset -50
        linear 0.25 yoffset 0
    crow "Oh, actually...!"
    show crow look_straight open -exclamation
    crow "Can you help me find them, friend?"
    jump bird_watch

label bird_watch:
    call screen bird_watch
    jump bird_watch

label poked_eye:
    if poked_eye_count < 2:
        show crow squint look_straight exclamation:
            linear 0.15 yoffset -50
            linear 0.25 yoffset 0
        crow "GAH!"
    else:
        show crow squint look_straight exclamation:
            linear 0.15 yoffset -50
            linear 0.25 yoffset 0
            block:
                linear 0.25 yoffset -50
                linear 0.25 yoffset 0
                repeat
        with vpunch
        crow "SQUAAAK!!!"
    if poked_eye_count == 0:
        show crow open -exclamation
        crow "Excuse me!"
        crow "That is no worm, that is my eye!"
        show crow top_closed
        crow "Please do not touch my eye again."
    elif poked_eye_count == 1:
        show crow open -exclamation
        crow "{b}*AHEM*{/b} You did it again. You poked my eye."
        show crow top_closed
        crow "Please stop, we are looking for a {b}worm{/b} not an {b}eye{/b}."
    elif poked_eye_count == 2:
        show crow top_closed -exclamation
        crow "HEY watch it!"
        show crow bottom_closed
        crow "Worms don't even have eyes! How are you making this mistake over and over?"
        show crow bottom_closed:
            yoffset 0
        crow "Do we have a problem? {i}[player]{/i}?"
        crow "I sense we do."
        show crow squint
        crow "You best leave and not come back!"
        $ persistent.pissed_off_crow = True
        jump angry_squaking
    show crow open
    $ poked_eye_count += 1
    return

label angry_squaking:
    show crow squint look_straight exclamation:
        linear 0.15 yoffset -50
        linear 0.25 yoffset 0
        block:
            linear 0.25 yoffset -50
            linear 0.25 yoffset 0
            repeat
    with vpunch
    crow "SQUAAAK!!!"
    jump end_game

    return

label choose_name(prompt):
    menu:
        crow "[prompt]"
        "A wizard.":
            $ player = "Wizard"
            crow "Huh, really, a wizard?"
        "A friend.":
            $ player = "Friend"
            crow "Oh, that's nice, friends are nice!"
        "A lost soul." if not seen_lost_soul_choice:
            $ seen_lost_soul_choice = True
            show crow top_closed
            crow "Uhh, that's weird, I'm not going to call you that..."
            show crow open
            crow "Who are you really?"
            call choose_name("Who are you really?")
        "I am...(name yourself)":
            call enter_name(prompt)
    $ persistent.name = player
    return

label enter_name(prompt):
    $ potential_name = renpy.input(prompt,
                                   allow=string.ascii_lowercase+string.ascii_uppercase+" -",
                                   length=15,
                                   default=player)
    $ potential_name = potential_name.strip().title()
    if not potential_name:
        show crow open
        crow "..."
        crow "Were you going to say something?"
        crow "What should I call you?"
        call enter_name("What should I call you?")
    elif potential_name == "Professor Crow":
        show crow squint
        crow "Very funny. Did my adjunt send you to play a prank on me?"
        crow "Tell me your real name."
        call enter_name("Tell me your real name.")
    else:
        $ player = potential_name
        if potential_name == "Sabrina":
            crow "Oh, you must know my associate, Salem."
        elif potential_name == "Peanut":
            show crow open exclamation:
                linear 0.15 yoffset -50
                linear 0.25 yoffset 0
            with vpunch
            crow "Did you say {i}{b}peanut{/b}{/i}?!"
            show crow open -exclamation
            crow "Oh, I just {b}LOVE{/b} peanuts!"
            show crow bottom_closed look_up:
                linear 0.25 yoffset -50
                linear 0.25 yoffset 0
                repeat
            crow "They get me so excited!"
            show crow bottom_closed look_straight exclamation:
                yoffset 0
            pause 1.5
            show crow open look_straight -exclamation
            crow "*ahem*"
        else:
            crow "Really?"
            crow "That's a weird name."
    return

label end_game:
    scene black with Dissolve(2.5)
    pause 3.0
    $ renpy.full_restart()
    return

transform eye:
    pos (755, 180)
    anchor (0.5, 0.5)

screen bird_watch(interactable=True):
    default pupil_transform = pupil
    add "white"
    add "bird"
    imagebutton:
        at eye
        idle "eye"
        if interactable:
            action NullAction()
        hovered Call("poked_eye")
        focus_mask True
    add "pupil" at pupil_transform
    mousearea area (107, 60, 1066, 600):
        if interactable:
            hovered SetScreenVariable("pupil_transform", pupil_follow)
            unhovered SetScreenVariable("pupil_transform", pupil)
