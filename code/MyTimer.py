from pyray import get_time

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
