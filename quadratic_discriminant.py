from manim import *
import numpy as np

# ---------------------------------------------------------
# GLOBAL CONFIGURATION (TikTok / Reels / Shorts)
# ---------------------------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#0e0e11"


class DiscriminantExplainer(Scene):

    # -----------------------------------------------------
    # HELPER: TITLE MANAGER
    # -----------------------------------------------------
    def set_title(self, new_title_group):
        if hasattr(self, "current_title_group"):
            self.play(FadeOut(self.current_title_group))
        self.current_title_group = new_title_group
        self.play(Write(self.current_title_group))

    def construct(self):

        # =====================================================
        # SCENE 1 — WHAT DOES "CROSS X-AXIS" MEAN?
        # =====================================================
        # 1. Top Section (Text)
        title_text = Text("Kapan sebuah kurva\n memotong sumbu X?", font_size=50)
        eq = MathTex("y = ax^2 + bx + c", font_size=60, color=BLUE_B)
        root_label = Text("Memotong berarti y = 0", font_size=40, color=RED)

        # Group and arrange top elements
        header_group = VGroup(title_text, eq, root_label).arrange(DOWN, buff=0.4)
        header_group.to_edge(UP, buff=1.0)

        # 2. Bottom Section (Graph)
        axes = Axes(
            x_range=[-3, 3], y_range=[-2, 5],
            x_length=7, y_length=6,
            tips=False, axis_config={"color": GREY_B}
        ).to_edge(DOWN, buff=1.5)

        graph = axes.plot(lambda x: x**2 - 1, color=BLUE)

        # 3. Intersection Points & Arrows
        p1 = axes.c2p(-1, 0)
        p2 = axes.c2p(1, 0)
        
        roots = VGroup(
            Dot(p1, color=RED, radius=0.15),
            Dot(p2, color=RED, radius=0.15),
        )

        arrows = VGroup(
            Arrow(start=p1 + UP + LEFT, end=p1, color=RED, buff=0.1),
            Arrow(start=p2 + UP + RIGHT, end=p2, color=RED, buff=0.1)
        )

        # Animation Sequence
        self.set_title(header_group)
        self.play(Create(axes), Create(graph))
        self.play(ScaleInPlace(roots, 1.5), FadeIn(roots))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]))
        self.wait(2)

        self.play(FadeOut(arrows), FadeOut(roots), FadeOut(graph), FadeOut(axes))

        # =====================================================
        # SCENE 2 — WHY f(x) = 0?
        # =====================================================
        t2 = Text("Kenapa harus\nmemecahkan f(x) = 0?", font_size=48)
        
        step1 = MathTex("y = f(x)", font_size=56)
        step2 = MathTex("\\text{Pada sumbu X, } y = 0", font_size=48)
        step3 = MathTex("\\therefore f(x) = 0", font_size=64, color=YELLOW)

        group2 = VGroup(t2, step1, step2, step3).arrange(DOWN, buff=0.6)
        group2.to_edge(UP, buff=2.0)

        self.set_title(group2)
        self.wait(2)

        # =====================================================
        # SCENE 3 — QUADRATIC FORMULA
        # =====================================================
        t3 = Text("Cari nilai x", font_size=50)
        
        # Split formula to ensure it fits width
        formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            font_size=60
        )
        
        group3 = VGroup(t3, formula).arrange(DOWN, buff=0.8)
        group3.to_edge(UP, buff=2.0)

        self.set_title(group3)
        self.wait(1)

        # Highlight Discriminant
        disc_part = formula.get_part_by_tex("b^2 - 4ac")
        rect = SurroundingRectangle(disc_part, color=YELLOW, buff=0.1)
        
        lbl_D = MathTex("D = b^2 - 4ac", font_size=70, color=YELLOW)
        lbl_D.next_to(formula, DOWN, buff=1.0)

        self.play(Create(rect))
        self.play(Write(lbl_D))
        self.wait(2)

        # Keep lbl_D for next scene, fade others
        self.play(FadeOut(group3), FadeOut(rect), lbl_D.animate.to_edge(UP, buff=1))
        self.current_title_group = lbl_D # Update reference

        # =====================================================
        # SCENE 4 — GEOMETRIC MEANING
        # =====================================================
        # D is already at top
        
        vertex_eq = MathTex("y = a(x-h)^2 + k", font_size=50)
        
        # Explanation text with wrapping for vertical screen
        exp_text = Text(
            "D menentukan posisi\nvertikal puncak.",
            font_size=40,
            line_spacing=1.3,
            t2c={"vertical": BLUE}
        )

        group4 = VGroup(vertex_eq, exp_text).arrange(DOWN, buff=0.5)
        group4.next_to(lbl_D, DOWN, buff=1)

        self.play(Write(group4))
        self.wait(2)
        
        self.play(FadeOut(group4), FadeOut(lbl_D))

        # =====================================================
        # SCENE 5 — THREE CASES (FIXED OVERLAP & ADDED POINTS)
        # =====================================================
        title5 = Text("Tiga kasus", font_size=56).to_edge(UP, buff=1)
        self.play(Write(title5))

        axes = Axes(
            x_range=[-3, 3], y_range=[-3, 4],
            x_length=7, y_length=6,
            tips=False, axis_config={"color": GREY_B}
        ).to_edge(DOWN, buff=1.5)
        
        self.play(Create(axes))

        # --- CASE 1: D > 0 ---
        label_pos = MathTex("D > 0 \\Rightarrow 2 \\text{ Akar}", font_size=56, color=GREEN)
        label_pos.next_to(title5, DOWN, buff=0.5)
        
        graph_pos = axes.plot(lambda x: x**2 - 1.5, color=GREEN)
        
        # Points
        dot1 = Dot(axes.c2p(-1.22, 0), color=GREEN)
        dot2 = Dot(axes.c2p(1.22, 0), color=GREEN)
        arr1 = Arrow(start=axes.c2p(-1.22, -1.5), end=axes.c2p(-1.22, -0.1), color=GREEN, buff=0)
        arr2 = Arrow(start=axes.c2p(1.22, -1.5), end=axes.c2p(1.22, -0.1), color=GREEN, buff=0)

        case1_group = VGroup(label_pos, graph_pos, dot1, dot2, arr1, arr2)

        self.play(Write(label_pos))
        self.play(Create(graph_pos))
        self.play(FadeIn(dot1), FadeIn(dot2), GrowArrow(arr1), GrowArrow(arr2))
        self.wait(2)

        # --- CASE 2: D = 0 ---
        label_zero = MathTex("D = 0 \\Rightarrow 1 \\text{ Akar}", font_size=56, color=ORANGE)
        label_zero.move_to(label_pos)
        
        graph_zero = axes.plot(lambda x: x**2, color=ORANGE)
        
        dot_z = Dot(axes.c2p(0, 0), color=ORANGE)
        arr_z = Arrow(start=axes.c2p(0, -1.5), end=axes.c2p(0, -0.1), color=ORANGE, buff=0)

        case2_group = VGroup(label_zero, graph_zero, dot_z, arr_z)

        self.play(FadeOut(case1_group))
        self.play(Write(label_zero))
        self.play(Create(graph_zero))
        self.play(FadeIn(dot_z), GrowArrow(arr_z))
        self.wait(2)

        # --- CASE 3: D < 0 ---
        label_neg = MathTex("D < 0 \\Rightarrow \\text{Tak ada\nakar nyata (real)}", font_size=56, color=RED)
        label_neg.move_to(label_pos)
        
        graph_neg = axes.plot(lambda x: x**2 + 1.5, color=RED)
        
        case3_group = VGroup(label_neg, graph_neg)

        self.play(FadeOut(case2_group))
        self.play(Write(label_neg))
        self.play(Create(graph_neg))
        self.wait(2)

        self.play(FadeOut(case3_group), FadeOut(axes), FadeOut(title5))

        # =====================================================
        # SCENE 6 — FINAL DYNAMIC MODEL
        # =====================================================
        final_title = Text("Model dinamis", font_size=50).to_edge(UP, buff=1)
        
        # Status text fixed below title
        status_text = MathTex("Mengecek akar-akar...", font_size=48)
        status_text.next_to(final_title, DOWN, buff=0.5)

        axes = Axes(
            x_range=[-3, 3], y_range=[-3, 5],
            x_length=7, y_length=8,
            tips=False, axis_config={"color": GREY_B}
        ).to_edge(DOWN, buff=0.5)

        h = ValueTracker(-2.0)

        # Dynamic Parabola
        parabola = always_redraw(
            lambda: axes.plot(lambda x: x**2 + h.get_value(), color=BLUE)
        )

        # Dynamic Dots (Only appear when crossing x-axis)
        def get_dots():
            h_val = h.get_value()
            group = VGroup()
            
            # If h <= 0, we have roots at +/- sqrt(-h)
            if h_val <= 0.05: # Small buffer for float comparison
                root_val = np.sqrt(abs(h_val))
                
                # Left Dot
                d1 = Dot(axes.c2p(-root_val, 0), color=RED, radius=0.12)
                group.add(d1)
                
                # Right Dot (only if distinct, but visuals overlap anyway so it's fine)
                d2 = Dot(axes.c2p(root_val, 0), color=RED, radius=0.12)
                group.add(d2)
                
            return group

        dynamic_dots = always_redraw(get_dots)

        # Dynamic Status Text
        def get_status():
            val = h.get_value()
            if val < -0.1:
                return MathTex("D > 0 \\quad (2 \\text{ akar})", color=GREEN).next_to(final_title, DOWN, buff=0.5)
            elif abs(val) <= 0.1:
                 return MathTex("D = 0 \\quad (1 \\text{ akar})", color=ORANGE).next_to(final_title, DOWN, buff=0.5)
            else:
                 return MathTex("D < 0 \\quad (Tidak ada akar)", color=RED).next_to(final_title, DOWN, buff=0.5)

        dynamic_label = always_redraw(get_status)

        self.play(Write(final_title), Create(axes))
        self.add(parabola, dynamic_dots, dynamic_label)

        # Animation Loop
        self.play(h.animate.set_value(0), run_time=2)   # Go to 1 root
        self.wait(0.5)
        self.play(h.animate.set_value(2), run_time=1.5) # Go to 0 roots
        self.wait(0.5)
        self.play(h.animate.set_value(-2), run_time=2)  # Go to 2 roots
        
        self.wait(3)