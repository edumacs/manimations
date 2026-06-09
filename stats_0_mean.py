from manim import *
import numpy as np

# ==========================================================
# VERTICAL CINEMATIC EDUCATION PLATFORM (9:16)
# ==========================================================

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8.0

class GeometricVarianceVertical(Scene):
    def construct(self):
        # Premium Dark Classroom aesthetic
        self.camera.background_color = "#0F172A"

        # --- UPPER SOUND TRACK LINK ---
        self.add_sound("backsound38.mp3")

        # --- SCREEN TITLE ---
        title = Text("VISUALIZING VARIANCE", font_size=36, color=WHITE, weight="BOLD")
        title.to_edge(UP, buff=0.6)
        sub_title = Text("A Geometric Proof", font_size=22, color="#94A3B8").next_to(title, DOWN, buff=0.15)
        self.add(title, sub_title)

        # --- GLOBAL DATA DATASET ---
        # Minimal set with a clean integer mean (Mean = 6)
        data_values = [2, 4, 5, 8, 11]
        mu = 6
        
        # --- TECHNICAL FORMULA CARD DISPLAY ---
        # This serves as a fixed reference frame during the explanation
        formula_box = RoundedRectangle(
            width=7.0, height=1.6, corner_radius=0.15,
            stroke_color="#334155", stroke_width=2, fill_color="#1E293B", fill_opacity=0.8
        ).move_to([0, 3.8, 0])
        
        formula_label = Text("CURRENT FORMULA", font_size=14, color="#64748B", weight="BOLD")
        formula_label.move_to(formula_box.get_top() + DOWN * 0.2)
        
        self.add(formula_box, formula_label)
        
        # Dynamic math placeholder inside the card
        active_formula = MathTex(r"X = \{x_1, x_2, \dots, x_n\}", color="#38BDF8", font_size=38)
        active_formula.move_to(formula_box.get_center() + DOWN * 0.1)
        self.add(active_formula)

        # --- NARROW COMPACT NUMBER LINE ---
        # Scaled to 6.8 width units to completely prevent 9:16 border bleeding
        ax = NumberLine(
            x_range=[0, 12, 1],
            length=6.8,
            color="#64748B",
            include_numbers=True,
            numbers_to_include=[0, 2, 4, 6, 8, 10, 12],
            font_size=20
        ).move_to([0, 1.0, 0])
        
        # Exact system transformation scale factor for calculations
        unit_len = ax.n2p(1)[0] - ax.n2p(0)[0]
        
        self.play(Create(ax), run_time=1.2)
        self.wait(0.5)

        # ==========================================================
        # STEP 1: THE DISCRETE RAW DATA SET
        # ==========================================================
        dots = VGroup()
        for x in data_values:
            dot = Dot(ax.n2p(x), color="#38BDF8", radius=0.12)
            # Add a subtle glowing outer ring
            ring = Dot(ax.n2p(x), color="#38BDF8", radius=0.18, fill_opacity=0.2)
            dots.add(VGroup(ring, dot))
            
        self.play(
            LaggedStart(*[FadeIn(d, shift=UP*0.3) for d in dots], lag_ratio=0.15),
            run_time=1.5
        )
        self.wait(1.0)

        # ==========================================================
        # STEP 2: THE CENTRAL TENDENCY (MEAN)
        # ==========================================================
        new_formula = MathTex(r"\mu = \frac{\sum x_i}{N} = \frac{30}{5} = 6", color="#FBBF24", font_size=36)
        new_formula.move_to(active_formula)
        
        self.play(Transform(active_formula, new_formula))
        
        mean_x = ax.n2p(mu)[0]
        mean_line = DashedLine(
            start=[mean_x, 1.5, 0],
            end=[mean_x, -4.5, 0],
            color="#FBBF24",
            stroke_width=2.5,
            dash_length=0.12
        )
        
        mean_indicator = Triangle(color="#FBBF24", fill_opacity=1).scale(0.12).move_to([mean_x, 1.35, 0], aligned_edge=DOWN)
        mean_indicator.rotate(PI)
        
        self.play(Create(mean_line), FadeIn(mean_indicator))
        self.wait(1.5)

        # ==========================================================
        # STEP 3: THE DEVIATIONS (LINEAR DISTANCE)
        # ==========================================================
        new_formula = MathTex(r"\text{Deviation} = (x_i - \mu)", color="#FB923C", font_size=38)
        new_formula.move_to(active_formula)
        self.play(Transform(active_formula, new_formula))

        deviations = VGroup()
        # Stagger vector elevations downward systematically to keep layout extremely clear
        y_offsets = [-0.4, -0.9, -1.4, -1.9, -2.4]
        
        for idx, x_val in enumerate(data_values):
            start_pt = [mean_x, y_offsets[idx], 0]
            end_pt = [ax.n2p(x_val)[0], y_offsets[idx], 0]
            
            dev_line = Line(start=start_pt, end=end_pt, color="#FB923C", stroke_width=4.5)
            # Add micro anchor lines mapping back to data positions
            anchor = DashedLine(start=ax.n2p(x_val), end=end_pt, color="#475569", stroke_width=1)
            
            deviations.add(VGroup(anchor, dev_line))

        self.play(
            LaggedStart(*[Create(d) for d in deviations], lag_ratio=0.2),
            run_time=2.0
        )
        self.wait(1.5)

        # ==========================================================
        # STEP 4: GEOMETRIC SQUARING (2D EXPANSION)
        # ==========================================================
        new_formula = MathTex(r"\text{Squared Distance} = (x_i - \mu)^2", color="#F87171", font_size=38)
        new_formula.move_to(active_formula)
        self.play(Transform(active_formula, new_formula))

        squares = VGroup()
        for idx, x_val in enumerate(data_values):
            dev_line = deviations[idx][1]
            length_units = abs(x_val - mu)
            pixel_size = length_units * unit_len
            
            # Projecting squares downwards to maximize vertical empty space
            sq = Square(
                side_length=pixel_size,
                stroke_color="#F87171",
                stroke_width=2,
                fill_color="#EF4444",
                fill_opacity=0.25
            )
            
            # Align anchor edges based on left/right position relative to mean
            if x_val > mu:
                sq.next_to(dev_line, DOWN, buff=0).align_to(dev_line, LEFT)
            else:
                sq.next_to(dev_line, DOWN, buff=0).align_to(dev_line, RIGHT)
                
            squares.add(sq)

        # Watch 1D vectors explode outwards into literal physical areas
        self.play(Create(squares), run_time=2.5)
        self.wait(2.0)

        # ==========================================================
        # STEP 5: COMPILING THE MEAN VARIANCE AREA
        # ==========================================================
        new_formula = MathTex(r"\sigma^2 = \frac{\sum (x_i - \mu)^2}{N}", color="#34D399", font_size=38)
        new_formula.move_to(active_formula)
        self.play(Transform(active_formula, new_formula))

        # Completely clean workspace background, maintaining context focus
        self.play(
            FadeOut(ax), FadeOut(dots), FadeOut(deviations),
            FadeOut(mean_line), FadeOut(mean_indicator),
            run_time=1.2
        )

        # Re-center and arrange raw geometric areas to demonstrate aggregation
        squares.generate_target()
        squares.target.arrange(RIGHT, aligned_edge=DOWN, buff=0.15)
        squares.target.move_to([0, -1.5, 0])
        
        self.play(MoveToTarget(squares), run_time=1.8)
        
        # FIX: Explicit layout generation to bypass internal brace.get_text() limitations
        brace = Brace(squares, DOWN, color="#64748B")
        brace_lbl = Text("Total Squared Variance Area = 50", font_size=20, color="#94A3B8")
        brace_lbl.next_to(brace, DOWN, buff=0.15)
        
        self.play(GrowFromCenter(brace), Write(brace_lbl))
        self.wait(2.0)

        # Calculate exact side length for the structural target average area (50 / 5 = 10)
        avg_area = 10.0
        avg_pixel_side = np.sqrt(avg_area) * unit_len

        variance_square = Square(
            side_length=avg_pixel_side,
            stroke_color="#34D399",
            stroke_width=5,
            fill_color="#10B981",
            fill_opacity=0.45
        ).move_to([0, -1.0, 0])

        # Condense all disjoint areas into a single true Average Square
        self.play(
            FadeOut(brace), FadeOut(brace_lbl),
            Transform(squares, variance_square),
            run_time=2.0
        )

        # Display foundational downstream statistical properties
        final_var_lbl = MathTex(r"\text{Variance } (\sigma^2) = \text{Area} = 10.0", color="#34D399", font_size=34)
        final_var_lbl.next_to(variance_square, UP, buff=0.4)
        
        final_sd_lbl = MathTex(r"\text{Std Dev } (\sigma) = \text{Side} = \sqrt{10} \approx 3.16", color=WHITE, font_size=30)
        final_sd_lbl.next_to(variance_square, DOWN, buff=0.4)

        self.play(Write(final_var_lbl), Write(final_sd_lbl))
        self.wait(4.0)

        # ==========================================================
        # CLEAN MINIMAL OUTRO SEQUENCE
        # ==========================================================
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.2)
        self.clear()

        closing_primary = Text("Like & Share", color="#38BDF8", weight="BOLD").scale(0.8)
        closing_secondary = Text("Follow @ScanPintar", color="#F43F5E", weight="BOLD").scale(0.65)
        outro_group = VGroup(closing_primary, closing_secondary).arrange(DOWN, buff=0.35)
        
        self.play(Write(outro_group), run_time=1.2)
        self.wait(2.0)