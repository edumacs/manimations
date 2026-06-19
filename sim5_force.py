from manim import *
import numpy as np

# ==========================================================
# ADVANCED STRUCTURAL ANALYSIS PLATFORM ENGINE (CANTILEVER MODE)
# ==========================================================

# portrait 9:16 aspect ratio
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8

class SimulasiPerhitunganBeban(Scene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        # ==========================================================
        # STRUCTURAL PROPERTIES & GEOMETRY FROM IMAGE
        # ==========================================================
        L = 9.0
        beam_len_screen = 6.0 
        
        # Global Layout Scale Matrix
        Y_HEADER_MAIN = 5.2
        Y_HEADER_SUB = 4.8
        Y_WATERMARK = 4.2
        
        # Shifted diagram up and calculations down to prevent collision
        Y_DIAGRAM = 2.4
        Y_CALC = -2.5
        Y_CLOSING = -5.8
        
        COLOR_PRIMARY = "#0369A1" 
        COLOR_SECONDARY = "#BE123C" 
        COLOR_WATERMARK = "#64748B"
        COLOR_FRAME_STROKE = "#94A3B8"
        COLOR_FRAME_FILL = "#F8FAFC"
        COLOR_BEAM = "#4F6A7A" 
        COLOR_TEXT_GEN = "#1E293B" 
        COLOR_FORCE_ARROW = "#EF4444" 
        COLOR_CALC_TITLE = "#D97706" 
        COLOR_BOX_FORCE = "#16A34A" 
        COLOR_BOX_LOC = "#A855F7" 

        x_diag_start = -beam_len_screen / 2
        x_diag_end = beam_len_screen / 2

        # ==========================================================
        # PHASE 1: STATIC UI FRAMES & HEADERS
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

        diag_frame = create_plot_frame(Y_DIAGRAM, "DIAGRAM BEBAN & GEOMETRI", "#16A34A", height=3.8, width=7.4)
        calc_frame = create_plot_frame(Y_CALC, "LANGKAH PERHITUNGAN", COLOR_CALC_TITLE, height=5.2, width=7.4)
        self.add(diag_frame, calc_frame)

        # ==========================================================
        # PHASE 2: STATIC DIAGRAM AT BEGINNING
        # ==========================================================
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

        def sx(x_val):
            return x_diag_start + (x_val / L) * beam_len_screen

        beam_rect = Rectangle(width=beam_len_screen, height=0.2, stroke_color=COLOR_BEAM, stroke_width=2, fill_color=COLOR_BEAM, fill_opacity=0.3).move_to([0, Y_DIAGRAM, 0])
        self.add(beam_rect)
        
        lbl_A = Text("A", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).next_to(beam_rect, DOWN, buff=0.1).set_x(sx(0))
        lbl_B = Text("B", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).next_to(beam_rect, DOWN, buff=0.1).set_x(sx(6.0))
        lbl_C = Text("C", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).next_to(beam_rect, DOWN, buff=0.1).set_x(sx(9.0))
        self.add(lbl_A, lbl_B, lbl_C)
        
        dim_line_tot = Line([sx(0), Y_DIAGRAM - 1.3, 0], [sx(9.0), Y_DIAGRAM - 1.3, 0], color=COLOR_WATERMARK, stroke_width=1.5)
        for x_tick in [0, 9.0]:
            tick = Line([sx(x_tick), Y_DIAGRAM - 1.3 - 0.08, 0], [sx(x_tick), Y_DIAGRAM - 1.3 + 0.08, 0], color=COLOR_WATERMARK, stroke_width=1.5)
            self.add(tick)
        lbl_tot = Text("9 m (Total Visual)", color=COLOR_WATERMARK, weight="BOLD").scale(0.18).next_to(dim_line_tot, DOWN, buff=0.1)
        self.add(dim_line_tot, lbl_tot)

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

        support_A = draw_pinned_support(sx(0), Y_DIAGRAM)
        support_B = draw_roller_support(sx(6.0), Y_DIAGRAM)
        self.add(support_A, support_B)

        # FIXED Force 1: Load at x=2 (450 N at 60deg to horizontal)
        load_1_tip = np.array([sx(2.0), Y_DIAGRAM + 0.1, 0])
        load_1_origin = load_1_tip + np.array([-1.2 * np.cos(60*DEGREES), 1.2 * np.sin(60*DEGREES), 0])
        p_arrow_1 = Arrow(start=load_1_origin, end=load_1_tip, color=COLOR_FORCE_ARROW, stroke_width=3, tip_length=0.2, buff=0)
        angle_arc_1 = Arc(radius=0.4, start_angle=120*DEGREES, angle=60*DEGREES, arc_center=load_1_tip, color=COLOR_WATERMARK, stroke_width=1.5)
        lbl_arc_1 = Text("60$^\circ$", color=COLOR_WATERMARK).scale(0.15).move_to(load_1_tip + np.array([-0.65, 0.25, 0]))
        lbl_p1 = Text("450 N", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.2).next_to(load_1_origin, UP, buff=0.05)
        self.add(p_arrow_1, angle_arc_1, lbl_arc_1, lbl_p1)

        # FIXED Force 2: Load at B (300 N straight down)
        load_2_tip = np.array([sx(6.0), Y_DIAGRAM + 0.1, 0])
        load_2_origin = load_2_tip + np.array([0, 1.2, 0])
        p_arrow_2 = Arrow(start=load_2_origin, end=load_2_tip, color=COLOR_FORCE_ARROW, stroke_width=3, tip_length=0.2, buff=0)
        lbl_p2 = Text("300 N", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.2).next_to(load_2_origin, UP, buff=0.1)
        self.add(p_arrow_2, lbl_p2)

        # FIXED Force 3: Load at x=9 (700 N at 30deg from vertical)
        load_3_tip = np.array([sx(9.0), Y_DIAGRAM + 0.1, 0])
        load_3_origin = load_3_tip + np.array([1.2 * np.sin(30*DEGREES), 1.2 * np.cos(30*DEGREES), 0])
        p_arrow_3 = Arrow(start=load_3_origin, end=load_3_tip, color=COLOR_FORCE_ARROW, stroke_width=3, tip_length=0.2, buff=0)
        vert_line = DashedLine(load_3_tip, load_3_tip + np.array([0, 1.5, 0]), color=COLOR_WATERMARK, stroke_width=1.5, dash_length=0.12)
        angle_arc_3 = Arc(radius=0.5, start_angle=60*DEGREES, angle=30*DEGREES, arc_center=load_3_tip, color=COLOR_WATERMARK, stroke_width=1.5)
        lbl_arc_3 = Text("30$^\circ$", color=COLOR_WATERMARK).scale(0.15).move_to(load_3_tip + np.array([0.2, 0.65, 0]))
        lbl_p3 = Text("700 N", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.2).next_to(load_3_origin, UP, buff=0.05)
        self.add(p_arrow_3, vert_line, angle_arc_3, lbl_arc_3, lbl_p3)

        couple_C = draw_couple_moment(sx(9.0), Y_DIAGRAM)
        self.add(couple_C)

        self.wait(1.5)

        # ==========================================================
        # PHASE 3: CALCULATION STEPS (FIXED ALIGNMENT)
        # ==========================================================
        x_calc_start = -7.4 / 2 + 0.3 
        
        fh1 = Text("BAGIAN 1: MENENTUKAN RESULTAN GAYA R", color=COLOR_CALC_TITLE).scale(0.22)
        fh1.move_to([x_calc_start, Y_CALC + 2.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(fh1), run_time=1.0)

        # -- Fx --
        fx_sum = MathTex(r"\sum F_x = 450\cos(60^\circ) - 700\sin(30^\circ)", color=COLOR_TEXT_GEN).scale(0.3)
        arrow1 = MathTex(r"\rightarrow", color=COLOR_WATERMARK).scale(0.4)
        fx_val = MathTex(r"R_x = 225 - 350 = -125 \text{ N}", color=COLOR_BOX_FORCE).scale(0.3)
        
        line_fx = VGroup(fx_sum, arrow1, fx_val).arrange(RIGHT, buff=0.2)
        line_fx.move_to([x_calc_start + 0.1, Y_CALC + 1.4, 0], aligned_edge=LEFT)
        
        self.play(Write(fx_sum), run_time=1.0)
        self.play(FadeIn(arrow1), Write(fx_val), run_time=1.0)

        # -- Fy --
        fy_sum = MathTex(r"\sum F_y = -450\sin(60^\circ) - 300 - 700\cos(30^\circ)", color=COLOR_TEXT_GEN).scale(0.3)
        arrow2 = MathTex(r"\rightarrow", color=COLOR_WATERMARK).scale(0.4)
        fy_val = MathTex(r"R_y = -389.7 - 300 - 606.2 = -1295.9 \text{ N}", color=COLOR_BOX_FORCE).scale(0.3)
        
        line_fy = VGroup(fy_sum, arrow2, fy_val).arrange(RIGHT, buff=0.2)
        line_fy.move_to([x_calc_start + 0.1, Y_CALC + 0.8, 0], aligned_edge=LEFT)
        
        self.play(Write(fy_sum), run_time=1.0)
        self.play(FadeIn(arrow2), Write(fy_val), run_time=1.0)

        # -- Resultant --
        fres_eq = MathTex(r"R = \sqrt{{(-125)}^2 + {(-1295.9)}^2}", color=COLOR_TEXT_GEN).scale(0.3)
        arrow3 = MathTex(r"\rightarrow", color=COLOR_WATERMARK).scale(0.4)
        fres_val = MathTex(r"\mathbf{R} \approx \mathbf{1301.9} \textbf{ N}", color=COLOR_BOX_FORCE).scale(0.32)
        
        line_fres = VGroup(fres_eq, arrow3, fres_val).arrange(RIGHT, buff=0.2)
        line_fres.move_to([x_calc_start + 0.1, Y_CALC + 0.2, 0], aligned_edge=LEFT)
        
        fres_box = SurroundingRectangle(fres_val, color=COLOR_BOX_FORCE, stroke_width=2)
        
        self.play(Write(fres_eq), run_time=1.0)
        self.play(FadeIn(arrow3), Write(fres_val), run_time=1.0)
        self.play(Create(fres_box), run_time=0.5)

        # -- Moment --
        fh2 = Text("BAGIAN 2: MENENTUKAN LOKASI R DARI B", color=COLOR_CALC_TITLE).scale(0.22)
        fh2.move_to([x_calc_start, Y_CALC - 0.5, 0], aligned_edge=LEFT)
        self.play(FadeIn(fh2), run_time=0.8)

        mb_sum = MathTex(r"\sum M_B (\text{CW}+) = 450\sin(60^\circ)(4) - 700\cos(30^\circ)(3) - 1500", color=COLOR_TEXT_GEN).scale(0.3)
        mb_sum.move_to([x_calc_start + 0.1, Y_CALC - 1.0, 0], aligned_edge=LEFT)
        self.play(Write(mb_sum), run_time=1.5)

        mb_val = MathTex(r"M_{B,net} = 1558.8 - 1818.6 - 1500 = -1759.8 \text{ N$\cdot$m}", color=COLOR_TEXT_GEN).scale(0.3)
        mb_cw = Text("= 1759.8 N$\cdot$m (CW)", color=COLOR_WATERMARK).scale(0.18)
        
        line_mb = VGroup(mb_val, mb_cw).arrange(RIGHT, buff=0.2)
        line_mb.move_to([x_calc_start + 0.1, Y_CALC - 1.5, 0], aligned_edge=LEFT)
        
        self.play(Write(mb_val), run_time=1.0)
        self.play(FadeIn(mb_cw), run_time=0.5)

        # -- Distance d --
        d_eq = MathTex(r"d = \frac{|\sum M_B|}{|R_y|} = \frac{1759.8}{1295.9}", color=COLOR_TEXT_GEN).scale(0.3)
        arrow4 = MathTex(r"\rightarrow", color=COLOR_WATERMARK).scale(0.4)
        
        d_val = MathTex(r"d \approx 1.36 \text{ m}", color=COLOR_BOX_LOC).scale(0.32)
        d_side = Text("(Di sebelah kanan B)", color=COLOR_WATERMARK).scale(0.18)
        d_result_group = VGroup(d_val, d_side).arrange(RIGHT, buff=0.1)
        
        line_d = VGroup(d_eq, arrow4, d_result_group).arrange(RIGHT, buff=0.2)
        line_d.move_to([x_calc_start + 0.1, Y_CALC - 2.1, 0], aligned_edge=LEFT)
        
        d_box = SurroundingRectangle(d_result_group, color=COLOR_BOX_LOC, stroke_width=2)
        
        self.play(Write(d_eq), run_time=1.0)
        self.play(FadeIn(arrow4), Write(d_result_group), run_time=1.0)
        self.play(Create(d_box), run_time=0.5)
        self.wait(1.5)

        # ==========================================================
        # PHASE 4: RESULTANT FORCE ANIMATION
        # ==========================================================
        # Fade out original forces
        self.play(
            FadeOut(p_arrow_1), FadeOut(lbl_p1), FadeOut(angle_arc_1), FadeOut(lbl_arc_1), 
            FadeOut(p_arrow_2), FadeOut(lbl_p2),
            FadeOut(p_arrow_3), FadeOut(lbl_p3), FadeOut(angle_arc_3), FadeOut(lbl_arc_3), FadeOut(vert_line),
            FadeOut(couple_C),
            run_time=1.2
        )

        # Calculate coordinates for Resultant Force (1.36m right of B)
        x_res = 6.0 + 1.36
        
        # Resultant vector is pointing mostly down (y=-1295), slightly left (x=-125)
        res_start = [sx(x_res) + 0.15, Y_DIAGRAM + 1.6, 0] 
        res_end = [sx(x_res), Y_DIAGRAM + 0.1, 0]

        res_arrow = Arrow(start=res_start, end=res_end, color=COLOR_BOX_FORCE, stroke_width=5, tip_length=0.25, buff=0)
        res_lbl = Text("R = 1301.9 N", color=COLOR_BOX_FORCE, weight="BOLD").scale(0.2).next_to(res_arrow.get_start(), UP, buff=0.1)

        d_arrow = DoubleArrow(start=[sx(6.0), Y_DIAGRAM - 0.45, 0], end=[sx(x_res), Y_DIAGRAM - 0.45, 0], color=COLOR_BOX_LOC, stroke_width=2, tip_length=0.1)
        d_lbl = Text("d = 1.36 m", color=COLOR_BOX_LOC, weight="BOLD").scale(0.18).next_to(d_arrow, DOWN, buff=0.08)

        # Emphasize reference point B
        highlight_B = Circle(radius=0.25, color=COLOR_BOX_LOC, stroke_width=3).move_to([sx(6.0), Y_DIAGRAM, 0])

        self.play(FadeIn(highlight_B))
        self.play(GrowArrow(d_arrow), Write(d_lbl), run_time=1.0)
        self.play(GrowArrow(res_arrow), Write(res_lbl), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(highlight_B))
        self.wait(2.5)

        # ==========================================================
        # PHASE 5: OUTRO SEQUENCE
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