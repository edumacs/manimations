from manim import *
import numpy as np

# =====================
# 9:16 VERTICAL VIDEO CONFIG
# =====================
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8.0

class VectorElaboration(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # PARAMETERS
        a_len, b_len = 2.5, 2.0
        COL_A, COL_B, COL_R = BLUE_D, GREEN_D, RED_E
        COL_EXT, TXT = GREY_B, BLACK
        
        origin = LEFT * 1.0 + DOWN * 2.0
        theta_val = 40 * DEGREES

        # 1. TITLE & INITIAL FORMULA
        title = Text("Menurunkan Rumus\nResultan Vektor", color=TXT, weight=BOLD, line_spacing=0.9).scale(0.8)
        title.to_edge(UP, buff=1.0)
        
        initial_logic = MathTex(
            r"R^2 = (\text{alas})^2 + (\text{tinggi})^2",
            tex_to_color_map={r"\text{alas}": COL_A, r"\text{tinggi}": COL_B},
            color=TXT
        ).scale(0.8).next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(initial_logic))
        self.wait(1)

        # 2. DRAW VECTORS (START AT ORIGIN)
        vec_a = Arrow(origin, origin + RIGHT * a_len, buff=0, color=COL_A, stroke_width=8)
        label_a = MathTex("a", color=COL_A).scale(0.8).next_to(vec_a, DOWN, buff=0.2)

        vec_b = Arrow(origin, origin + rotate_vector(RIGHT * b_len, theta_val), buff=0, color=COL_B, stroke_width=8)
        label_b = MathTex("b", color=COL_B).scale(0.8).next_to(vec_b.get_center(), UP+LEFT, buff=0.1)

        # Angle theta
        arc = Arc(radius=0.6, start_angle=0, angle=theta_val, arc_center=origin, color=TXT)
        lbl_theta = MathTex(r"\theta", color=TXT).scale(0.7).move_to(origin + 0.8 * np.array([np.cos(theta_val/2), np.sin(theta_val/2), 0]))

        self.play(GrowArrow(vec_a), FadeIn(label_a))
        self.play(GrowArrow(vec_b), FadeIn(label_b), Create(arc), FadeIn(lbl_theta))
        self.wait(1)

        # 3. TRANSLATE VEC B TO TIP OF A (Head-to-Tail)
        # We move b to the end of a to form the right triangle
        new_b_pos = vec_a.get_end()
        self.play(
            vec_b.animate.shift(vec_a.get_end() - origin),
            label_b.animate.shift(vec_a.get_end() - origin),
            FadeOut(arc), FadeOut(lbl_theta),
            run_time=1.5
        )

        # 4. SHOW COMPONENTS (The "Secret" Right Triangle)
        # Projection lines starting from end of a
        dashed_h = DashedLine(vec_a.get_end(), vec_a.get_end() + RIGHT * (b_len * np.cos(theta_val)), color=COL_EXT)
        dashed_v = DashedLine(dashed_h.get_end(), vec_b.get_end(), color=COL_EXT)
        
        # New angle at the junction
        arc_new = Arc(radius=0.5, start_angle=0, angle=theta_val, arc_center=vec_a.get_end(), color=TXT)
        lbl_theta_new = MathTex(r"\theta", color=TXT).scale(0.6).move_to(
            vec_a.get_end() + 0.7 * np.array([np.cos(theta_val/2), np.sin(theta_val/2), 0])
        )

        label_bcos = MathTex(r"b\cos\theta", color=COL_B).scale(0.6).next_to(dashed_h, DOWN, buff=0.1)
        label_bsin = MathTex(r"b\sin\theta", color=COL_B).scale(0.6).next_to(dashed_v, RIGHT, buff=0.1)

        self.play(Create(dashed_h), Create(dashed_v), Create(arc_new), FadeIn(lbl_theta_new))
        self.play(FadeIn(label_bcos), FadeIn(label_bsin))
        self.wait(1)

        # 5. DRAW RESULTANT
        vec_r = Arrow(origin, vec_b.get_end(), buff=0, color=COL_R, stroke_width=10)
        label_r = MathTex("R", color=COL_R).scale(0.9).move_to(vec_r.get_center() + UP*0.3 + LEFT*0.3)
        
        self.play(GrowArrow(vec_r), FadeIn(label_r))
        self.wait(1)

        # 6. ALGEBRAIC DERIVATION
        # Transform the initial logic into the real step
        step1 = MathTex(
            r"R^2 = (a + b\cos\theta)^2 + (b\sin\theta)^2",
            color=TXT
        ).scale(0.7).move_to(initial_logic)

        self.play(ReplacementTransform(initial_logic, step1))
        self.wait(1)

        # Expansion
        step2 = MathTex(
            r"R^2 = a^2 + 2ab\cos\theta + b^2\cos^2\theta + b^2\sin^2\theta",
            color=TXT
        ).scale(0.6).next_to(step1, DOWN, buff=0.4)
        
        step3 = MathTex(
            r"R^2 = a^2 + 2ab\cos\theta + b^2(\sin^2\theta + \cos^2\theta)",
            color=TXT
        ).scale(0.6).next_to(step2, DOWN, buff=0.4)

        self.play(Write(step2))
        self.wait(1)
        self.play(Write(step3))
        self.wait(1)

        # Final Formula
        final_formula = MathTex(
            r"R = \sqrt{a^2 + b^2 + 2ab\cos\theta}",
            color=WHITE
        ).scale(1.0)
        
        final_box = SurroundingRectangle(
            final_formula, color=COL_R, fill_color=COL_R, fill_opacity=1, buff=0.4
        )
        final_group = VGroup(final_box, final_formula).to_edge(DOWN, buff=1.2)

        self.play(
            FadeOut(step1), FadeOut(step2), FadeOut(step3),
            FadeIn(final_box), Write(final_formula)
        )
        self.wait(3)