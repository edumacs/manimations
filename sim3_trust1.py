from manim import *
import numpy as np

# ==========================================================
# ADVANCED FINITE ELEMENT MASTERCLASS (VERTICAL / MOBILE)
# ==========================================================

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8

class TrussFEAMasterclass(Scene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        # --- HEADER & WATERMARK ---
        watermark = Text("@ScanPintar", font_size=24, color="#E11D48", weight="BOLD")
        
        title = MarkupText("<b>SIMULASI ANALISIS</b>\n<b>RANGKA BATANG (FEA)</b>", color="#0F172A")
        title.scale_to_fit_width(6.8)
        
        sub_title = Text("Memahami Alur Kerja Metode Elemen Hingga", font_size=20, color="#334155")
        sub_title.scale_to_fit_width(6.2)
        
        header_group = VGroup(watermark, title, sub_title).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        self.add(header_group)

        # --- BANNER GENERATOR ---
        def create_step_banner(text, color):
            bg = RoundedRectangle(
                corner_radius=0.15, width=7.6, height=0.8,
                fill_color=color, fill_opacity=0.1,
                stroke_color=color, stroke_width=2
            )
            txt = Text(text, color=color, weight="BOLD", font_size=22)
            if txt.width > 7.0:
                txt.scale_to_fit_width(7.0)
            return VGroup(bg, txt).move_to([0, 3.6, 0])

        # ==========================================================
        # EXACT COORDINATE SYSTEM (BASED ON ATTACHED IMAGE)
        # ==========================================================
        base_y = -2.0
        n = {
            "A": np.array([-3.0, base_y, 0.0]),
            "B": np.array([-1.5, base_y, 0.0]),
            "C": np.array([ 0.0, base_y, 0.0]),
            "D": np.array([ 1.5, base_y, 0.0]),
            "E": np.array([ 3.0, base_y, 0.0]),
            "H": np.array([-1.5, base_y + 1.0, 0.0]),
            "G": np.array([ 0.0, base_y + 2.0, 0.0]),
            "J": np.array([ 1.5, base_y + 1.0, 0.0])
        }

        # ==========================================================
        # SCENE 1: PEMODELAN GEOMETRI & BEBAN 
        # ==========================================================
        title1 = create_step_banner("1. PEMODELAN: GEOMETRI, TUMPUAN & BEBAN", "#16A34A")
        self.play(FadeIn(title1))

        # 1a. Draw Nodes
        nodes_vgroup = VGroup(*[Dot(pos, color="#0F172A", radius=0.08) for pos in n.values()])
        node_labels = VGroup(*[Text(key, color="#1E293B", font_size=28, weight="BOLD").next_to(pos, LEFT if key in ["A", "H"] else RIGHT, buff=0.1) for key, pos in n.items()])
        
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in nodes_vgroup], lag_ratio=0.1))
        self.play(FadeIn(node_labels))

        # 1b. Draw Elements
        lines_def = [
            ("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), # Bottom Chord
            ("A", "H"), ("H", "G"), ("G", "J"), ("J", "E"), # Top Chord
            ("H", "B"), ("G", "C"), ("J", "D"),             # Verticals
            ("H", "C"), ("J", "C")                          # Diagonals
        ]
        
        elements = VGroup()
        line_dict = {}
        for start, end in lines_def:
            l = Line(n[start], n[end], color="#94A3B8", stroke_width=5)
            elements.add(l)
            line_dict[f"{start}{end}"] = l
        
        self.play(LaggedStart(*[Create(line) for line in elements], lag_ratio=0.1), run_time=2)

        # 1c. Draw Supports
        supA = Triangle(color="#0284C7", fill_color="#0284C7", fill_opacity=1).scale(0.2).move_to(n["A"] + DOWN*0.2, aligned_edge=UP)
        supE = Triangle(color="#0284C7", fill_color="#0284C7", fill_opacity=1).scale(0.2).move_to(n["E"] + DOWN*0.2, aligned_edge=UP)
        rollerE = Circle(color="#0284C7", radius=0.06).move_to(n["E"]+DOWN*0.35, aligned_edge=UP)
        
        supA_label = Text("Pin", font_size=16, color="#0284C7").next_to(supA, DOWN)
        supE_label = Text("Roller", font_size=16, color="#0284C7").next_to(rollerE, DOWN)
        supports = VGroup(supA, supE, rollerE, supA_label, supE_label)

        self.play(FadeIn(supports, shift=UP*0.5))

        # 1d. Add Loads
        load_data = [("A", "4 kN"), ("H", "6 kN"), ("G", "12 kN"), ("J", "9 kN"), ("E", "6 kN")]
        loads = VGroup()
        for node_key, mag in load_data:
            start_pos = n[node_key] + UP*1.0
            end_pos = n[node_key] + UP*0.1
            arr = Arrow(start=start_pos, end=end_pos, color="#E11D48", stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.2)
            txt = Text(mag, color="#E11D48", font_size=20, weight="BOLD").next_to(arr, UP, buff=0.1)
            loads.add(VGroup(arr, txt))

        # Build Detailed Dimensions
        dim_color = "#64748B"
        dims = VGroup()
        
        dim_y = base_y - 1.2
        spans = [("A", "B", "1.5 m"), ("B", "C", "1.5 m"), ("C", "D", "1.5 m"), ("D", "E", "1.5 m")]
        for start, end, label in spans:
            w1 = Line(n[start]+DOWN*0.6, [n[start][0], dim_y - 0.2, 0], color=dim_color, stroke_width=2)
            w2 = Line(n[end]+DOWN*0.6, [n[end][0], dim_y - 0.2, 0], color=dim_color, stroke_width=2)
            arr = DoubleArrow(start=[n[start][0], dim_y, 0], end=[n[end][0], dim_y, 0], color=dim_color, buff=0, stroke_width=3)
            txt = Text(label, color=dim_color, font_size=16).next_to(arr, DOWN, buff=0.1)
            dims.add(w1, w2, arr, txt)

        v_labels = [("H", "B", "1 m"), ("G", "C", "2 m"), ("J", "D", "1 m")]
        for top, bot, label in v_labels:
            txt = Text(label, color=dim_color, font_size=16).next_to(line_dict[f"{top}{bot}"], RIGHT, buff=0.1)
            dims.add(txt)

        self.play(FadeIn(loads, shift=DOWN*0.3))
        self.play(FadeIn(dims))
        self.wait(1.5)

        # OVERLAP FIX: Move scaled truss significantly higher and scale slightly smaller
        truss_system = VGroup(nodes_vgroup, node_labels, elements, supports, loads, dims)
        self.play(FadeOut(title1))
        self.play(truss_system.animate.scale(0.55).move_to([0, 2.0, 0]))

        # ==========================================================
        # SCENE 2: MATRIKS ELEMEN & PERAKITAN GLOBAL
        # ==========================================================
        title2 = create_step_banner("2. DISKRITISASI & MATRIKS GLOBAL", "#0284C7")
        self.play(FadeIn(title2))

        # 2a. Generic Formula
        k_formula_title = Text("Rumus Umum Matriks Elemen:", font_size=20, color="#64748B").move_to([0, 0.4, 0])
        k_math = MathTex(
            r"k^{e} = \frac{EA}{L}",
            r"\begin{bmatrix} c^2 & cs & -c^2 & -cs \\ cs & s^2 & -cs & -s^2 \\ -c^2 & -cs & c^2 & cs \\ -cs & -s^2 & cs & s^2 \end{bmatrix}"
        ).scale(0.85).next_to(k_formula_title, DOWN, buff=0.3)
        k_math[0].set_color("#0284C7")
        
        local_group = VGroup(k_formula_title, k_math)

        self.play(FadeIn(local_group, shift=UP*0.2))
        self.wait(1.5)
        self.play(FadeOut(local_group))

        # 2b. Derivation Example (NEW ADDITION)
        deriv_title = Text("Contoh Derivasi: Elemen A-B", font_size=22, color="#0F172A", weight="BOLD").move_to([0, 0.4, 0])
        deriv_params = MathTex(r"L = 1.5\text{ m}, \quad \theta = 0^\circ \implies c=1, \ s=0").scale(0.8).next_to(deriv_title, DOWN, buff=0.2)
        deriv_params.set_color("#64748B")

        k_ab_math = MathTex(
            r"k^{AB} = \frac{EA}{1.5}",
            r"\begin{bmatrix} 1 & 0 & -1 & 0 \\ 0 & 0 & 0 & 0 \\ -1 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}"
        ).scale(0.8).next_to(deriv_params, DOWN, buff=0.2)
        k_ab_math[0].set_color("#D97706")

        self.play(Write(deriv_title))
        self.play(FadeIn(deriv_params))
        self.play(Write(k_ab_math))
        
        # Highlight specific element A-B
        self.play(elements[0].animate.set_color("#D97706").set_stroke(width=9))
        self.wait(2)
        self.play(elements[0].animate.set_color("#94A3B8").set_stroke(width=5))
        self.play(FadeOut(deriv_title, deriv_params, k_ab_math))

        # 2c. Global Assembly
        assembly_title = Text("Perakitan Sistem Global: K u = F", font_size=24, color="#0F172A", weight="BOLD").move_to([0, -0.2, 0])
        global_eq = MathTex(
            r"\begin{bmatrix} K_{1,1} & \cdots & K_{1,16} \\ \vdots & \ddots & \vdots \\ K_{16,1} & \cdots & K_{16,16} \end{bmatrix}",
            r"\begin{bmatrix} u_{Ax} \\ u_{Ay} \\ \vdots \\ u_{Ey} \end{bmatrix}",
            r"=",
            r"\begin{bmatrix} F_{Ax} \\ F_{Ay} \\ \vdots \\ F_{Ey} \end{bmatrix}"
        ).scale(0.85).next_to(assembly_title, DOWN, buff=0.4)
        
        global_eq[0].set_color("#0284C7") 
        global_eq[1].set_color("#16A34A") 
        global_eq[3].set_color("#E11D48") 

        # Highlight mapping to top left corner of K matrix
        k_highlight = SurroundingRectangle(global_eq[0][0][1:7], color="#D97706", buff=0.05, stroke_width=2)

        self.play(Write(assembly_title))
        self.play(FadeIn(global_eq))
        self.play(Create(k_highlight))
        self.wait(1.5)
        self.play(FadeOut(title2), FadeOut(assembly_title), FadeOut(k_highlight))

        # ==========================================================
        # SCENE 3: SYARAT BATAS (BOUNDARY CONDITIONS)
        # ==========================================================
        title3 = create_step_banner("3. SYARAT BATAS (BOUNDARY CONDITIONS)", "#BE185D")
        self.play(FadeIn(title3))

        bc_desc = Text("Tumpuan dimasukkan untuk menghindari matriks singular.", font_size=18, color="#64748B").next_to(global_eq, UP, buff=0.4)
        self.play(FadeIn(bc_desc))

        global_eq_bc = MathTex(
            r"\begin{bmatrix} K_{1,1} & \cdots & K_{1,16} \\ \vdots & \ddots & \vdots \\ K_{16,1} & \cdots & K_{16,16} \end{bmatrix}",
            r"\begin{bmatrix} \mathbf{0} \\ \mathbf{0} \\ \vdots \\ u_{Ey} \end{bmatrix}",
            r"=",
            r"\begin{bmatrix} F_{Ax} \\ F_{Ay} \\ \vdots \\ F_{Ey} \end{bmatrix}"
        ).scale(0.85).move_to(global_eq.get_center())
        
        global_eq_bc[0].set_color("#0284C7") 
        global_eq_bc[1].set_color("#16A34A") 
        global_eq_bc[1][0][1:3].set_color("#BE185D") 
        global_eq_bc[3].set_color("#E11D48") 

        self.play(Flash(supA, color="#BE185D", line_length=0.3), Flash(rollerE, color="#BE185D", line_length=0.3))
        self.play(Transform(global_eq, global_eq_bc))
        
        strike1 = Line(global_eq_bc[0].get_left() + UP*0.6, global_eq_bc[3].get_right() + UP*0.6, color="#BE185D", stroke_width=4)
        strike2 = Line(global_eq_bc[0].get_top() + LEFT*0.8, global_eq_bc[0].get_bottom() + LEFT*0.8, color="#BE185D", stroke_width=4)
        
        self.play(Create(strike1), Create(strike2))
        self.wait(1.5)

        self.play(
            FadeOut(title3), FadeOut(bc_desc), FadeOut(global_eq), 
            FadeOut(strike1), FadeOut(strike2)
        )

        # ==========================================================
        # SCENE 4: PENYELESAIAN & GAYA DALAM (CALCULATED RESULTS)
        # ==========================================================
        title4 = create_step_banner("4. SOLUSI: DISPLACEMENT & GAYA DALAM", "#D97706")
        self.play(FadeIn(title4))

        solve_math = MathTex(
            r"\{\mathbf{u}_{unknown}\} = [\mathbf{K}_{reduced}]^{-1} \{\mathbf{F}_{known}\}"
        ).scale(1.1).move_to([0, -1.2, 0])
        solve_math.set_color_by_tex("u", "#16A34A").set_color_by_tex("K", "#0284C7").set_color_by_tex("F", "#E11D48")
        
        self.play(Write(solve_math))
        self.wait(1.5)
        self.play(FadeOut(solve_math))

        # Restore Truss
        self.play(truss_system.animate.scale(1/0.55).move_to([0, 0.6, 0]))
        self.play(FadeOut(dims), FadeOut(loads))

        # Setup Legend
        legend_group = VGroup(
            VGroup(Dot(color="#0284C7", radius=0.1), Text("Compression (-) / Tekan", font_size=20, color="#0284C7")).arrange(RIGHT),
            VGroup(Dot(color="#E11D48", radius=0.1), Text("Tension (+) / Tarik", font_size=20, color="#E11D48")).arrange(RIGHT),
            VGroup(Arrow(start=DOWN*0.5, end=ORIGIN, color="#16A34A", buff=0), Text("Reactions / Reaksi", font_size=20, color="#16A34A")).arrange(RIGHT)
        ).arrange(DOWN, aligned_edge=LEFT).move_to([0, -3.2, 0])
        
        self.play(FadeIn(legend_group))

        # Analyzed Internal Forces based on statics
        forces = {
            "AB": 19.1, "BC": 19.1, "CD": 21.4, "DE": 21.4,
            "AH": -23.0, "HG": -29.3, "GJ": -30.9, "JE": -25.7,
            "HB": 0.0, "GC": 11.3, "JD": 0.0,
            "HC": 12.2, "JC": 15.3
        }

        # Color the members based on compression/tension
        comp_anims, tens_anims, zero_anims = [], [], []
        for key, val in forces.items():
            if val < 0:
                comp_anims.append(line_dict[key].animate.set_color("#0284C7").set_stroke(width=9))
            elif val > 0:
                tens_anims.append(line_dict[key].animate.set_color("#E11D48").set_stroke(width=9))
            else:
                zero_anims.append(line_dict[key].animate.set_color("#94A3B8").set_stroke(width=4))
                
        self.play(*(comp_anims + tens_anims + zero_anims), run_time=1.5)

        # Create force labels dynamically
        force_labels = VGroup()
        for key, val in forces.items():
            if val == 0:
                color, sign = "#64748B", ""
            else:
                color = "#E11D48" if val > 0 else "#0284C7"
                sign = "+" if val > 0 else ""
            
            txt = Text(f"{sign}{val}", font_size=16, color=color, weight="BOLD")
            bg = BackgroundRectangle(txt, color=WHITE, fill_opacity=0.9, buff=0.05)
            lbl = VGroup(bg, txt).move_to(line_dict[key].get_center())
            force_labels.add(lbl)

        self.play(FadeIn(force_labels))

        # Add Computed Reaction Forces
        RA_post = Arrow(start=n["A"]+DOWN*0.8, end=n["A"]+DOWN*0.2, color="#16A34A", stroke_width=8, buff=0)
        RE_post = Arrow(start=n["E"]+DOWN*0.8, end=n["E"]+DOWN*0.2, color="#16A34A", stroke_width=8, buff=0)
        
        txt_RA = Text("16.75 kN", color="#16A34A", font_size=20, weight="BOLD").next_to(RA_post, RIGHT, buff=0.1)
        txt_RE = Text("20.25 kN", color="#16A34A", font_size=20, weight="BOLD").next_to(RE_post, LEFT, buff=0.1)

        self.play(GrowArrow(RA_post), GrowArrow(RE_post))
        self.play(FadeIn(txt_RA), FadeIn(txt_RE))
        self.play(Flash(n["A"], color="#16A34A", line_length=0.5), Flash(n["E"], color="#16A34A", line_length=0.5))
        
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