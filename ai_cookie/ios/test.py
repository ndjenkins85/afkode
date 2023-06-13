# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

# https://forum.omz-software.com/topic/5277/speech-speech-activation/7
# https://gist.github.com/jsbain/b732076dc521c3c130a865924b6731d5


from math import floor

import sound
import ui


class RecorderView(ui.View):
    """simple metering view, attached to a recorder"""

    def __init__(self, filename, callback=None, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.r = sound.Recorder(filename)
        self.filename = filename
        self.callback = callback
        self.p = ui.Path()
        self.bg_color = "yellow"
        self.add_subview(ui.Label(frame=self.bounds, name="lbl"))
        self["lbl"].text = self.filename

    @ui.in_background
    def start(self):
        self["lbl"].text = self.filename + "(REC)"
        self.r.record()

    @ui.in_background
    def stop(self):
        self.r.stop()
        self["lbl"].text = self.filename
        self.p = ui.Path()
        # do something here... voice recog
        if callable(self.callback):
            self.callback(self.filename)

    def draw(self):
        y = self.r.meters["average"][0]
        self.p.line_to(self.r.current_time * 100, (-y))
        self.p.stroke()


H = 50


class MultiRecorder(ui.View):
    """start multiple, parallel recorders, iverlapping in time.
    record time will be at least T seconds, but maybe longer depending on processing.  do processing in a thread"""

    def __init__(self, Nrecorders=3, T=3):
        self.r = [
            RecorderView("test" + str(i) + ".m4a", callback=self.callback, frame=(0, H + i * H, 100 * T, 44))
            for i in range(Nrecorders)
        ]
        for r in self.r:
            self.add_subview(r)
        self.N = Nrecorders
        self.update_interval = 1 / 60
        self.idx = 0  # next recorder to stop
        self.cycle_frames = floor(T / self.update_interval / (Nrecorders - 1))
        self.t = 0  # next
        self.add_subview(ui.Label(frame=(0, 0, 400, H), name="status"))

    def will_close(self):
        [r.stop() for r in self.r]

    def callback(self, filename):
        """override to do speech processing"""
        self["status"].text = "[processing]" + filename

    def update(self):
        if self.t % self.cycle_frames == 0:
            self.r[self.idx - 1].start()
            self.r[self.idx].stop()
            # do something with 'test'+str(i)+'.wav'
            self.idx = (self.idx + 1) % self.N
        for r in self.r:
            r.set_needs_display()

        self.t += 1


v = MultiRecorder()
v.frame = (0, 0, 500, 400)
v.bg_color = "white"
v.present("sheet")
