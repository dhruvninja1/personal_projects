from manim import *

class thing(Scene):
    def construct(self):
        text = Text("Monkey")
        image = SVGMobject("icon.svg")
        self.play(Write(text))
        self.play(Rotate(text, angle=6, run_time=2), Transform(text, image), run_time=2)
        self.wait()
