from manim import *
import Libraries.LEB as LEB

class Main(Scene):
    def construct(self):

        m0 = Matrix([
            [1, 0, 0],
            [0.5, 0, 0.5],
            [0, 1, 0]
        ], element_alignment_corner=[0,0,0])

        m1 = Matrix([
            [0, 1, 0],
            [0.5, 0, 0.5],
            [0, 0, 1],
        ], element_alignment_corner=[0,0,0])
       
        mb = Matrix([
            ['1-b', 'b', 0],
            [0.5, 0, 0.5],
            [0, '1-b', 'b']
        ], element_alignment_corner=[0,0,0])

        top_group = VGroup(m0, m1).arrange_in_grid()
        group = VGroup(top_group, mb).arrange(DOWN)
        m0_t = MathTex('m_0').next_to(m0, direction=UP)
        m1_t = MathTex('m_1').next_to(m1, direction=UP)

        rects0 = [
            SurroundingRectangle(m0.get_rows()[0][1], color=GREEN),
            SurroundingRectangle(m1.get_rows()[0][1], color=GREEN),
            SurroundingRectangle(m1.get_rows()[2][2], color=GREEN),
            SurroundingRectangle(m0.get_rows()[2][2], color=GREEN)
        ]

        rects1 = [
            SurroundingRectangle(m0.get_rows()[0][0], color=RED),
            SurroundingRectangle(m0.get_rows()[2][1], color=RED),
            SurroundingRectangle(m1.get_rows()[0][0], color=RED),
            SurroundingRectangle(m1.get_rows()[2][1], color=RED)
        ]

        self.add(top_group, m0_t, m1_t)

        self.wait(8)

        self.play(*[Create(r) for r in rects0])
        self.wait(2)
        self.play(*[Create(r) for r in rects1])
        self.wait(2)

        self.play(Create(mb))

        self.wait(2)

        self.play(
            mb[0][0].animate.set_color(RED),
            mb[0][1].animate.set_color(GREEN),
            mb[0][7].animate.set_color(RED),
            mb[0][8].animate.set_color(GREEN)
        )

        self.wait(3)