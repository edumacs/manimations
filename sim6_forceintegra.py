from manim import *
import numpy as np

# ==========================================================
# ADVANCED STRUCTURAL ANALYSIS PLATFORM ENGINE (DISTRIBUTED LOAD - REVISED)
# ==========================================================

# portrait 9:16 aspect ratio
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8

class SimulasiDistribusiBeban(Scene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        # ==========================================================
        # STRUCTURAL PROPERTIES & GEOMETRY
        # ==========================================================
        L_real = 2.0 
        beam_len_screen = 6.0 
        
        # Global Layout Scale Matrix (Shifted Down)
        Y_HEADER_MAIN = 5.4
        Y_HEADER_SUB = 5.0
        Y_WATERMARK = 4.4
        
        # Lowered to give the curve plenty of vertical space
        Y_DIAGRAM = 0.4 
        Y_CALC = -3.2
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
        COLOR_SUM_RECT = "#F87171"

        x_diag_start = -beam_len_screen / 2
        max_curve_height = 2.5 

        def sx(x_val):
            return x_diag_start + (x_val / L_real) * beam_len_screen

        def sy(w_val):
            return Y_DIAGRAM + (w_val / 240.0) * max_curve_height

        def fx(x_val):
            return 60 * x_val**2

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

        header_title = Text("SIMULASI PERHITUNGAN BEBAN", color=COLOR_PRIMARY, weight="BOLD").scale(0.35)
        header_sub = Text("BEBAN TERDISTRIBUSI & GAYA RESULTAN", color=COLOR_SECONDARY).scale(0.25)
        
        header_title.move_to([0, Y_HEADER_MAIN, 0])
        header_sub.next_to(header_title, DOWN, buff=0.15)
        self.add(header_title, header_sub)

        watermark = Text("@ScanPintar", color=COLOR_WATERMARK, weight="BOLD").scale(0.30)
        watermark.move_to([0, Y_WATERMARK, 0])
        self.add(watermark)

        # Shifted diagram frame to center=1.8, expanded height=4.8
        diag_frame = create_plot_frame(1.8, "DIAGRAM BENDA BEBAS (FBD)", "#16A34A", height=4.8, width=7.4)
        # Shifted calc frame to center=-3.2, height=4.6
        calc_frame = create_plot_frame(Y_CALC, "LANGKAH INTEGRASI", COLOR_CALC_TITLE, height=4.6, width=7.4)
        self.add(diag_frame, calc_frame)

        # ==========================================================
        # PHASE 2: STATIC DIAGRAM
        # ==========================================================
        def draw_hinge_support(x, y):
            base_line = Line([x-0.15, y-0.3, 0], [x+0.15, y-0.3, 0], color=COLOR_WATERMARK, stroke_width=1.5)
            hash_marks = VGroup(*[Line([x + i*0.06 - 0.03, y-0.3, 0], [x + i*0.06 + 0.03, y-0.36, 0], color=COLOR_WATERMARK) for i in range(-2, 3)])
            clevis_plate = Rectangle(width=0.2, height=0.1, stroke_width=1.5, color=COLOR_TEXT_GEN).next_to(base_line, UP, buff=0.01)
            pin_circle = Circle(radius=0.07, color=COLOR_TEXT_GEN, stroke_width=1.5, fill_opacity=1, fill_color=COLOR_TEXT_GEN).move_to([x, y-0.2, 0])
            return VGroup(base_line, hash_marks, clevis_plate, pin_circle)

        def draw_roller_support(x, y):
            roller_wheels = VGroup(*[Circle(radius=0.06, color=COLOR_TEXT_GEN, stroke_width=1.5) for _ in range(2)]).arrange(RIGHT, buff=0.1).move_to([x, y-0.3, 0])
            top_plate = Rectangle(width=0.25, height=0.05, stroke_width=1.5, color=COLOR_TEXT_GEN).next_to(roller_wheels, UP, buff=0.01)
            fixed_surface = Rectangle(width=0.3, height=0.05, stroke_width=1, color=COLOR_WATERMARK, fill_color=COLOR_WATERMARK, fill_opacity=0.3).next_to(roller_wheels, DOWN, buff=0.01)
            return VGroup(roller_wheels, top_plate, fixed_surface)

        # Beam and Supports
        beam_rect = Rectangle(width=beam_len_screen + 0.4, height=0.2, stroke_color=COLOR_BEAM, stroke_width=2, fill_color=COLOR_BEAM, fill_opacity=0.3).move_to([0, Y_DIAGRAM, 0])
        self.add(beam_rect)
        
        support_O = draw_hinge_support(sx(0), Y_DIAGRAM) 
        support_end = draw_roller_support(sx(2.0), Y_DIAGRAM) 
        self.add(support_O, support_end)

        lbl_O = Text("O", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).next_to(support_O, LEFT, buff=0.1).shift(UP*0.1)
        self.add(lbl_O)

        # Axes
        axis_x = Arrow(start=[sx(0)-0.2, Y_DIAGRAM, 0], end=[sx(2.0)+0.8, Y_DIAGRAM, 0], color=COLOR_TEXT_GEN, stroke_width=2, tip_length=0.15)
        lbl_axis_x = Text("x", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.2).next_to(axis_x, RIGHT, buff=0.1)
        
        axis_w = Arrow(start=[sx(0), Y_DIAGRAM-0.2, 0], end=[sx(0), sy(240)+0.5, 0], color=COLOR_TEXT_GEN, stroke_width=2, tip_length=0.15)
        lbl_axis_w = Text("w", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.2).next_to(axis_w, UP, buff=0.1)
        self.add(axis_x, lbl_axis_x, axis_w, lbl_axis_w)

        # Dimensions
        dim_line_tot = Line([sx(0), Y_DIAGRAM - 0.8, 0], [sx(2.0), Y_DIAGRAM - 0.8, 0], color=COLOR_WATERMARK, stroke_width=1.5)
        for x_tick in [0, 2.0]:
            tick = Line([sx(x_tick), Y_DIAGRAM - 0.8 - 0.08, 0], [sx(x_tick), Y_DIAGRAM - 0.8 + 0.08, 0], color=COLOR_WATERMARK, stroke_width=1.5)
            self.add(tick)
        lbl_tot = Text("2 m", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.18).next_to(dim_line_tot, DOWN, buff=0.1)
        self.add(dim_line_tot, lbl_tot)

        # Distributed Load Curve w = 60x^2
        curve = ParametricFunction(
            lambda t: np.array([sx(t), sy(fx(t)), 0]),
            t_range=[0, 2.0], color=COLOR_FORCE_ARROW, stroke_width=2
        )
        self.play(Create(curve), run_time=1.0)

        lbl_curve = MathTex(r"w(x) = (60 x^2) \text{ N/m}", color=COLOR_TEXT_GEN).scale(0.25).move_to([sx(1.2), sy(fx(1.2)) + 0.4, 0])
        lbl_max = Text("w_max = 240 N/m", color=COLOR_TEXT_GEN).scale(0.2).next_to([sx(2.0), sy(240), 0], UP, buff=0.1)
        
        # ==========================================================
        # PHASE 2.5: RIEMANNIAN SUM & INTEGRATION PROCESS
        # ==========================================================
        riemann_title = Text("SIMULASI PENJUMLAHAN RIEMANN", color=COLOR_PRIMARY).scale(0.25).move_to([0, Y_DIAGRAM + 3.2, 0])
        
        x_calc_start = -7.4 / 2 + 0.3 
        
        # Displaying the calculation method in the bottom frame
        riemann_fh = Text("METODE PENDEKATAN: PENJUMLAHAN RIEMANN", color=COLOR_CALC_TITLE).scale(0.22)
        riemann_fh.move_to([x_calc_start, Y_CALC + 1.6, 0], aligned_edge=LEFT)

        eq_riemann = MathTex(r"F_R \approx \sum_{i=1}^{n} w(x_i) \, \Delta x", color=COLOR_TEXT_GEN).scale(0.4)
        eq_riemann.move_to([x_calc_start + 0.2, Y_CALC + 0.8, 0], aligned_edge=LEFT)

        self.play(
            Write(riemann_title), Write(lbl_curve), Write(lbl_max),
            FadeIn(riemann_fh), Write(eq_riemann), run_time=1.0
        )
        
        def get_manual_riemann_rects(n):
            rects = VGroup()
            dx = 2.0 / n
            rect_w_screen = sx(dx) - sx(0)
            
            for i in range(n):
                x_coord = i * dx
                x_sample = x_coord + dx / 2 
                w_val = fx(x_sample)
                rect_h_screen = sy(w_val) - Y_DIAGRAM - 0.1 
                
                rect = Rectangle(width=rect_w_screen, height=rect_h_screen, 
                                stroke_width=1.5, stroke_color=COLOR_SUM_RECT, 
                                fill_color=COLOR_SUM_RECT, fill_opacity=0.3)
                rect.move_to([sx(x_sample), Y_DIAGRAM + 0.1 + rect_h_screen/2, 0])
                rects.add(rect)
            return rects

        prev_rects = VGroup()
        for n in [4, 8, 16, 32]:
            current_rects = get_manual_riemann_rects(n)
            lbl_n = Text(f"n = {n} Elemen", color=COLOR_SUM_RECT).scale(0.2).move_to([sx(1.0), Y_DIAGRAM + 3.6, 0])
            
            self.play(FadeOut(prev_rects), FadeIn(current_rects), FadeIn(lbl_n), run_time=0.8)
            self.wait(0.8)
            
            if n < 32:
                self.play(FadeOut(lbl_n), run_time=0.2)
                prev_rects = current_rects

        # Convergence Area Polygon
        verts = [np.array([sx(0), Y_DIAGRAM + 0.1, 0]), np.array([sx(2.0), Y_DIAGRAM + 0.1, 0])]
        for t in np.linspace(2.0, 0, 50):
            verts.append(np.array([sx(t), sy(fx(t)), 0]))
            
        final_area_poly = Polygon(*verts, stroke_width=0, fill_color=COLOR_SUM_RECT, fill_opacity=0.4)
        lbl_convergence = Text("Konvergensi ke Gaya Total (F_R)", color=COLOR_BOX_FORCE).scale(0.25).move_to([sx(1.0), Y_DIAGRAM + 3.6, 0])
        
        # Direct transformation from Riemann sum to Definite Integral limit
        eq_limit = MathTex(r"F_R = \lim_{n \to \infty} \sum_{i=1}^n w(x_i) \, \Delta x = \int_0^2 w(x) \, dx", color=COLOR_FORCE_ARROW).scale(0.4)
        eq_limit.move_to([x_calc_start + 0.2, Y_CALC + 0.8, 0], aligned_edge=LEFT)

        self.play(
            FadeOut(lbl_n), FadeIn(lbl_convergence), 
            FadeOut(current_rects), FadeIn(final_area_poly), 
            Transform(eq_riemann, eq_limit), run_time=1.5
        )
        self.wait(2.0)

        # Clear UI elements gracefully to prepare for direct integration steps
        self.play(
            FadeOut(riemann_title), FadeOut(lbl_convergence), FadeOut(lbl_curve), FadeOut(lbl_max),
            FadeOut(riemann_fh), FadeOut(eq_riemann), FadeOut(dim_line_tot), FadeOut(lbl_tot),
            final_area_poly.animate.set_opacity(0.15), run_time=1.2
        )
        self.wait(0.5)

        # ==========================================================
        # PHASE 3: CALCULATION STEPS
        # ==========================================================
        fh1 = Text("1. MAGNITUDO GAYA RESULTAN (F_R)", color=COLOR_CALC_TITLE).scale(0.22)
        fh1.move_to([x_calc_start, Y_CALC + 1.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(fh1), run_time=0.8)

        fr_eq1 = MathTex(r"F_R = \int_A dA = \int_0^2 w \, dx = \int_0^2 (60x^2) \, dx", color=COLOR_TEXT_GEN).scale(0.35)
        fr_eq1.move_to([x_calc_start + 0.2, Y_CALC + 1.0, 0], aligned_edge=LEFT)
        
        fr_eq2 = MathTex(r"F_R = \left[ 20x^3 \right]_0^2 = 20(2)^3 - 20(0)^3", color=COLOR_TEXT_GEN).scale(0.35)
        fr_eq2.move_to([x_calc_start + 0.2, Y_CALC + 0.4, 0], aligned_edge=LEFT)

        fr_val = MathTex(r"F_R = 160 \text{ N}", color=COLOR_BOX_FORCE).scale(0.4)
        fr_val.move_to([x_calc_start + 5.0, Y_CALC + 0.7, 0])
        fr_box = SurroundingRectangle(fr_val, color=COLOR_BOX_FORCE, stroke_width=2)

        self.play(Write(fr_eq1), run_time=1.2)
        self.play(Write(fr_eq2), run_time=1.0)
        self.play(FadeIn(fr_val), Create(fr_box), run_time=0.8)

        fh2 = Text("2. LOKASI GAYA RESULTAN (x̄)", color=COLOR_CALC_TITLE).scale(0.22)
        fh2.move_to([x_calc_start, Y_CALC - 0.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(fh2), run_time=0.8)

        xb_eq1 = MathTex(r"\bar{x} = \frac{\int_A x \, dA}{\int_A dA} = \frac{\int_0^2 x(60x^2) \, dx}{160} = \frac{\int_0^2 60x^3 \, dx}{160}", color=COLOR_TEXT_GEN).scale(0.35)
        xb_eq1.move_to([x_calc_start + 0.2, Y_CALC - 1.0, 0], aligned_edge=LEFT)
        
        xb_eq2 = MathTex(r"\bar{x} = \frac{\left[ 15x^4 \right]_0^2}{160} = \frac{15(16)}{160} = \frac{240}{160}", color=COLOR_TEXT_GEN).scale(0.35)
        xb_eq2.move_to([x_calc_start + 0.2, Y_CALC - 1.6, 0], aligned_edge=LEFT)

        xb_val = MathTex(r"\bar{x} = 1.5 \text{ m}", color=COLOR_BOX_LOC).scale(0.4)
        xb_val.move_to([x_calc_start + 5.0, Y_CALC - 1.3, 0])
        xb_box = SurroundingRectangle(xb_val, color=COLOR_BOX_LOC, stroke_width=2)

        self.play(Write(xb_eq1), run_time=1.5)
        self.play(Write(xb_eq2), run_time=1.2)
        self.play(FadeIn(xb_val), Create(xb_box), run_time=0.8)
        self.wait(1.5)

        # ==========================================================
        # PHASE 4: RESULTANT FORCE EQUIVALENCE ANIMATION
        # ==========================================================
        self.play(
            FadeOut(final_area_poly), 
            curve.animate.set_stroke(opacity=0.1),
            run_time=1.5
        )

        x_bar_real = 1.5
        res_start = [sx(x_bar_real), sy(160), 0] 
        res_end = [sx(x_bar_real), Y_DIAGRAM + 0.1, 0]

        res_arrow = Arrow(start=res_start, end=res_end, color=COLOR_BOX_FORCE, stroke_width=5, tip_length=0.25, buff=0)
        dot_C = Dot(point=res_arrow.get_center(), color=COLOR_TEXT_GEN, radius=0.06)
        lbl_C = Text("C", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.2).next_to(dot_C, RIGHT, buff=0.1)
        res_lbl = MathTex(r"F_R = 160 \text{ N}", color=COLOR_BOX_FORCE).scale(0.3).next_to(res_arrow.get_start(), UP, buff=0.1)

        dim_line_xbar = Line([sx(0), Y_DIAGRAM - 0.4, 0], [sx(x_bar_real), Y_DIAGRAM - 0.4, 0], color=COLOR_BOX_LOC, stroke_width=2)
        tick_xbar = Line([sx(x_bar_real), Y_DIAGRAM - 0.4 - 0.08, 0], [sx(x_bar_real), Y_DIAGRAM - 0.4 + 0.08, 0], color=COLOR_BOX_LOC, stroke_width=2)
        lbl_xbar = MathTex(r"\bar{x} = 1.5 \text{ m}", color=COLOR_BOX_LOC).scale(0.25).next_to(dim_line_xbar, DOWN, buff=0.1)

        self.play(GrowArrow(res_arrow), FadeIn(dot_C), FadeIn(lbl_C), Write(res_lbl), run_time=1.2)
        self.play(Create(dim_line_xbar), FadeIn(tick_xbar), Write(lbl_xbar), run_time=1.0)
        self.wait(3.0)

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
    os.system("manim -pql simulasi_distribusi_beban.py SimulasiDistribusiBeban")