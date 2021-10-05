from manim import *
import numpy as np

class Normal(Scene):
    def construct(self):
        t1 = Text("Update\nIndirect Args").scale(0.6)
        b1 = SurroundingRectangle(t1, color=WHITE)
        g1 = VGroup(t1,  b1)

        t2 = Text("Indirect Draw").scale(0.6)
        b2 = SurroundingRectangle(t2, color=WHITE)
        g2 = VGroup(t2, b2)

        t3 = Text("Sum Reduction").scale(0.6)
        b3 = SurroundingRectangle(t3, color=WHITE)
        g3 = VGroup(t3, b3)

        t4 = Text("Subdivision").scale(0.6)
        b4 = SurroundingRectangle(t4, color=WHITE)
        g4 = VGroup(t4, b4)

        g_main1 = VGroup(g1, g2, g3, g4).arrange(RIGHT, buff=0.7)
        a1 = Arrow(b1.get_right(), b2.get_left(), buff=0)
        a2 = Arrow(b2.get_right(), b3.get_left(), buff=0)
        a3 = Arrow(b3.get_right(), b4.get_left(), buff=0)
        a4 = VGroup(*[
            Line(b4.get_top(), b4.get_top() + UP),
            Line(b4.get_top() + UP, b1.get_top() + UP),
            Arrow(b1.get_top() + UP, b1.get_top(), buff=0)
        ])
        self.play(Create(g1))
        self.wait(1)
        self.play(Create(g2), Create(a1))
        self.wait(1)
        self.play(Create(g3), Create(a2))
        self.wait(1)
        self.play(Create(g4), Create(a3))
        self.wait(1)
        self.play(Create(a4))
        self.wait(3)

class MeshShader(Scene):
    def construct(self):
        t1 = Text("Update\nIndirect Args").scale(0.6)
        b1 = SurroundingRectangle(t1, color=WHITE)
        g1 = VGroup(t1,  b1)

        t2 = Text("Sum Reduction").scale(0.6)
        b2 = SurroundingRectangle(t2, color=WHITE)
        g2 = VGroup(t2, b2)

        t4 = Text("Indirect Dispatch Mesh").scale(0.6)
        b4 = SurroundingRectangle(t4, color=WHITE)
        g4 = VGroup(t4, b4)

        g_main1 = VGroup(g1, g2, g4).arrange(RIGHT, buff=0.7)
        a1 = Arrow(b1.get_right(), b2.get_left(), buff=0)
        a3 = Arrow(b2.get_right(), b4.get_left(), buff=0)
        a4 = VGroup(*[
            Line(b4.get_top(), b4.get_top() + UP),
            Line(b4.get_top() + UP, b1.get_top() + UP),
            Arrow(b1.get_top() + UP, b1.get_top(), buff=0)
        ])
        self.play(Create(g1))
        self.wait(0.5)
        self.play(Create(g2), Create(a1))
        self.wait(0.5)
        self.play(Create(g4), Create(a3))
        self.wait(0.5)
        self.play(Create(a4))
        self.wait(1)

