from manim import *
import numpy as np

# ==========================================================
# ADVANCED STRUCTURAL ANALYSIS PLATFORM ENGINE 
# (MOMENT OF A FORCE - 5 METHODS)
# ==========================================================

# portrait 9:16 aspect ratio
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8

class SimulasiMomenGaya(Scene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        # ==========================================================
        # STRUCTURAL PROPERTIES & GEOMETRY SCALING
        # ==========================================================
        # Scale for screen
        s = 0.6 
        
        # Origin point (O) in screen coordinates
        O_x = -1.5
        O_y = 0.0
        O_screen = np.array([O_x, O_y, 0])
        
        # Point A coordinates (2m right, 4m up from O)
        A_x = O_x + 2 * s
        A_y = O_y + 4 * s
        A_screen = np.array([A_x, A_y, 0])

        # Force direction & components
        rad = 40 * np.pi / 180
        u_hat = np.array([np.cos(-rad), np.sin(-rad), 0]) # Direction of force
        n_hat = np.array([np.sin(rad), np.cos(rad), 0])   # Normal to force
        
        # Global Layout Scale Matrix
        Y_HEADER_MAIN = 5.4
        Y_HEADER_SUB = 5.0
        Y_WATERMARK = 4.4
        
        Y_DIAGRAM = 1.8 
        Y_CALC = -3.2
        Y_CLOSING = -5.8
        
        # Color Palette
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
        COLOR_DIM = "#94A3B8"

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

        header_title = Text("SIMULASI STATIKA STRUKTUR", color=COLOR_PRIMARY, weight="BOLD").scale(0.35)
        header_sub = Text("5 METODE PERHITUNGAN MOMEN GAYA", color=COLOR_SECONDARY).scale(0.25)
        
        header_title.move_to([0, Y_HEADER_MAIN, 0])
        header_sub.next_to(header_title, DOWN, buff=0.15)
        self.add(header_title, header_sub)

        watermark = Text("@ScanPintar", color=COLOR_WATERMARK, weight="BOLD").scale(0.30)
        watermark.move_to([0, Y_WATERMARK, 0])
        self.add(watermark)

        diag_frame = create_plot_frame(Y_DIAGRAM, "DIAGRAM BENDA BEBAS (FBD)", "#16A34A", height=5.0, width=7.4)
        calc_frame = create_plot_frame(Y_CALC, "LANGKAH PENYELESAIAN", COLOR_CALC_TITLE, height=4.6, width=7.4)
        self.add(diag_frame, calc_frame)

        # ==========================================================
        # PHASE 2: STATIC DIAGRAM (STRUCTURE BASE)
        # ==========================================================
        # Structure Body
        post = Line(O_screen, [O_x, A_y, 0], stroke_color=COLOR_BEAM, stroke_width=8)
        arm = Line([O_x, A_y, 0], A_screen, stroke_color=COLOR_BEAM, stroke_width=8)
        joint_O = Circle(radius=0.08, color=COLOR_TEXT_GEN, fill_opacity=1).move_to(O_screen)
        joint_A = Circle(radius=0.06, color=COLOR_BEAM, fill_opacity=1).move_to(A_screen)
        
        base_support = Rectangle(width=0.8, height=0.1, color=COLOR_WATERMARK, fill_opacity=1).next_to(joint_O, DOWN, buff=0.02)
        
        self.add(post, arm, joint_O, joint_A, base_support)

        # Labels
        lbl_O = Text("O", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.25).next_to(joint_O, LEFT, buff=0.2)
        lbl_A = Text("A", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.25).next_to(joint_A, UP, buff=0.1)
        self.add(lbl_O, lbl_A)

        # Main Force
        F_length = 1.6
        F_end = A_screen + F_length * u_hat
        force_arrow = Arrow(A_screen, F_end, color=COLOR_FORCE_ARROW, buff=0, stroke_width=4, tip_length=0.2)
        lbl_F = MathTex(r"600 \text{ N}", color=COLOR_FORCE_ARROW).scale(0.3).next_to(F_end, RIGHT, buff=0.1)
        
        # Dimensions
        dim_y = DoubleArrow([O_x - 0.4, O_y, 0], [O_x - 0.4, A_y, 0], color=COLOR_DIM, buff=0, tip_length=0.1, stroke_width=2)
        lbl_dim_y = Text("4 m", color=COLOR_TEXT_GEN).scale(0.2).next_to(dim_y, LEFT, buff=0.1)
        
        dim_x = DoubleArrow([O_x, A_y + 0.4, 0], [A_x, A_y + 0.4, 0], color=COLOR_DIM, buff=0, tip_length=0.1, stroke_width=2)
        lbl_dim_x = Text("2 m", color=COLOR_TEXT_GEN).scale(0.2).next_to(dim_x, UP, buff=0.1)

        ref_line = DashedLine(A_screen, A_screen + [1, 0, 0], color=COLOR_DIM)
        angle_arc = Arc(radius=0.5, start_angle=0, angle=-rad, arc_center=A_screen, color=COLOR_DIM)
        lbl_angle = MathTex(r"40^\circ", color=COLOR_TEXT_GEN).scale(0.25).next_to(angle_arc, RIGHT, buff=0.05).shift(UP*0.05)

        self.play(Create(dim_y), Write(lbl_dim_y), Create(dim_x), Write(lbl_dim_x), run_time=1)
        self.play(GrowArrow(force_arrow), Write(lbl_F), Create(ref_line), Create(angle_arc), Write(lbl_angle), run_time=1.5)
        self.wait(0.5)

        x_calc_start = -7.4 / 2 + 0.3 
        
        # ==========================================================
        # PHASE 3: CALCULATION METHODS (1 TO 5)
        # ==========================================================
        
        # --- METHOD I: MOMENT ARM d ---
        title_m1 = Text("(I) Menggunakan Lengan Momen (d)", color=COLOR_CALC_TITLE).scale(0.22).move_to([x_calc_start, Y_CALC + 1.6, 0], aligned_edge=LEFT)
        
        # Geometry for Method 1
        loa_start = A_screen - 1.5 * u_hat
        loa_end = A_screen + 3.0 * u_hat
        line_of_action = DashedLine(loa_start, loa_end, color=COLOR_DIM, stroke_width=1.5)
        
        d_screen_val = 4.35 * s
        P_screen = O_screen + d_screen_val * n_hat
        d_line = Line(O_screen, P_screen, color=COLOR_BOX_FORCE, stroke_width=3)
        lbl_d = MathTex(r"d", color=COLOR_BOX_FORCE).scale(0.3).next_to(d_line.get_center(), UP, buff=0.1)

        # Equations for Method 1
        eq1_1 = MathTex(r"d = 4 \cos 40^\circ + 2 \sin 40^\circ = 4.35 \text{ m}", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 0.8, 0], aligned_edge=LEFT)
        eq1_2 = MathTex(r"M_O = F \cdot d = 600(4.35)", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 0.2, 0], aligned_edge=LEFT)
        res_box = MathTex(r"M_O = 2610 \text{ N}\cdot\text{m} \text{ (CW)}", color=COLOR_BOX_FORCE).scale(0.4).move_to([x_calc_start + 3.5, Y_CALC - 0.6, 0])
        box_outline = SurroundingRectangle(res_box, color=COLOR_BOX_FORCE, stroke_width=2)

        method1_group_geom = VGroup(line_of_action, d_line, lbl_d)
        method1_group_calc = VGroup(title_m1, eq1_1, eq1_2, res_box, box_outline)

        self.play(FadeIn(title_m1), Create(line_of_action), run_time=0.8)
        self.play(Create(d_line), Write(lbl_d), Write(eq1_1), run_time=1)
        self.play(Write(eq1_2), run_time=0.8)
        self.play(FadeIn(res_box), Create(box_outline), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(method1_group_geom), FadeOut(method1_group_calc), run_time=0.8)

        # --- METHOD II: VARIGNON'S THEOREM AT A ---
        title_m2 = Text("(II) Teorema Varignon (Komponen di A)", color=COLOR_CALC_TITLE).scale(0.22).move_to([x_calc_start, Y_CALC + 1.6, 0], aligned_edge=LEFT)

        # Geometry for Method 2
        F1_vec = Arrow(A_screen, A_screen + [F_length * np.cos(rad), 0, 0], color=COLOR_SECONDARY, buff=0, stroke_width=4, tip_length=0.2)
        F2_vec = Arrow(A_screen, A_screen + [0, -F_length * np.sin(rad), 0], color=COLOR_SECONDARY, buff=0, stroke_width=4, tip_length=0.2)
        lbl_F1 = MathTex(r"F_1", color=COLOR_SECONDARY).scale(0.3).next_to(F1_vec, UP, buff=0.05)
        lbl_F2 = MathTex(r"F_2", color=COLOR_SECONDARY).scale(0.3).next_to(F2_vec, LEFT, buff=0.05)
        
        proj_F1 = DashedLine(A_screen, [O_x, A_y, 0], color=COLOR_SECONDARY, stroke_width=1.5)
        proj_F2 = DashedLine(A_screen, [A_x, O_y, 0], color=COLOR_SECONDARY, stroke_width=1.5)

        # Equations for Method 2
        eq2_1 = MathTex(r"F_1 = 600 \cos 40^\circ = 460 \text{ N}", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 1.0, 0], aligned_edge=LEFT)
        eq2_2 = MathTex(r"F_2 = 600 \sin 40^\circ = 386 \text{ N}", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 4.0, Y_CALC + 1.0, 0], aligned_edge=LEFT)
        eq2_3 = MathTex(r"M_O = F_1(4) + F_2(2) = 460(4) + 386(2)", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 0.2, 0], aligned_edge=LEFT)

        method2_group_geom = VGroup(F1_vec, F2_vec, lbl_F1, lbl_F2, proj_F1, proj_F2)
        method2_group_calc = VGroup(title_m2, eq2_1, eq2_2, eq2_3)

        self.play(FadeIn(title_m2), FadeOut(force_arrow), FadeOut(lbl_F), run_time=0.8)
        self.play(GrowArrow(F1_vec), GrowArrow(F2_vec), Write(lbl_F1), Write(lbl_F2), run_time=1)
        self.play(Write(eq2_1), Write(eq2_2), Create(proj_F1), Create(proj_F2), run_time=1)
        self.play(Write(eq2_3), run_time=0.8)
        self.play(FadeIn(res_box), FadeIn(box_outline), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(method2_group_geom), FadeOut(method2_group_calc), FadeOut(res_box), FadeOut(box_outline), run_time=0.8)

        # --- METHOD III: TRANSMISSIBILITY TO B ---
        title_m3 = Text("(III) Prinsip Transmisibilitas (Geser ke Titik B)", color=COLOR_CALC_TITLE).scale(0.22).move_to([x_calc_start, Y_CALC + 1.6, 0], aligned_edge=LEFT)
        
        # Geometry for Method 3
        t_B = -1.566
        B_screen = A_screen + t_B * u_hat
        dot_B = Circle(radius=0.06, color=COLOR_FORCE_ARROW, fill_opacity=1).move_to(B_screen)
        lbl_B = Text("B", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.25).next_to(dot_B, LEFT, buff=0.1)
        
        F_at_B = Arrow(B_screen, B_screen + F_length * u_hat, color=COLOR_FORCE_ARROW, buff=0, stroke_width=4, tip_length=0.2)
        F1_at_B = Arrow(B_screen, B_screen + [F_length * np.cos(rad), 0, 0], color=COLOR_SECONDARY, buff=0, stroke_width=4, tip_length=0.2)
        
        line_extend_y = DashedLine([O_x, A_y, 0], B_screen, color=COLOR_BEAM, stroke_width=2)
        
        # Equations for Method 3
        eq3_1 = MathTex(r"d_1 = 4 + 2 \tan 40^\circ = 5.68 \text{ m}", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 0.8, 0], aligned_edge=LEFT)
        eq3_2 = MathTex(r"M_O = F_1(d_1) = 460(5.68)", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 0.2, 0], aligned_edge=LEFT)

        method3_group_geom = VGroup(dot_B, lbl_B, F_at_B, F1_at_B, line_extend_y, line_of_action)
        method3_group_calc = VGroup(title_m3, eq3_1, eq3_2)

        self.play(FadeIn(title_m3), FadeIn(force_arrow), Create(line_of_action), run_time=0.8)
        self.play(force_arrow.animate.move_to(F_at_B.get_center()), Create(line_extend_y), FadeIn(dot_B), Write(lbl_B), run_time=1.2)
        self.play(GrowArrow(F1_at_B), Write(eq3_1), run_time=1)
        self.play(Write(eq3_2), run_time=0.8)
        self.play(FadeIn(res_box), FadeIn(box_outline), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(method3_group_geom), FadeOut(method3_group_calc), FadeOut(res_box), FadeOut(box_outline), FadeOut(force_arrow), run_time=0.8)

        # --- METHOD IV: TRANSMISSIBILITY TO C ---
        title_m4 = Text("(IV) Prinsip Transmisibilitas (Geser ke Titik C)", color=COLOR_CALC_TITLE).scale(0.22).move_to([x_calc_start, Y_CALC + 1.6, 0], aligned_edge=LEFT)
        
        # Geometry for Method 4
        t_C = 3.732
        C_screen = A_screen + t_C * u_hat
        dot_C = Circle(radius=0.06, color=COLOR_FORCE_ARROW, fill_opacity=1).move_to(C_screen)
        lbl_C = Text("C", color=COLOR_TEXT_GEN, weight="BOLD").scale(0.25).next_to(dot_C, UP, buff=0.1)
        
        F_at_C = Arrow(C_screen, C_screen + F_length * u_hat, color=COLOR_FORCE_ARROW, buff=0, stroke_width=4, tip_length=0.2)
        F2_at_C = Arrow(C_screen, C_screen + [0, -F_length * np.sin(rad), 0], color=COLOR_SECONDARY, buff=0, stroke_width=4, tip_length=0.2)
        
        line_extend_x = DashedLine(O_screen, C_screen, color=COLOR_BEAM, stroke_width=2)

        # Equations for Method 4
        eq4_1 = MathTex(r"d_2 = 2 + 4 \cot 40^\circ = 6.77 \text{ m}", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 0.8, 0], aligned_edge=LEFT)
        eq4_2 = MathTex(r"M_O = F_2(d_2) = 386(6.77)", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 0.2, 0], aligned_edge=LEFT)

        method4_group_geom = VGroup(dot_C, lbl_C, F_at_C, F2_at_C, line_extend_x, line_of_action)
        method4_group_calc = VGroup(title_m4, eq4_1, eq4_2)

        force_arrow.move_to(A_screen + (F_length/2)*u_hat) # Reset F arrow position silently

        self.play(FadeIn(title_m4), FadeIn(force_arrow), Create(line_of_action), run_time=0.8)
        self.play(force_arrow.animate.move_to(F_at_C.get_center()), Create(line_extend_x), FadeIn(dot_C), Write(lbl_C), run_time=1.2)
        self.play(GrowArrow(F2_at_C), Write(eq4_1), run_time=1)
        self.play(Write(eq4_2), run_time=0.8)
        self.play(FadeIn(res_box), FadeIn(box_outline), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(method4_group_geom), FadeOut(method4_group_calc), FadeOut(res_box), FadeOut(box_outline), FadeOut(force_arrow), run_time=0.8)

        # --- METHOD V: VECTOR CROSS PRODUCT ---
        title_m5 = Text("(V) Formulasi Vektor (Cross Product)", color=COLOR_CALC_TITLE).scale(0.22).move_to([x_calc_start, Y_CALC + 1.6, 0], aligned_edge=LEFT)
        
        # Geometry for Method 5
        force_arrow.move_to(A_screen + (F_length/2)*u_hat)
        r_vec = Arrow(O_screen, A_screen, color=COLOR_PRIMARY, buff=0, stroke_width=4, tip_length=0.2)
        lbl_r = MathTex(r"\mathbf{r}", color=COLOR_PRIMARY).scale(0.35).next_to(r_vec.get_center(), LEFT, buff=0.1)

        # Equations for Method 5
        eq5_1 = MathTex(r"\mathbf{r} = 2\mathbf{i} + 4\mathbf{j}", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 0.9, 0], aligned_edge=LEFT)
        eq5_2 = MathTex(r"\mathbf{F} = 600(\cos 40^\circ \mathbf{i} - \sin 40^\circ \mathbf{j}) = 460\mathbf{i} - 386\mathbf{j}", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC + 0.3, 0], aligned_edge=LEFT)
        eq5_3 = MathTex(r"\mathbf{M}_O = \mathbf{r} \times \mathbf{F} = (2\mathbf{i} + 4\mathbf{j}) \times (460\mathbf{i} - 386\mathbf{j})", color=COLOR_TEXT_GEN).scale(0.35).move_to([x_calc_start + 0.2, Y_CALC - 0.3, 0], aligned_edge=LEFT)
        res_box_vec = MathTex(r"\mathbf{M}_O = -2610\mathbf{k} \text{ N}\cdot\text{m}", color=COLOR_BOX_FORCE).scale(0.4).move_to([x_calc_start + 4.5, Y_CALC - 0.9, 0])
        box_outline_vec = SurroundingRectangle(res_box_vec, color=COLOR_BOX_FORCE, stroke_width=2)

        method5_group_geom = VGroup(r_vec, lbl_r)
        method5_group_calc = VGroup(title_m5, eq5_1, eq5_2, eq5_3, res_box_vec, box_outline_vec)

        self.play(FadeIn(title_m5), FadeIn(force_arrow), FadeIn(lbl_F), run_time=0.8)
        self.play(GrowArrow(r_vec), Write(lbl_r), Write(eq5_1), run_time=1)
        self.play(Write(eq5_2), run_time=0.8)
        self.play(Write(eq5_3), run_time=0.8)
        self.play(FadeIn(res_box_vec), Create(box_outline_vec), run_time=0.8)
        self.wait(3)

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
    os.system("manim -pql simulasi_momen_gaya.py SimulasiMomenGaya")