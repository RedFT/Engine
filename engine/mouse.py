class Mouse:
    LEFT=0
    MIDDLE=1
    RIGHT=2

    _held_buttons = [-1, -1, -1]
    _pressed_buttons = [False, False, False]
    _released_buttons = [False, False, False]

    @staticmethod
    def begin_new_frame(dt):
        Mouse._pressed_buttons = [False, False, False]
        Mouse._released_buttons = [False, False, False]

        for k in range(3):
            if Mouse._held_buttons != -1:
                Mouse._held_buttons += dt

    @staticmethod
    def register_mouse_release(button):
        Mouse._released_buttons[button]=True
        Mouse._held_buttons[button] = -1


    @staticmethod
    def register_mouse_press(button):
        Mouse._pressed_buttons[button] = True
        Mouse._held_buttons[button] = 0

    @staticmethod
    def was_pressed(button):
        return Mouse._pressed_buttons[button]

    @staticmethod
    def was_released(button):
        return Mouse._released_buttons[button]

    @staticmethod
    def is_held(button):
        if Mouse._held_buttons[button] != 0:
            return True
        return False
