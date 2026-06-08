from manim import *

# Set the aspect ratio to 9:16 for TikTok/Shorts
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8.0

class SquareExpansion(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Configuration ---
        A_LEN = 3.0
        B_LEN = 1.5
        TOTAL_LEN = A_LEN + B_LEN

        COLOR_A = BLUE_D
        COLOR_B = GREEN_D
        COLOR_AB = YELLOW_D
        TEXT_COLOR = BLACK

        # --- 1. Introduction: The Line (a + b) ---
        title = Text("Bukti Geometris:", color=TEXT_COLOR).scale(1.2).to_edge(UP, buff=1.0)
        formula_title = MathTex("(a + b)^2 = a^2 + 2ab + b^2", color=TEXT_COLOR).scale(1.1).next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(Write(formula_title))
        self.wait(1)

        # Draw a starting line to define a and b
        line_start = ORIGIN + UP * 2.5 + LEFT * (TOTAL_LEN/2)
        line_a_start = Line(line_start, line_start + RIGHT * A_LEN, color=COLOR_A, stroke_width=8)
        line_b_start = Line(line_start + RIGHT * A_LEN, line_start + RIGHT * TOTAL_LEN, color=COLOR_B, stroke_width=8)
        
        lbl_a = MathTex("a", color=COLOR_A).next_to(line_a_start, UP)
        lbl_b = MathTex("b", color=COLOR_B).next_to(line_b_start, UP)

        self.play(Create(line_a_start), Write(lbl_a))
        self.play(Create(line_b_start), Write(lbl_b))
        self.wait(1)

        # --- 2. Transforming into the Square ---
        big_square = Square(side_length=TOTAL_LEN, stroke_color=BLACK, stroke_width=4).move_to(ORIGIN + DOWN * 0.5)
        
        self.play(
            FadeOut(line_a_start, line_b_start, lbl_a, lbl_b, title),
            formula_title.animate.to_edge(UP, buff=1.0),
            Create(big_square),
            run_time=1.5
        )

        # Adding labels a and b to the sides
        # Left side
        a_left = MathTex("a", color=TEXT_COLOR).scale(0.8).move_to(big_square.get_left() + UP * (TOTAL_LEN/2 - A_LEN/2) + LEFT * 0.4)
        b_left = MathTex("b", color=TEXT_COLOR).scale(0.8).move_to(big_square.get_left() + DOWN * (TOTAL_LEN/2 - B_LEN/2) + LEFT * 0.4)
        # Top side
        a_top = MathTex("a", color=TEXT_COLOR).scale(0.8).move_to(big_square.get_top() + LEFT * (TOTAL_LEN/2 - A_LEN/2) + UP * 0.4)
        b_top = MathTex("b", color=TEXT_COLOR).scale(0.8).move_to(big_square.get_top() + RIGHT * (TOTAL_LEN/2 - B_LEN/2) + UP * 0.4)

        self.play(Write(a_left), Write(b_left))
        self.play(Write(a_top), Write(b_top))

        # --- 3. Geometric Partition ---
        v_line = Line(big_square.get_top() + RIGHT * (A_LEN - TOTAL_LEN/2), 
                      big_square.get_bottom() + RIGHT * (A_LEN - TOTAL_LEN/2), color=BLACK)
        h_line = Line(big_square.get_left() + DOWN * (A_LEN - TOTAL_LEN/2), 
                      big_square.get_right() + DOWN * (A_LEN - TOTAL_LEN/2), color=BLACK)

        self.play(Create(v_line), Create(h_line))

        # --- 4. Filling the Areas ---
        square_a2 = Square(side_length=A_LEN, fill_opacity=0.8, fill_color=COLOR_A, stroke_color=BLACK)\
            .move_to(big_square.get_corner(UL), aligned_edge=UL)
        rect_ab1 = Rectangle(width=B_LEN, height=A_LEN, fill_opacity=0.8, fill_color=COLOR_AB, stroke_color=BLACK)\
            .move_to(big_square.get_corner(UR), aligned_edge=UR)
        rect_ab2 = Rectangle(width=A_LEN, height=B_LEN, fill_opacity=0.8, fill_color=COLOR_AB, stroke_color=BLACK)\
            .move_to(big_square.get_corner(DL), aligned_edge=DL)
        square_b2 = Square(side_length=B_LEN, fill_opacity=0.8, fill_color=COLOR_B, stroke_color=BLACK)\
            .move_to(big_square.get_corner(DR), aligned_edge=DR)

        lab_a2 = MathTex("a^2", color=WHITE).move_to(square_a2)
        lab_ab1 = MathTex("ab", color=WHITE).move_to(rect_ab1)
        lab_ab2 = MathTex("ab", color=WHITE).move_to(rect_ab2)
        lab_b2 = MathTex("b^2", color=WHITE).move_to(square_b2)

        self.play(FadeIn(square_a2), Write(lab_a2))
        self.play(FadeIn(rect_ab1), Write(lab_ab1))
        self.play(FadeIn(rect_ab2), Write(lab_ab2))
        self.play(FadeIn(square_b2), Write(lab_b2))
        self.wait(1)

        # --- 5. Conclusion Equation ---
        final_eq = MathTex(
            "(a+b)^2", "=", "a^2", "+", "2ab", "+", "b^2",
            color=TEXT_COLOR
        ).scale(1.1).to_edge(DOWN, buff=1.5)

        final_eq[2].set_color(COLOR_A)
        final_eq[4].set_color(COLOR_AB)
        final_eq[6].set_color(COLOR_B)

        self.play(Write(final_eq[0]), Write(final_eq[1]))
        self.play(TransformFromCopy(lab_a2, final_eq[2]))
        self.play(Write(final_eq[3]))
        self.play(TransformFromCopy(VGroup(lab_ab1, lab_ab2), final_eq[4]))
        self.play(Write(final_eq[5]))
        self.play(TransformFromCopy(lab_b2, final_eq[6]))

        box = SurroundingRectangle(final_eq, color=TEXT_COLOR, buff=0.2)
        self.play(Create(box))
        self.wait(3)