class MouseParams:
    def __init__(self):
        pass

    held_buttons = [-1, -1, -1]
    pressed_buttons = [False, False, False]
    released_buttons = [False, False, False]


def begin_new_frame(dt):
    MouseParams.pressed_buttons = [False, False, False]
    MouseParams.released_buttons = [False, False, False]

    for k in range(3):
        if MouseParams.held_buttons != -1:
            MouseParams.held_buttons += dt


def register_mouse_release(button):
    MouseParams.released_buttons[button] = True
    MouseParams.held_buttons[button] = -1


def register_mouse_press(button):
    MouseParams.pressed_buttons[button] = True
    MouseParams.held_buttons[button] = 0


def was_pressed(button):
    return MouseParams.pressed_buttons[button]


def was_released(button):
    return MouseParams.released_buttons[button]


def is_held(button):
    if MouseParams.held_buttons[button] != 0:
        return True
    return False
