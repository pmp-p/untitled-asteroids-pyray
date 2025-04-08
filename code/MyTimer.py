from Settings import get_time
from pyray import *
from raylib import *


class Timer:
    def __init__(self, duration: int, repeat=False, autostart=False, func=None):
        # set the timer duration, repeat flag, autostart flag, and function to call when timer ends
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.repeat = repeat
        self.func = func

        # if autostart is True, start the timer automatically when the Timer object is created
        if autostart:
            self.activate()

    def activate(self):
        self.active = True
        self.start_time = get_time()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        if self.active:
            elapsed_time = get_time() - self.start_time
            if elapsed_time >= self.duration:
                if self.func and self.start_time:
                    self.func()
                self.deactivate()
            # print(elapsed_time)


# testing
if __name__ == "__main__":
    init_window(1920, 1080, "Timer")
    test_timer = Timer(5, False, False)
    test_timer.activate()
    while not window_should_close():
        test_timer.update()
        begin_drawing()
        clear_background(BLACK)
        end_drawing()
    close_window()
