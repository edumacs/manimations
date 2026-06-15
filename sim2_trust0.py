from manim import *
import numpy as np

# ==========================================================
# ADVANCED FINITE ELEMENT MASTERCLASS (FULL SCREEN)
# ==========================================================

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8

class TrussFEAMasterclass(Scene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        # --- HEADER & WATERMARK (FIXED CROPPING) ---
        watermark = Text("@ScanPintar", font_size=24, color="#E11D48", weight="BOLD")
        
        # Split title into two lines and scale to fit mobile frame width safely
        title = MarkupText("<b>SIMULASI ANALISIS</b>\n<b>RANGKA BATANG (FEA)</b>", color="#0F172A")
        title.scale_to_fit_width(6.8)
        
        sub_title = Text("Memahami Alur Kerja Metode Elemen Hingga", font_size=20, color="#334155")
        sub_title.scale_to_fit_width(6.2)
        
        header_group = VGroup(watermark, title, sub_title).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        self.add(header_group)

        # --- BANNER GENERATOR (FIXED OVERLAP) ---
        def create_step_banner(text, color):
            bg = RoundedRectangle(
                corner_radius=0.15, width=7.6, height=0.8,
                fill_color=color, fill_opacity=0.1,
                stroke_color=color, stroke_width=2
            )
            # Ensure banner text fits inside the box
            txt = Text(text, color=color, weight="BOLD", font_size=22)
            if txt.width > 7.0:
                txt.scale_to_fit_width(7.0)
                
            # Moved down to Y=4.3 to avoid colliding with the header
            return VGroup(bg, txt).move_to([0, 4.3, 0])

        # ==========================================================
        # EXACT CENTERED COORDINATE SYSTEM
        # ==========================================================
        n = {
            "A": np.array([-2.75, -1.0, 0.0]),
            "B": np.array([-0.75, -1.0, 0.0]),
            "C": np.array([ 0.75, -1.0, 0.0]),
            "D": np.array([ 2.75, -1.0, 0.0]),
            "E": np.array([ 0.75,  1.0, 0.0]),
            "F": np.array([-0.75,  1.0, 0.0])
        }

        # ==========================================================
        # SCENE 1: PEMODELAN GEOMETRI & BEBAN 
        # ==========================================================
        title1 = create_step_banner("1. PEMODELAN: GEOMETRI, TUMPUAN & BEBAN", "#16A34A")
        self.play(FadeIn(title1))

        # 1a. Draw Nodes
        nodes_vgroup = VGroup(*[Dot(pos, color="#0F172A", radius=0.08) for pos in n.values()])
        node_labels = VGroup(*[Text(key, color="#1E293B", font_size=28, weight="BOLD").next_to(pos, UP+RIGHT, buff=0.05) for key, pos in n.items()])
        
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in nodes_vgroup], lag_ratio=0.1))
        self.play(FadeIn(node_labels))

        # 1b. Draw Elements
        lines_def = [
            ("A", "B"), ("B", "C"), ("C", "D"),
            ("B", "F"), ("C", "E"), ("F", "E"),
            ("A", "F"), ("B", "E"), ("E", "D")
        ]
        elements = VGroup()
        line_dict = {}
        for start, end in lines_def:
            l = Line(n[start], n[end], color="#94A3B8", stroke_width=5)
            elements.add(l)
            line_dict[f"{start}{end}"] = l
        
        self.play(LaggedStart(*[Create(line) for line in elements], lag_ratio=0.15), run_time=2)

        # 1c. Draw Supports
        supA = Triangle(color="#0284C7", fill_color="#0284C7", fill_opacity=1).scale(0.2).move_to(n["A"] + DOWN*0.2, aligned_edge=UP)
        supD = Triangle(color="#0284C7", fill_color="#0284C7", fill_opacity=1).scale(0.2).move_to(n["D"] + DOWN*0.2, aligned_edge=UP)
        rollerD = Circle(color="#0284C7", radius=0.06).move_to(n["D"]+DOWN*0.35, aligned_edge=UP)
        
        supA_label = Text("Pin (Engsel)", font_size=16, color="#0284C7").next_to(supA, DOWN)
        supD_label = Text("Roller (Rol)", font_size=16, color="#0284C7").next_to(rollerD, DOWN)
        supports = VGroup(supA, supD, rollerD, supA_label, supD_label)

        self.play(FadeIn(supports, shift=UP*0.5))

        # 1d. Add Loads & Dimensions
        arr_B = Arrow(start=n["B"]+UP*1.5, end=n["B"], color="#E11D48", stroke_width=6, buff=0.1)
        txt_B = Text("11 kN", color="#E11D48", font_size=24, weight="BOLD").next_to(arr_B, UP, buff=0.1)
        
        arr_C = Arrow(start=n["C"]+UP*1.5, end=n["C"], color="#E11D48", stroke_width=6, buff=0.1)
        txt_C = Text("22 kN", color="#E11D48", font_size=24, weight="BOLD").next_to(arr_C, UP, buff=0.1)
        loads = VGroup(arr_B, txt_B, arr_C, txt_C)

        dim_arr = DoubleArrow(start=n["A"]+DOWN*1.2, end=n["D"]+DOWN*1.2, color="#64748B", buff=0)
        dim_txt = Text("Total L = 5.5 m", color="#64748B", font_size=20).next_to(dim_arr, DOWN, buff=0.1)
        dims = VGroup(dim_arr, dim_txt)

        self.play(GrowArrow(arr_B), FadeIn(txt_B), GrowArrow(arr_C), FadeIn(txt_C))
        self.play(FadeIn(dims))
        self.wait(1.5)

        # Scale down geometry for next steps
        truss_system = VGroup(nodes_vgroup, node_labels, elements, supports, loads, dims)
        self.play(FadeOut(title1))
        self.play(truss_system.animate.scale(0.65).move_to([0, 2.5, 0]))

        # ==========================================================
        # SCENE 2: MATRIKS ELEMEN & PERAKITAN GLOBAL
        # ==========================================================
        title2 = create_step_banner("2. DISKRITISASI & MATRIKS GLOBAL", "#0284C7")
        self.play(FadeIn(title2))

        k_formula_title = Text("Matriks Kekakuan Elemen Lokal:", font_size=20, color="#64748B").move_to([0, 0.2, 0])
        
        k_math = MathTex(
            r"k^{e} = \frac{EA}{L}",
            r"\begin{bmatrix} c^2 & cs & -c^2 & -cs \\ cs & s^2 & -cs & -s^2 \\ -c^2 & -cs & c^2 & cs \\ -cs & -s^2 & cs & s^2 \end{bmatrix}"
        ).scale(0.85).next_to(k_formula_title, DOWN, buff=0.3)
        k_math[0].set_color("#0284C7")
        
        local_group = VGroup(k_formula_title, k_math)

        self.play(FadeIn(local_group, shift=UP*0.2))
        self.play(elements[0].animate.set_color("#0284C7").set_stroke(width=8))
        self.wait(1.5)
        self.play(elements[0].animate.set_color("#94A3B8").set_stroke(width=5))
        self.play(FadeOut(local_group))

        assembly_title = Text("Perakitan Sistem Global: K u = F", font_size=24, color="#0F172A", weight="BOLD").move_to([0, 0.5, 0])
        
        global_eq = MathTex(
            r"\begin{bmatrix} K_{1,1} & \cdots & K_{1,12} \\ \vdots & \ddots & \vdots \\ K_{12,1} & \cdots & K_{12,12} \end{bmatrix}",
            r"\begin{bmatrix} u_{Ax} \\ u_{Ay} \\ \vdots \\ u_{Fy} \end{bmatrix}",
            r"=",
            r"\begin{bmatrix} F_{Ax} \\ F_{Ay} \\ \vdots \\ F_{Fy} \end{bmatrix}"
        ).scale(0.9).next_to(assembly_title, DOWN, buff=0.4)
        
        global_eq[0].set_color("#0284C7") 
        global_eq[1].set_color("#16A34A") 
        global_eq[3].set_color("#E11D48") 

        self.play(Write(assembly_title))
        self.play(FadeIn(global_eq))
        self.wait(1.5)
        self.play(FadeOut(title2), FadeOut(assembly_title))

        # ==========================================================
        # SCENE 3: SYARAT BATAS (BOUNDARY CONDITIONS)
        # ==========================================================
        title3 = create_step_banner("3. SYARAT BATAS (BOUNDARY CONDITIONS)", "#BE185D")
        self.play(FadeIn(title3))

        bc_desc = Text("Tumpuan dimasukkan untuk menghindari matriks singular.", font_size=18, color="#64748B").move_to([0, 0.8, 0])
        self.play(FadeIn(bc_desc))

        global_eq_bc = MathTex(
            r"\begin{bmatrix} K_{1,1} & \cdots & K_{1,12} \\ \vdots & \ddots & \vdots \\ K_{12,1} & \cdots & K_{12,12} \end{bmatrix}",
            r"\begin{bmatrix} \mathbf{0} \\ \mathbf{0} \\ \vdots \\ u_{Fy} \end{bmatrix}",
            r"=",
            r"\begin{bmatrix} F_{Ax} \\ F_{Ay} \\ \vdots \\ F_{Fy} \end{bmatrix}"
        ).scale(0.9).move_to(global_eq.get_center())
        
        global_eq_bc[0].set_color("#0284C7") 
        global_eq_bc[1].set_color("#16A34A") 
        global_eq_bc[1][0][1:3].set_color("#BE185D") 
        global_eq_bc[3].set_color("#E11D48") 

        self.play(Flash(supA, color="#BE185D", line_length=0.3), Flash(rollerD, color="#BE185D", line_length=0.3))
        self.play(Transform(global_eq, global_eq_bc))
        
        strike1 = Line(global_eq[0].get_left() + UP*0.6, global_eq[3].get_right() + UP*0.6, color="#BE185D", stroke_width=4)
        strike2 = Line(global_eq[0].get_top() + LEFT*0.8, global_eq[0].get_bottom() + LEFT*0.8, color="#BE185D", stroke_width=4)
        
        self.play(Create(strike1), Create(strike2))
        self.wait(1.5)

        self.play(
            FadeOut(title3), FadeOut(bc_desc), FadeOut(global_eq), 
            FadeOut(strike1), FadeOut(strike2)
        )

        # ==========================================================
        # SCENE 4: PENYELESAIAN & GAYA DALAM (WITH ACTUAL MATH)
        # ==========================================================
        title4 = create_step_banner("4. SOLUSI: DISPLACEMENT & GAYA DALAM", "#D97706")
        self.play(FadeIn(title4))

        solve_math = MathTex(
            r"\{\mathbf{u}_{unknown}\} = [\mathbf{K}_{reduced}]^{-1} \{\mathbf{F}_{known}\}"
        ).scale(1.1).move_to([0, -0.5, 0])
        solve_math.set_color_by_tex("u", "#16A34A").set_color_by_tex("K", "#0284C7").set_color_by_tex("F", "#E11D48")
        
        self.play(Write(solve_math))
        self.wait(1.5)
        self.play(FadeOut(solve_math))

        # Restore Truss
        self.play(truss_system.animate.scale(1/0.65).move_to([0, 1.2, 0]))
        self.play(FadeOut(dims), FadeOut(loads))

        # Setup Legend
        legend_group = VGroup(
            VGroup(Dot(color="#0284C7", radius=0.1), Text("Compression (-) / Tekan", font_size=20, color="#0284C7")).arrange(RIGHT),
            VGroup(Dot(color="#E11D48", radius=0.1), Text("Tension (+) / Tarik", font_size=20, color="#E11D48")).arrange(RIGHT),
            VGroup(Arrow(start=DOWN*0.5, end=ORIGIN, color="#16A34A", buff=0), Text("Reactions / Reaksi", font_size=20, color="#16A34A")).arrange(RIGHT)
        ).arrange(DOWN, aligned_edge=LEFT).move_to([0, -2.5, 0])
        
        self.play(FadeIn(legend_group))

        # Engineering Physics Corrected Results: 
        # CE is Tension (+22), BE is Compression (-5)
        comp_keys = ["AF", "FE", "ED", "BE"] 
        tens_keys = ["AB", "BC", "CD", "BF", "CE"]
        
        # Color the members
        self.play(
            *[line_dict[k].animate.set_color("#0284C7").set_stroke(width=10) for k in comp_keys],
            *[line_dict[k].animate.set_color("#E11D48").set_stroke(width=10) for k in tens_keys],
            run_time=1.5
        )

        # Actual Calculated Forces dictionary (kN)
        forces = {
            "AB": 15.0, "BC": 18.0, "CD": 18.0, "BF": 15.0, "CE": 22.0, 
            "AF": -21.2, "FE": -15.0, "ED": -25.5, "BE": -5.0 
        }

        # Create dynamically aligned text blocks for each structural member
        force_labels = VGroup()
        for key, val in forces.items():
            line = line_dict[key]
            color = "#E11D48" if val > 0 else "#0284C7"
            sign = "+" if val > 0 else ""
            
            # Formatting the text and placing a small white box behind it for legibility
            txt = Text(f"{sign}{val}", font_size=16, color=color, weight="BOLD")
            bg = BackgroundRectangle(txt, color=WHITE, fill_opacity=0.9, buff=0.05)
            lbl = VGroup(bg, txt).move_to(line.get_center())
            force_labels.add(lbl)

        self.play(FadeIn(force_labels))

        # Add Computed Reaction Forces (15 kN and 18 kN)
        RA_post = Arrow(start=n["A"]+DOWN*1.2, end=n["A"]+DOWN*0.2, color="#16A34A", stroke_width=8, buff=0)
        RD_post = Arrow(start=n["D"]+DOWN*1.2, end=n["D"]+DOWN*0.2, color="#16A34A", stroke_width=8, buff=0)
        
        txt_RA = Text("15 kN", color="#16A34A", font_size=20, weight="BOLD").next_to(RA_post, RIGHT, buff=0.1)
        txt_RD = Text("18 kN", color="#16A34A", font_size=20, weight="BOLD").next_to(RD_post, RIGHT, buff=0.1)

        self.play(GrowArrow(RA_post), GrowArrow(RD_post))
        self.play(FadeIn(txt_RA), FadeIn(txt_RD))
        self.play(Flash(n["A"], color="#16A34A", line_length=0.5), Flash(n["D"], color="#16A34A", line_length=0.5))
        
        self.wait(4)

        # ==========================================================
        # OUTRO SEQUENCE
        # ==========================================================
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.0)
        self.clear() 

        closing_primary = Text("Simpan untuk belajar FEA!", color="#0369A1", weight="BOLD").scale(1.0)
        closing_secondary = Text("Ikuti @ScanPintar", color="#BE123C", weight="BOLD").scale(0.8)
        outro_group = VGroup(closing_primary, closing_secondary).arrange(DOWN, buff=0.6)

        self.play(Write(outro_group), run_time=1.5)
        self.wait(2.5)