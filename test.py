from manim import *

class Test(Scene):
    def construct(self):
        eq = MathTex(r"\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}")
        self.play(Write(eq))
        self.wait()
