class KeyboardParams:
    def __init__(self):
        pass

    held_keys = {}
    pressed_keys = {}
    released_keys = {}


def begin_new_frame(dt):
    KeyboardParams.pressed_keys.clear()
    KeyboardParams.released_keys.clear()

    for key in list(KeyboardParams.held_keys.keys()):
        KeyboardParams.held_keys[key] += dt


def register_key_up(key):
    KeyboardParams.released_keys[key] = True
    if key in list(KeyboardParams.held_keys.keys()):
        del KeyboardParams.held_keys[key]


def register_key_down(key):
    KeyboardParams.pressed_keys[key] = True
    KeyboardParams.held_keys[key] = 0


def was_pressed(key):
    if key in list(KeyboardParams.pressed_keys.keys()):
        return True
    return False


def was_released(key):
    if key in list(KeyboardParams.released_keys.keys()):
        return True
    return False


def is_held(key):
    if key in list(KeyboardParams.held_keys.keys()):
        return True
    return False


def get_hold_time(key):
    if key in list(KeyboardParams.held_keys.keys()):
        return KeyboardParams.held_keys[key]
