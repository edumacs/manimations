from manim import *

# --- Vertical / TikTok Config ---
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8.0


class SquareContraction(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Parameters ---
        a = 4.5
        b = 1.5
        a_minus_b = a - b

        COL_A2 = BLUE_B
        COL_AMB2 = BLUE_E
        COL_B2 = GREEN_D
        COL_AB = RED_D
        TXT = BLACK

        # --------------------------------------------------
        # 1. Title & Initial Equation
        # --------------------------------------------------
        title = Text("Bukti Geometris", color=TXT, weight=BOLD)\
            .scale(1.3).to_edge(UP, buff=0.8)

        formula_top = MathTex(
            "(a-b)^2 = a^2 - 2ab + b^2",
            color=TXT
        ).scale(1.0).next_to(title, DOWN)

        self.play(Write(title), FadeIn(formula_top))
        self.wait(1)

        # --------------------------------------------------
        # 2. Big square a²
        # --------------------------------------------------
        big_square = Square(a, stroke_color=BLACK, stroke_width=4)\
            .shift(UP * 0.5)

        fill_a2 = Square(
            a, fill_color=COL_A2, fill_opacity=0.25, stroke_width=0
        ).move_to(big_square)

        label_a2 = MathTex("a^2", color=COL_A2)\
            .scale(1.6).move_to(big_square)

        side_a_top = MathTex("a", color=TXT).next_to(big_square, UP, buff=0.6)
        side_a_left = MathTex("a", color=TXT).next_to(big_square, LEFT, buff=0.6)

        self.play(Create(big_square))
        self.play(FadeIn(fill_a2), Write(label_a2))
        self.play(Write(side_a_top), Write(side_a_left))
        self.wait(1)

        # --------------------------------------------------
        # 3. Partition & Segment Labels
        # --------------------------------------------------
        v_cut = Line(
            big_square.get_top() + RIGHT * (a / 2 - b),
            big_square.get_bottom() + RIGHT * (a / 2 - b),
            color=BLACK
        )

        h_cut = Line(
            big_square.get_left() + DOWN * (a / 2 - b),
            big_square.get_right() + DOWN * (a / 2 - b),
            color=BLACK
        )

        self.play(Create(v_cut), Create(h_cut))

        label_amb_top = MathTex("a-b", color=TXT)\
            .scale(0.8).move_to(big_square.get_top() + LEFT * (b / 2) + UP * 0.3)
        label_b_top = MathTex("b", color=COL_B2)\
            .scale(0.8).move_to(big_square.get_top() + RIGHT * (a / 2 - b / 2) + UP * 0.3)

        label_amb_left = MathTex("a-b", color=TXT)\
            .scale(0.8).move_to(big_square.get_left() + UP * (b / 2) + LEFT * 0.4)
        label_b_left = MathTex("b", color=COL_B2)\
            .scale(0.8).move_to(big_square.get_left() + DOWN * (a / 2 - b / 2) + LEFT * 0.4)

        self.play(
            Write(label_amb_top), Write(label_b_top),
            Write(label_amb_left), Write(label_b_left),
            FadeOut(side_a_top), FadeOut(side_a_left)
        )
        self.wait(1)

        # --------------------------------------------------
        # 4. Double Subtraction (2ab)
        # --------------------------------------------------
        rect_ab_v = Rectangle(
            width=b, height=a,
            fill_color=COL_AB, fill_opacity=0.6, stroke_width=0
        ).move_to(big_square.get_corner(UR), aligned_edge=UR)

        rect_ab_h = Rectangle(
            width=a, height=b,
            fill_color=COL_AB, fill_opacity=0.6, stroke_width=0
        ).move_to(big_square.get_corner(DR), aligned_edge=DR)

        label_ab_v = MathTex("ab", color=WHITE).move_to(rect_ab_v)
        label_ab_h = MathTex("ab", color=WHITE).move_to(rect_ab_h)

        self.play(FadeOut(label_a2))
        self.play(FadeIn(rect_ab_v), Write(label_ab_v))
        self.wait(0.5)

        # Overlap b² (problem)
        overlap_b2 = Square(
            b, fill_color=DARK_BROWN, fill_opacity=0.85, stroke_width=0
        ).move_to(big_square.get_corner(DR), aligned_edge=DR)

        warning_txt = MathTex(
            r"b^2 \text{ terkurang dua kali}",
            color=RED
        ).scale(0.7).next_to(overlap_b2, DOWN, buff=0.25)

        self.play(FadeIn(rect_ab_h), Write(label_ab_h))
        self.play(FadeIn(overlap_b2), Write(warning_txt))
        self.play(Indicate(overlap_b2, color=RED, scale_factor=1.2))
        self.wait(1)

        # --------------------------------------------------
        # 5. Correction +b²
        # --------------------------------------------------
        correction_txt = MathTex(
            r"+\, b^2 \text{ (koreksi)}",
            color=COL_B2
        ).scale(0.7).move_to(warning_txt)

        actual_b2 = Square(
            b, fill_color=COL_B2, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=2
        ).move_to(overlap_b2)

        label_b2 = MathTex("b^2", color=WHITE).move_to(actual_b2)

        self.play(Transform(warning_txt, correction_txt))
        self.play(ReplacementTransform(overlap_b2, actual_b2), Write(label_b2))
        self.play(Flash(actual_b2, color=COL_B2))
        self.wait(1)

        # --------------------------------------------------
        # 6. (a-b)² Result Area
        # --------------------------------------------------
        square_amb2 = Square(
            a_minus_b, fill_color=COL_AMB2, fill_opacity=0.9
        ).move_to(big_square.get_corner(UL), aligned_edge=UL)

        label_amb2_final = MathTex("(a-b)^2", color=WHITE)\
            .scale(1.1).move_to(square_amb2)

        self.play(FadeOut(warning_txt))
        self.play(FadeIn(square_amb2), Write(label_amb2_final))
        self.wait(1)

        # --------------------------------------------------
        # 7. Final Equation
        # --------------------------------------------------
        result = MathTex(
            "(a-b)^2", "=", "a^2", "-", "2ab", "+", "b^2",
            color=TXT
        ).scale(1.15).to_edge(DOWN, buff=1.4)

        result[0].set_color(COL_AMB2)
        result[2].set_color(COL_A2)
        result[4].set_color(COL_AB)
        result[6].set_color(COL_B2)

        self.play(
            TransformFromCopy(label_amb2_final, result[0]),
            Write(result[1])
        )
        self.play(
            TransformFromCopy(fill_a2, result[2]),
            Write(result[3]),
            TransformFromCopy(VGroup(label_ab_v, label_ab_h), result[4])
        )
        self.play(
            Write(result[5]),
            TransformFromCopy(label_b2, result[6])
        )

        self.play(Create(SurroundingRectangle(result, color=COL_AMB2)))
        self.wait(3)
