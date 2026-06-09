from manim import *
import numpy as np

# ==========================================================
# ADVANCED STRUCTURAL ANALYSIS PLATFORM ENGINE (LIGHT MODE)
# ==========================================================

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8

class DiscretePositionBeam(Scene):
    def construct(self):
        # Crisp white workspace background
        self.camera.background_color = "#FFFFFF"

        # Structural Properties
        L = 10.0           # Total length of the beam (m)
        L_s = 7.0          # Position of the right support (m) -> Creates a 3m overhang
        EI = 2.4e5
        beam_len = 6.6     # Visual width scaling on screen

        # Fixed Global Layout Scale Matrix
        Y_BEAM = 3.6
        Y_INF  = 0.8
        Y_SFD  = -2.0
        Y_BMD  = -4.8
        
        # Scaling coefficients for stable visual sizing
        DEFLECTION_VISUAL_SCALE = 35.0
        SHEAR_SCALE = 0.0025
        MOMENT_SCALE = 0.0012

        x0 = -beam_len / 2
        x1 = beam_len / 2

        # ValueTracker initialized to the first position (1/4 from left)
        truck_x = ValueTracker(L / 4)

        # Configured for a single, heavy point load
        axles = [
            (100, 0.0),   # (Load kN, Distance from reference tracker m)
        ]

        # Coordinate Map: Structure x [0, L] -> Screen space [x0, x1]
        def sx(x):
            return x0 + beam_len * x / L

        def active_loads():
            out = []
            for P, off in axles:
                x = truck_x.get_value() + off
                if 0 <= x <= L:
                    out.append((P, x))
            return out

        def reactions():
            loads = active_loads()
            # Moment about A to find RB (Support is at L_s)
            RB = sum(P * x / L_s for P, x in loads)
            RA = sum(P for P, _ in loads) - RB
            return RA, RB

        def shear(x):
            RA, RB = reactions()
            v = 0
            eps = 1e-5 
            if x >= -eps:
                v += RA
            if x >= L_s - eps:
                v += RB
            for P, xp in active_loads():
                if x >= xp - eps:
                    v -= P
            return v

        def moment(x):
            RA, RB = reactions()
            m = 0
            if x > 0:
                m += RA * x
            if x > L_s:
                m += RB * (x - L_s)
            for P, xp in active_loads():
                if x > xp:
                    m -= P * (x - xp)
            return m

        def total_deflection(x):
            loads = active_loads()
            if not loads: 
                return 0.0
                
            RA, RB = reactions()
            total_y = 0.0
            
            for P, xp in loads:
                # Macaulay's Method for overhanging beam deflection
                def mac(val): return max(0.0, val)
                
                term_RA = RA * (x**3) / 6.0
                term_P  = -P * (mac(x - xp)**3) / 6.0
                term_RB = RB * (mac(x - L_s)**3) / 6.0
                
                # Boundary condition: y(L_s) = 0 solves for integration constant C1
                C1 = -((RA * (L_s**3) / 6.0) - (P * (mac(L_s - xp)**3) / 6.0)) / L_s
                
                y = (term_RA + term_P + term_RB + C1 * x) / EI
                total_y += y
                
            return -total_y 

        # ==========================================================
        # ULTRA-STABLE HIGH PERFORMANCE REDRAW ENGINE
        # ==========================================================
        def stable_redraw(func):
            container = VGroup()
            def updater(m):
                m.submobjects.clear()
                generated = func()
                if isinstance(generated, VGroup):
                    m.add(*generated.submobjects)
                elif generated is not None:
                    m.add(generated)
            container.add_updater(updater)
            return container

        # ==========================================================
        # MODERN COMPONENT UI FRAMES (LIGHT MODE)
        # ==========================================================
        def create_plot_frame(center_y, label, accent_color):
            frame = RoundedRectangle(
                width=7.4, height=2.4, corner_radius=0.12,
                stroke_color="#94A3B8", stroke_width=1.5,
                fill_color="#F8FAFC", fill_opacity=0.9
            ).move_to([0, center_y, 0])
            
            accent_tag = Rectangle(
                width=0.08, height=0.35,
                fill_color=accent_color, fill_opacity=1, stroke_width=0
            ).move_to([x0 - 0.25, center_y + 0.95, 0], aligned_edge=LEFT)

            title_text = Text(label, color="#1E293B", weight="BOLD").scale(0.24)
            title_text.move_to([x0 - 0.1, center_y + 0.95, 0], aligned_edge=LEFT)
            
            axis_line = Line([x0, center_y, 0], [x1, center_y, 0], color="#94A3B8", stroke_width=1.5)
            return VGroup(frame, accent_tag, title_text, axis_line)

        # Main Header
        header_title = Text("STATIC LOAD FINITE ELEMENT METRICS", color="#0369A1", weight="BOLD").scale(0.45)
        header_sub = Text("DISCRETE POSITION ANALYSIS", color="#BE123C").scale(0.28)
        
        header_title.to_edge(UP, buff=0.8) 
        header_sub.next_to(header_title, DOWN, buff=0.15)
        self.add(header_title, header_sub)

        # Watermark Label 
        watermark = Text("@ScanPintar", color="#64748B", weight="BOLD").scale(0.30)
        watermark.to_corner(DR, buff=0.4)
        self.add(watermark)

        # Accent colors chosen for readability against white
        self.add(create_plot_frame(Y_BEAM, "STRUCTURE DEFORMATION SYSTEM", "#16A34A"))
        self.add(create_plot_frame(Y_INF, "INFLUENCE LINE DESIGN MATRIX (RA)", "#D97706"))
        self.add(create_plot_frame(Y_SFD, "SHEAR FORCE DIAGRAM (SFD)", "#0284C7"))
        self.add(create_plot_frame(Y_BMD, "BENDING MOMENT DIAGRAM (BMD)", "#BE185D"))

        neutral_axis = DashedLine(
            start=[sx(0), Y_BEAM, 0], 
            end=[sx(L), Y_BEAM, 0], 
            color="#9CA3AF", 
            stroke_width=1.5, 
            dash_length=0.08
        )
        self.add(neutral_axis)

        # ==========================================================
        # DYNAMIC DEFORMING STRUCTURAL ELEMENT
        # ==========================================================
        def draw_dynamic_beam():
            xs = np.linspace(0, L, 80)
            pts = [[sx(x), Y_BEAM - total_deflection(x) * DEFLECTION_VISUAL_SCALE, 0] for x in xs]
            curve = VMobject(color="#16A34A", stroke_width=5)
            curve.set_points_smoothly(pts)
            return curve

        def draw_peak_deflection_label():
            xs = np.linspace(0, L, 100)
            defs = [total_deflection(x) for x in xs]
            max_idx = np.argmax([abs(d) for d in defs]) 
            max_x = xs[max_idx]
            max_def_m = defs[max_idx]
            max_def_mm = max_def_m * 1000 

            if abs(max_def_mm) > 0.1:
                y_pos = Y_BEAM - max_def_m * DEFLECTION_VISUAL_SCALE
                dot = Dot([sx(max_x), y_pos, 0], radius=0.04, color="#15803D")
                lbl = Text(f"{abs(max_def_mm):.1f} mm", color="#15803D", weight="BOLD").scale(0.20)
                lbl.next_to(dot, DOWN if max_def_m > 0 else UP, buff=0.1)
                return VGroup(dot, lbl)
            return VMobject()

        self.add(stable_redraw(draw_dynamic_beam))
        self.add(stable_redraw(draw_peak_deflection_label))

        # Support Icons (Darker grey/black for white background)
        hinge = Triangle(color="#1E293B", fill_color="#94A3B8", fill_opacity=1).scale(0.14).move_to([sx(0), Y_BEAM - 0.14, 0])
        roller = Circle(color="#1E293B", fill_color="#94A3B8", fill_opacity=1).scale(0.08).move_to([sx(L_s), Y_BEAM - 0.08, 0])
        self.add(hinge, roller)

        # ==========================================================
        # KINEMATIC PEDESTRIAN POINT-LOAD ASSET
        # ==========================================================
        def draw_pedestrian_load():
            g = VGroup()
            t_x = truck_x.get_value()
            
            for P, off in axles:
                axle_pos = t_x + off
                if 0 <= axle_pos <= L:
                    pos_x = sx(axle_pos)
                    base_y = Y_BEAM
                    
                    # Minimalist Architectural Silhouette Blueprint (Dark Blue)
                    head = Circle(radius=0.07, color="#2563EB", fill_color="#2563EB", fill_opacity=0.6, stroke_width=1.5).move_to([pos_x, base_y + 0.62, 0])
                    torso = Line([pos_x, base_y + 0.55, 0], [pos_x, base_y + 0.32, 0], color="#2563EB", stroke_width=3)
                    left_leg = Line([pos_x, base_y + 0.32, 0], [pos_x - 0.05, base_y + 0.12, 0], color="#2563EB", stroke_width=2.5)
                    right_leg = Line([pos_x, base_y + 0.32, 0], [pos_x + 0.05, base_y + 0.12, 0], color="#2563EB", stroke_width=2.5)
                    left_arm = Line([pos_x, base_y + 0.50, 0], [pos_x - 0.06, base_y + 0.35, 0], color="#2563EB", stroke_width=2)
                    right_arm = Line([pos_x, base_y + 0.50, 0], [pos_x + 0.06, base_y + 0.35, 0], color="#2563EB", stroke_width=2)
                    
                    person = VGroup(head, torso, left_leg, right_leg, left_arm, right_arm)
                    g.add(person)

                    # Concentrated Vector Force Arrow (Deep Red)
                    arrow_length = P * 0.01 
                    arrow = Arrow(
                        [pos_x, base_y + 0.10 + arrow_length, 0],
                        [pos_x, base_y + 0.10, 0],
                        buff=0, color="#DC2626", stroke_width=4, max_tip_length_to_length_ratio=0.15
                    )
                    txt = Text(f"{P} kN", color="#DC2626", weight="BOLD").scale(0.18)
                    txt.next_to(arrow, UP, buff=0.06)
                    g.add(arrow, txt)

            return g

        self.add(stable_redraw(draw_pedestrian_load))

        def render_reactions():
            RA, RB = reactions()
            t1 = Text(f"RA = {RA:.1f} kN", color="#D97706", weight="BOLD").scale(0.22).move_to([sx(0), Y_BEAM - 0.45, 0])
            t2 = Text(f"RB = {RB:.1f} kN", color="#D97706", weight="BOLD").scale(0.22).move_to([sx(L_s), Y_BEAM - 0.45, 0])
            return VGroup(t1, t2)

        self.add(stable_redraw(render_reactions))

        # ==========================================================
        # INFLUENCE LINE TRACKING SYSTEM 
        # ==========================================================
        infl_pts = [
            [sx(0), Y_INF, 0],
            [sx(0), Y_INF + 0.8, 0],
            [sx(L_s), Y_INF, 0],
            [sx(L), Y_INF + 0.8 * (1 - L / L_s), 0],
            [sx(L), Y_INF, 0],
            [sx(0), Y_INF, 0]
        ]
        infl_poly = VMobject(fill_color="#D97706", fill_opacity=0.1, stroke_color="#D97706", stroke_width=1.5)
        infl_poly.set_points_as_corners(infl_pts)
        self.add(infl_poly)

        def draw_influence_marker():
            loads = active_loads()
            if not loads:
                return VMobject()
            leading_x = loads[0][1]
            y_val = (1 - leading_x / L_s) * 0.8
            dot = Dot([sx(leading_x), Y_INF + y_val, 0], color="#D97706", radius=0.05)
            val_lbl = Text(f"η = {1-(leading_x/L_s):.2f}", color="#D97706", weight="BOLD").scale(0.20)
            val_lbl.next_to(dot, UP if y_val >= 0 else DOWN, buff=0.08)
            return VGroup(dot, val_lbl)

        self.add(stable_redraw(draw_influence_marker))

        # ==========================================================
        # VECTOR STEP-DIAGRAM AND SHARP PEAK ENGINES
        # ==========================================================
        def create_sfd_diagram():
            loads = active_loads()
            nodes = [0, L_s, L] 
            for _, xp in loads:
                if 0 < xp < L:
                    nodes.append(xp)
            nodes = sorted(list(set(nodes)))

            outline_pts = []
            v_eval = []
            x_eval_pos = []
            
            for i in range(len(nodes) - 1):
                x_start, x_end = nodes[i], nodes[i+1]
                v = shear((x_start + x_end) / 2) 
                outline_pts.append([sx(x_start), Y_SFD + v * SHEAR_SCALE, 0])
                outline_pts.append([sx(x_end), Y_SFD + v * SHEAR_SCALE, 0])
                v_eval.append(v)
                x_eval_pos.append((x_start + x_end) / 2)

            if not outline_pts:
                return VMobject()

            fill_pts = [[sx(0), Y_SFD, 0]] + outline_pts + [[sx(L), Y_SFD, 0]]
            fill_obj = VMobject(stroke_width=0, fill_color="#0284C7", fill_opacity=0.15).set_points_as_corners(fill_pts)
            line_obj = VMobject(color="#0284C7", stroke_width=2.5).set_points_as_corners(outline_pts)
            g = VGroup(fill_obj, line_obj)

            if v_eval:
                p_idx = np.argmax([abs(v) for v in v_eval])
                max_v = v_eval[p_idx]
                if abs(max_v) > 2.0:
                    dot = Dot([sx(x_eval_pos[p_idx]), Y_SFD + max_v * SHEAR_SCALE, 0], radius=0.04, color="#0F172A")
                    lbl = Text(f"{max_v:.1f} kN", color="#0F172A", weight="BOLD").scale(0.20)
                    lbl.next_to(dot, UP if max_v >= 0 else DOWN, buff=0.08)
                    g.add(dot, lbl)
            return g

        def create_bmd_diagram():
            loads = active_loads()
            nodes = [0, L_s, L]
            for _, xp in loads:
                if 0 < xp < L:
                    nodes.append(xp)
            nodes = sorted(list(set(nodes)))

            outline_pts = [[sx(x), Y_BMD + moment(x) * MOMENT_SCALE, 0] for x in nodes]
            fill_pts = [[sx(0), Y_BMD, 0]] + outline_pts + [[sx(L), Y_BMD, 0]]
            
            fill_obj = VMobject(stroke_width=0, fill_color="#BE185D", fill_opacity=0.15).set_points_as_corners(fill_pts)
            line_obj = VMobject(color="#BE185D", stroke_width=2.5).set_points_as_corners(outline_pts)
            g = VGroup(fill_obj, line_obj)

            vals = [moment(x) for x in nodes]
            if vals:
                p_idx = np.argmax([abs(v) for v in vals])
                max_m = vals[p_idx]
                if abs(max_m) > 2.0:
                    dot = Dot([sx(nodes[p_idx]), Y_BMD + max_m * MOMENT_SCALE, 0], radius=0.04, color="#0F172A")
                    lbl = Text(f"{max_m:.1f} kNm", color="#0F172A", weight="BOLD").scale(0.20)
                    lbl.next_to(dot, UP if max_m >= 0 else DOWN, buff=0.08)
                    g.add(dot, lbl)
            return g

        self.add(stable_redraw(create_sfd_diagram))
        self.add(stable_redraw(create_bmd_diagram))

        # ==========================================================
        # DISCRETE POSITION SWITCHING SEQUENCE
        # ==========================================================
        
        # Position 1: 1/4 from left side
        truck_x.set_value(L / 4)
        self.wait(3.0)

        # Position 2: 1/2 of the beam
        truck_x.set_value(L / 2)
        self.wait(3.0)

        # Position 3: At the end of overhang
        truck_x.set_value(L)
        self.wait(3.0)