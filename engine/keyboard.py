class Keyboard:
    _held_keys = {}
    _pressed_keys = {}
    _released_keys = {}

    @staticmethod
    def begin_new_frame(dt):
        Keyboard._pressed_keys.clear()
        Keyboard._released_keys.clear()

        for key in Keyboard._held_keys.keys():
            Keyboard._held_keys[key] += dt

    @staticmethod
    def register_key_up(key):
        Keyboard._released_keys[key] = True
        if key in Keyboard._held_keys.keys():
            del Keyboard._held_keys[key]
    

    @staticmethod
    def register_key_down(key):
        Keyboard._pressed_keys[key] = True
        Keyboard._held_keys[key] = 0

    @staticmethod
    def was_pressed(key):
        if key in Keyboard._pressed_keys.keys():
            return True
        return False

    @staticmethod
    def was_released(key):
        if key in Keyboard._released_keys.keys():
            return True
        return False

    @staticmethod
    def is_held(key):
        if key in Keyboard._held_keys.keys():
            return True
        return False

    @staticmethod
    def get_hold_time(key):
        if key in Keyboard._held_keys.keys():
            return Keyboard._held_keys[key]

