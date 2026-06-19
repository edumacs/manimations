from manim import *
import numpy as np

# ==========================================================
# ADVANCED STRUCTURAL ANALYSIS PLATFORM ENGINE (CANTILEVER MODE)
# ==========================================================

# portrait 9:16 aspect ratio, as requested
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8

class SimulasiPerhitunganBeban(Scene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        # ==========================================================
        # AUDIO TRACK (Optional Failsafe)
        # ==========================================================
        try:
            self.add_sound("backsound.mp3")
        except Exception:
            pass

        # ==========================================================
        # STRUCTURAL PROPERTIES & GEOMETRY FROM IMAGE
        # ==========================================================
        # Total length of the beam (m). Visual length only for scaling diagrams.
        L = 9.0
        # Reduced from 7.4 to prevent labels from getting cut off at the edge of the 9x16 frame.
        beam_len_screen = 6.0 
        
        # Global Layout Scale Matrix (Adjusted for portrait frame)
        Y_HEADER_MAIN = 5.2
        Y_HEADER_SUB = 4.8
        Y_WATERMARK = 4.2
        
        Y_DIAGRAM = 2.0
        Y_CALC = -2.0
        # Positioned closer to the bottom to allow space for calculation steps.
        Y_CLOSING = -5.5
        
        # Color palette inspired by reference code
        COLOR_PRIMARY = "#0369A1" # Header primary
        COLOR_SECONDARY = "#BE123C" # Header sub, BMD fill
        COLOR_WATERMARK = "#64748B"
        COLOR_FRAME_STROKE = "#94A3B8"
        COLOR_FRAME_FILL = "#F8FAFC"
        # Greyish blue from beam visual
        COLOR_BEAM = "#4F6A7A" 
        # Dark grey for general text
        COLOR_TEXT_GEN = "#1E293B" 
        # Red for forces
        COLOR_FORCE_ARROW = "#EF4444" 
        # Yellow for calc titles
        COLOR_CALC_TITLE = "#D97706" 
        # Green box for force results
        COLOR_BOX_FORCE = "#16A34A" 
        # Purple box for location result
        COLOR_BOX_LOC = "#A855F7" 

        x_diag_start = -beam_len_screen / 2
        x_diag_end = beam_len_screen / 2

        # ==========================================================
        # STATIC UI FRAMES & HEADERS
        # ==========================================================
        def create_plot_frame(center_y, label, accent_color, height=3.0, width=7.4):
            frame = RoundedRectangle(
                width=width, height=height, corner_radius=0.12,
                stroke_color=COLOR_FRAME_STROKE, stroke_width=1.5,
                fill_color=COLOR_FRAME_FILL, fill_opacity=0.9
            ).move_to([0, center_y, 0])
            
            x_frame_start = -width/2
            accent_tag = Rectangle(
                width=0.08, height=0.35,
                fill_color=accent_color, fill_opacity=1, stroke_width=0
            ).move_to([x_frame_start + 0.15, center_y + (height/2 - 0.25), 0], aligned_edge=LEFT)

            title_text = Text(label, color=COLOR_TEXT_GEN, weight="BOLD").scale(0.24)
            title_text.move_to([x_frame_start + 0.3, center_y + (height/2 - 0.25), 0], aligned_edge=LEFT)
            
            return VGroup(frame, accent_tag, title_text)

        header_title = Text("SIMULASI PERHITUNGAN BEBAN BALOK", color=COLOR_PRIMARY, weight="BOLD").scale(0.35)
        header_sub = Text("ANALISIS GAYA RESULTAN DAN LOKASINYA", color=COLOR_SECONDARY).scale(0.25)
        
        header_title.move_to([0, Y_HEADER_MAIN, 0])
        header_sub.next_to(header_title, DOWN, buff=0.15)
        self.add(header_title, header_sub)

        watermark = Text("@ScanPintar", color=COLOR_WATERMARK, weight="BOLD").scale(0.30)
        watermark.move_to([0, Y_WATERMARK, 0])
        self.add(watermark)

        # Create frames for diagram and calculation areas
        diag_frame = create_plot_frame(Y_DIAGRAM, "DIAGRAM BEBAN & GEOMETRI", "#16A34A", height=3.8, width=7.4)
        # Larger frame for all calculations. Position adjusted.
        calc_frame = create_plot_frame(Y_CALC, "LANGKAH PERHITUNGAN", COLOR_CALC_TITLE, height=5.5, width=7.4)
        self.add(diag_frame, calc_frame)

        # ==========================================================
        # PHASE 2: STATIC DIAGRAM AT BEGINNING
        # ==========================================================
        diagram_group = VGroup()
        
        def draw_pinned_support(x, y):
            base_rect = Rectangle(width=0.4, height=0.08, stroke_width=1).set_color(COLOR_TEXT_GEN).move_to([x, y - 0.3, 0])
            dots = VGroup(*[Circle(radius=0.015, color=COLOR_TEXT_GEN, fill_opacity=1) for _ in range(4)])
            dots.arrange_in_grid(1, 4, buff=0.04).next_to(base_rect, DOWN, buff=0.03)
            pedestal_rect = Rectangle(width=0.25, height=0.15, stroke_width=1).set_color(COLOR_TEXT_GEN).next_to(base_rect, UP, buff=0.01)
            pin_circle = Circle(radius=0.05, color=COLOR_TEXT_GEN, stroke_width=1, fill_opacity=0).move_to(pedestal_rect.get_center())
            beam_support_plate = Rectangle(width=0.12, height=0.05, stroke_width=1).set_color(COLOR_TEXT_GEN).next_to(pin_circle, UP, buff=0.01)
            return VGroup(base_rect, dots, pedestal_rect, pin_circle, beam_support_plate)

        def draw_roller_support(x, y):
            roller_circle = Circle(radius=0.1, color=COLOR_TEXT_GEN, stroke_width=1, fill_opacity=0).move_to([x, y - 0.25, 0])
            base_rect = Rectangle(width=0.5, height=0.08, stroke_width=1).set_color(COLOR_TEXT_GEN).move_to([x, y - 0.35, 0])
            dots = VGroup(*[Circle(radius=0.015, color=COLOR_TEXT_GEN, fill_opacity=1) for _ in range(4)])
            dots.arrange_in_grid(1, 4, buff=0.04).next_to(base_rect, DOWN, buff=0.03)
            return VGroup(roller_circle, base_rect, dots)

        def draw_couple_moment(x, y):
            couple_arrow = Arc(radius=0.3, start_angle=-20*DEGREES, angle=220*DEGREES, color=COLOR_FORCE_ARROW, stroke_width=2.5)
            couple_arrow.add_tip(tip_shape=StealthTip, tip_length=0.2).move_to([x, y, 0])
            couple_label = Text("1500 N$\cdot$m", color=COLOR_FORCE_ARROW, weight="BOLD").scale(0.18).next_to(couple_arrow, RIGHT, buff=0.08)
            return VGroup(couple_arrow, couple_label)

        # Coordinate mapping for diagram on screen
        def sx(x_val):
            return x_diag_start + (x_val / L) * beam_len_screen

        beam_rect = Rectangle(width=beam_len_screen, height=0.2, stroke_color=COLOR_BEAM, stroke_width=2, fill_color=COLOR_BEAM, fill_opacity=0.3).move_to([0, Y_DIAGRAM, 0])
        self.add(beam_rect)
        
        lbl_A = Text("A", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).next_to(beam_rect, DOWN, buff=0.1).set_x(sx(0))
        lbl_B = Text("B", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).next_to(beam_rect, DOWN, buff=0.1).set_x(sx(6.0))
        lbl_C = Text("C", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).next_to(beam_rect, DOWN, buff=0.1).set_x(sx(9.0))
        self.add(lbl_A, lbl_B, lbl_C)
        
        # Dimension lines - overall
        dim_line_tot = Line([sx(0), Y_DIAGRAM - 1.3, 0], [sx(9.0), Y_DIAGRAM - 1.3, 0], color=COLOR_WATERMARK, stroke_width=1.5)
        for x_tick in [0, 9.0]:
            tick = Line([sx(x_tick), Y_DIAGRAM - 1.3 - 0.08, 0], [sx(x_tick), Y_DIAGRAM - 1.3 + 0.08, 0], color=COLOR_WATERMARK, stroke_width=1.5)
            self.add(tick)
        lbl_tot = Text("9 m (Total Visual)", color=COLOR_WATERMARK, weight="BOLD").scale(0.18).next_to(dim_line_tot, DOWN, buff=0.1)
        self.add(dim_line_tot, lbl_tot)

        # Dimension lines - sections
        dim_line_sect = VGroup()
        ticks_sect = VGroup()
        for x_tick in [0, 2.0, 6.0, 9.0]:
            tick = Line([sx(x_tick), Y_DIAGRAM - 1.1 - 0.08, 0], [sx(x_tick), Y_DIAGRAM - 1.1 + 0.08, 0], color=COLOR_WATERMARK, stroke_width=1.5)
            ticks_sect.add(tick)
        
        dim_2m = Line([sx(0), Y_DIAGRAM - 1.1, 0], [sx(2.0), Y_DIAGRAM - 1.1, 0], color=COLOR_WATERMARK, stroke_width=1.5)
        dim_4m = Line([sx(2.0), Y_DIAGRAM - 1.1, 0], [sx(6.0), Y_DIAGRAM - 1.1, 0], color=COLOR_WATERMARK, stroke_width=1.5)
        dim_3m = Line([sx(6.0), Y_DIAGRAM - 1.1, 0], [sx(9.0), Y_DIAGRAM - 1.1, 0], color=COLOR_WATERMARK, stroke_width=1.5)
        dim_line_sect.add(dim_2m, dim_4m, dim_3m)

        lbl_2m = Text("2 m", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).move_to([sx(1.0), Y_DIAGRAM - 1.1, 0], aligned_edge=DOWN).shift(UP*0.1)
        lbl_4m = Text("4 m", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).move_to([sx(4.0), Y_DIAGRAM - 1.1, 0], aligned_edge=DOWN).shift(UP*0.1)
        lbl_3m = Text("3 m", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).move_to([sx(7.5), Y_DIAGRAM - 1.1, 0], aligned_edge=DOWN).shift(UP*0.1)
        
        self.add(dim_line_sect, ticks_sect, lbl_2m, lbl_4m, lbl_3m)

        # Draw supports
        support_A = draw_pinned_support(sx(0), Y_DIAGRAM)
        support_B = draw_roller_support(sx(6.0), Y_DIAGRAM)
        self.add(support_A, support_B)

        # Load at x=2 (450 N at 60deg from horizontal)
        load_1_origin = [sx(2.0), Y_DIAGRAM + 1.0, 0]
        load_1_tip = [sx(2.0), Y_DIAGRAM + 0.1, 0]
        horiz_line = Line([sx(2.0) - 0.5, Y_DIAGRAM + 1.0, 0], [sx(2.0) + 0.5, Y_DIAGRAM + 1.0, 0], color=COLOR_WATERMARK, stroke_width=1)
        angle_arc_1 = Arc(radius=0.4, start_angle=180*DEGREES, angle=60*DEGREES, color=COLOR_WATERMARK, stroke_width=1.5).move_to(load_1_origin)
        angle_arc_1.shift(RIGHT*0.15)
        lbl_arc_1 = Text("60$^\circ$", color=COLOR_WATERMARK).scale(0.15).move_to([sx(2.0) - 0.25, Y_DIAGRAM + 1.25, 0])
        p_arrow_1 = Arrow(start=load_1_origin, end=load_1_tip, color=COLOR_FORCE_ARROW, stroke_width=3, tip_length=0.2, buff=0)
        lbl_p1 = Text("450 N", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.2).move_to([sx(2.0) + 0.3, Y_DIAGRAM + 1.2, 0], aligned_edge=LEFT)
        self.add(horiz_line, angle_arc_1, lbl_arc_1, p_arrow_1, lbl_p1)

        # Load at B (300 N straight down)
        load_2_origin = [sx(6.0), Y_DIAGRAM + 0.9, 0]
        load_2_tip = [sx(6.0), Y_DIAGRAM + 0.1, 0]
        p_arrow_2 = Arrow(start=load_2_origin, end=load_2_tip, color=COLOR_FORCE_ARROW, stroke_width=3, tip_length=0.2, buff=0)
        lbl_p2 = Text("300 N", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.2).next_to(load_2_origin, UP, buff=0.1)
        self.add(p_arrow_2, lbl_p2)

        # Load at x=9 (700 N at 30deg from vertical)
        load_3_origin = [sx(9.0), Y_DIAGRAM + 1.0, 0]
        vert_line = DashedLine([sx(9.0), Y_DIAGRAM, 0], [sx(9.0), Y_DIAGRAM + 1.5, 0], color=COLOR_WATERMARK, stroke_width=1.5, dash_length=0.12)
        arrow_len = 1.0
        load_3_tip = [sx(9.0) - arrow_len * np.sin(30*DEGREES), Y_DIAGRAM + 0.1, 0]
        p_arrow_3 = Arrow(start=load_3_origin, end=load_3_tip, color=COLOR_FORCE_ARROW, stroke_width=3, tip_length=0.2, buff=0)
        angle_arc_3 = Arc(radius=0.4, start_angle=90*DEGREES, angle=30*DEGREES, color=COLOR_WATERMARK, stroke_width=1.5).move_to(load_3_origin)
        angle_arc_3.shift(DOWN*0.1)
        lbl_arc_3 = Text("30$^\circ$", color=COLOR_WATERMARK).scale(0.15).move_to([sx(9.0) - 0.2, Y_DIAGRAM + 1.3, 0])
        lbl_p3 = Text("700 N", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.2).move_to([sx(9.0) + 0.3, Y_DIAGRAM + 1.2, 0], aligned_edge=LEFT)
        self.add(p_arrow_3, vert_line, angle_arc_3, lbl_arc_3, lbl_p3)

        # Couple moment at x=9
        couple_C = draw_couple_moment(sx(9.0), Y_DIAGRAM)
        self.add(couple_C)

        self.wait(2.5, frozen_frame=False)

        # ==========================================================
        # PHASE 3: CALCULATION STEPS
        # ==========================================================
        calc_content_group = VGroup()
        x_calc_start = -7.4 / 2 + 0.3 # x-coordinate from frame start
        
        # Sub-header for force part
        fh1 = Text("BAGIAN 1: MENENTUKAN RESULTAN GAYA R", color=COLOR_CALC_TITLE).scale(0.22)
        fh1.move_to([x_calc_start, Y_CALC + 2.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(fh1), run_time=1.0)
        self.wait(1.0)

        # Sum of forces in x
        fx_sum = MathTex(
            r"\sum F_x = 450\cos(60^\circ) - 700\sin(30^\circ)",
            color=COLOR_TEXT_GEN
        ).scale(0.3)
        fx_val = MathTex(
            r"R_x = 225 - 350 = -125 \text{ N}",
            color=COLOR_BOX_FORCE
        ).scale(0.3)
        line_fx = VGroup(fx_sum, fx_val, Arrow([0, 0, 0], [0.5, 0, 0], color=BLUE))
        line_fx.move_to([x_calc_start + 0.1, Y_CALC + 1.5, 0], aligned_edge=LEFT)
        self.play(Write(fx_sum), run_time=1.5)
        self.wait(0.8)
        self.play(Write(fx_val), run_time=1.0)
        self.wait(1.0)

        # Sum of forces in y
        fy_sum = MathTex(
            r"\sum F_y = -450\sin(60^\circ) - 300 - 700\cos(30^\circ)",
            color=COLOR_TEXT_GEN
        ).scale(0.3)
        fy_val = MathTex(
            r"R_y = -389.7 - 300 - 606.2 = -1295.9 \text{ N}",
            color=COLOR_BOX_FORCE
        ).scale(0.3)
        
        # FIXED: Removed the origin coordinate [0,0,0] from Vector
        line_fy = VGroup(fy_sum, fy_val, Vector([0, -0.5, 0], color=COLOR_WATERMARK)).arrange(RIGHT, buff=0.1)
        line_fy.move_to([x_calc_start + 0.1, Y_CALC + 1.1, 0], aligned_edge=LEFT)
        
        self.play(Write(fy_sum), run_time=1.5)
        self.wait(0.8)
        self.play(Write(fy_val), run_time=1.0)
        self.wait(1.0)

        # Resultant magnitude equation
        fres_eq = MathTex(
            r"R = \sqrt{{(-125)}^2 + {(-1295.9)}^2}",
            color=COLOR_TEXT_GEN
        ).scale(0.3)
        fres_val = MathTex(
            r"\mathbf{R} \approx \mathbf{1301.9} \textbf{ N}",
            color=COLOR_BOX_FORCE
        ).scale(0.32)
        fres_box = SurroundingRectangle(fres_val, color=COLOR_BOX_FORCE, stroke_width=2)
        
        # FIXED: Removed the origin coordinate [0,0,0] from Vector
        line_fres = VGroup(fres_eq, Vector([0.5, -0.5, 0], color=COLOR_WATERMARK), fres_val, fres_box).arrange(RIGHT, buff=0.1)
        line_fres.move_to([x_calc_start + 0.1, Y_CALC + 0.6, 0], aligned_edge=LEFT)
        
        self.play(Write(fres_eq), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(fres_box), Write(fres_val), run_time=1.0)
        self.wait(2.0)

        # Sub-header for location part
        fh2 = Text("BAGIAN 2: MENENTUKAN LOKASI R DARI B", color=COLOR_CALC_TITLE).scale(0.22)
        fh2.move_to([x_calc_start, Y_CALC - 0.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(fh2), run_time=1.0)
        self.wait(1.0)

        # Sum of moments about B equation
        mb_sum = MathTex(
            r"\sum M_B (\text{CW}+) = 450\sin(60^\circ)(4) - 700\cos(30^\circ)(3) - 1500",
            color=COLOR_TEXT_GEN
        ).scale(0.3)
        mb_sum.move_to([x_calc_start + 0.1, Y_CALC - 0.7, 0], aligned_edge=LEFT)
        self.play(Write(mb_sum), run_time=2.0)
        self.wait(1.5)

        mb_val = MathTex(
            r"M_{B,net} = 1558.8 - 1818.6 - 1500 = -1759.8 \text{ N$\cdot$m}",
            color=COLOR_TEXT_GEN
        ).scale(0.3)
        mb_cw = Text("= 1759.8 N$\cdot$m (CW)", color=COLOR_WATERMARK).scale(0.18).next_to(mb_val, RIGHT, buff=0.08)
        line_mb = VGroup(mb_val, mb_cw)
        line_mb.move_to([x_calc_start + 0.1, Y_CALC - 1.1, 0], aligned_edge=LEFT)
        self.play(Write(mb_val), run_time=1.5)
        self.wait(0.8)
        self.play(FadeIn(mb_cw), run_time=0.8)
        self.wait(1.5)

        # Location d equation
        d_eq = MathTex(
            r"d = \frac{|\sum M_B|}{|R_y|} = \frac{1759.8}{1295.9}",
            color=COLOR_TEXT_GEN
        ).scale(0.3)
        d_val = MathTex(
            r"d \approx 1.36 \text{ m}",
            color=COLOR_BOX_LOC
        ).scale(0.32)
        d_side = Text("(Di sebelah kanan B)", color=COLOR_WATERMARK).scale(0.18).next_to(d_val, RIGHT, buff=0.08)
        d_box = SurroundingRectangle(VGroup(d_val, d_side), color=COLOR_BOX_LOC, stroke_width=2)

        # FIXED: Removed the origin coordinate [0,0,0] from Vector
        line_d = VGroup(d_eq, Vector([0.5, 0, 0], color=COLOR_WATERMARK), d_val, d_side, d_box).arrange(RIGHT, buff=0.1)
        line_d.move_to([x_calc_start + 0.1, Y_CALC - 1.6, 0], aligned_edge=LEFT)
        
        self.play(Write(d_eq), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(d_box), Write(d_val), Write(d_side), run_time=1.0)
        self.wait(3.0)

        # ==========================================================
        # PHASE 4: OUTRO SEQUENCE
        # ==========================================================
        for mob in self.mobjects:
            mob.clear_updaters()

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.0)
        self.clear() 

        closing_primary = Text("Suka & Bagikan", color="#0369A1", weight="BOLD").scale(0.7)
        closing_secondary = Text("Ikuti @ScanPintar", color="#BE123C", weight="BOLD").scale(0.5)
        outro_group = VGroup(closing_primary, closing_secondary).arrange(DOWN, buff=0.4)
        outro_group.move_to([0, Y_CLOSING, 0])

        self.play(Write(outro_group), run_time=1.5)
        self.wait(2.5)

if __name__ == "__main__":
    import os
    os.system("manim -pql simulasi_perhitungan_beban.py SimulasiPerhitunganBeban")