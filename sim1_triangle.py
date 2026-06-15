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
        L = 3.0            # Total length of the beam (m)
        EI = 2.4e5
        beam_len = 6.6     # Visual width scaling on screen
        
        # Dynamic Tracker: Right support starting at the right end (x = L)
        support_B_x = ValueTracker(3.0)

        # Global Layout Scale Matrix
        Y_BEAM = 3.6
        Y_INF  = 0.8
        Y_SFD  = -2.0
        Y_BMD  = -4.8
        
        Y_TOP_ALIGN = 4.8
        Y_BOTTOM_ALIGN = -6.0
        
        # Visual scaling coefficients
        DEFLECTION_VISUAL_SCALE = 30000.0
        SHEAR_SCALE = 0.12
        MOMENT_SCALE = 0.15

        x0 = -beam_len / 2
        x1 = beam_len / 2

        def sx(x):
            return x0 + beam_len * x / L

        # ==========================================================
        # EXACT PIECEWISE LOAD CALCULUS ENGINE
        # ==========================================================
        # Q_val(x): Integral of load q(t) dt from 0 to x (Total force up to x)
        def Q_val(x):
            if x <= 0: return 0.0
            if x <= 1.5:
                return 8.0 * x - (x**2)
            elif x <= 2.25:
                return 9.75 + 5.0 * (x - 1.5)
            elif x <= 3.0:
                t = x - 2.25
                return 13.5 + 5.0 * t - (10.0 / 3.0) * (t**2)
            else:
                return 15.375

        # Iq_val(x): Integral of t * q(t) dt from 0 to x (Moment of load up to x about origin)
        def Iq_val(x):
            if x <= 0: return 0.0
            if x <= 1.5:
                return 4.0 * (x**2) - (2.0 / 3.0) * (x**3)
            elif x <= 2.25:
                return 6.75 + 2.5 * ((x**2) - 2.25)
            elif x <= 3.0:
                upper = 10.0 * (x**2) - (20.0 / 9.0) * (x**3)
                return 13.78125 + (upper - 25.3125)
            else:
                return 18.46875

        # Moment of the distributed load up to x, taken ABOUT x
        def M_q(x):
            return x * Q_val(x) - Iq_val(x)

        # ==========================================================
        # DYNAMIC STRUCTURAL MATH ENGINE
        # ==========================================================
        def reactions():
            xB = support_B_x.get_value()
            F_load = 15.375      # Total downward force
            M_load_O = 18.46875  # Total moment about pinned origin O
            
            RB = M_load_O / xB
            RA = F_load - RB
            return RA, RB

        def shear(x):
            xB = support_B_x.get_value()
            RA, RB = reactions()
            
            v = 0
            eps = 1e-5 
            if x >= -eps:
                v += RA
            if x >= xB - eps:
                v += RB
            
            v -= Q_val(x)
            return v

        def moment(x):
            xB = support_B_x.get_value()
            RA, RB = reactions()
            
            m = 0
            if x > 0:
                m += RA * x
            if x > xB:
                m += RB * (x - xB)
                
            m -= M_q(x)
            return m

        # Stable Numerical Double Integration for exact piecewise deflection
        def total_deflection_array():
            xB = support_B_x.get_value()
            xs = np.linspace(0, L, 250)
            dx = xs[1] - xs[0]
            
            M_vals = np.array([moment(x) for x in xs])
            
            # Fast cumulative trapezoidal integration (EI y'' = M(x))
            theta_raw = np.zeros_like(M_vals)
            theta_raw[1:] = np.cumsum(0.5 * (M_vals[:-1] + M_vals[1:]) * dx)
            
            y_raw = np.zeros_like(theta_raw)
            y_raw[1:] = np.cumsum(0.5 * (theta_raw[:-1] + theta_raw[1:]) * dx)
            
            # Boundary condition mapping
            idx_xB = np.argmin(np.abs(xs - xB))
            if xB > 0.05:
                C1 = -y_raw[idx_xB] / xB
            else:
                C1 = 0
                
            # y_upward captures true structural upward displacement (which is negative under gravity)
            y_upward = (y_raw + C1 * xs) / EI
            
            # Return inverted positive values so the visual renderer correctly pushes coordinates DOWN
            return xs, -y_upward 

        # ==========================================================
        # ULTRA-STABLE REDRAW WRAPPER
        # ==========================================================
        def stable_redraw(func):
            m = func()
            def updater(mob):
                mob.become(func())
            m.add_updater(updater)
            return m

        # ==========================================================
        # STATIC UI FRAMES & HEADERS
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

        header_title = Text("ANALISIS DUKUNGAN KINEMATIS DINAMIS", color="#0369A1", weight="BOLD").scale(0.40)
        header_sub = Text("DISTRIBUSI BEBAN KOMPLEKS DENGAN BATAS BERGERAK", color="#BE123C").scale(0.25)
        
        header_title.to_edge(UP, buff=0.8) 
        header_sub.next_to(header_title, DOWN, buff=0.15)
        self.add(header_title, header_sub)

        watermark = Text("@ScanPintar", color="#64748B", weight="BOLD").scale(0.30)
        watermark.next_to(header_sub, DOWN, buff=0.4)
        self.add(watermark)

        self.add(create_plot_frame(Y_BEAM, "SISTEM DEFORMASI STRUKTUR", "#16A34A"))
        self.add(create_plot_frame(Y_INF, "MATRIKS DESAIN GARIS PENGARUH (RA)", "#D97706"))
        self.add(create_plot_frame(Y_SFD, "DIAGRAM GAYA GESER (SFD)", "#0284C7"))
        self.add(create_plot_frame(Y_BMD, "DIAGRAM MOMEN LENTUR (BMD)", "#BE185D"))

        # ==========================================================
        # STATIC UDL GRAPHICS & DIMENSIONS
        # ==========================================================
        def generate_udl_graphics():
            udl_group = VGroup()
            load_scale = 0.08
            
            # Envelope Polygon
            pts = [
                [sx(0), Y_BEAM + 8 * load_scale, 0],
                [sx(1.5), Y_BEAM + 5 * load_scale, 0],
                [sx(2.25), Y_BEAM + 5 * load_scale, 0],
                [sx(3.0), Y_BEAM, 0] 
            ]
            
            top_line = VMobject(color="#0EA5E9", stroke_width=2)
            top_line.set_points_as_corners(pts)
            udl_group.add(top_line)
            
            # Trapezoid segment arrows
            for x in np.linspace(0, 1.5, 9):
                q_val = 8.0 - 2.0 * x
                arrow = Arrow([sx(x), Y_BEAM + q_val * load_scale, 0], [sx(x), Y_BEAM + 0.05, 0],
                              buff=0, color="#0EA5E9", stroke_width=1.5, max_tip_length_to_length_ratio=0.25)
                udl_group.add(arrow)
                
            # Rectangle segment arrows
            for x in np.linspace(1.5, 2.25, 5)[1:]:
                arrow = Arrow([sx(x), Y_BEAM + 5.0 * load_scale, 0], [sx(x), Y_BEAM + 0.05, 0],
                              buff=0, color="#0EA5E9", stroke_width=1.5, max_tip_length_to_length_ratio=0.25)
                udl_group.add(arrow)
                
            # Triangle segment arrows
            for x in np.linspace(2.25, 3.0, 5)[1:-1]: 
                q_val = 5.0 - (20.0 / 3.0) * (x - 2.25)
                arrow = Arrow([sx(x), Y_BEAM + q_val * load_scale, 0], [sx(x), Y_BEAM + 0.05, 0],
                              buff=0, color="#0EA5E9", stroke_width=1.5, max_tip_length_to_length_ratio=0.25)
                udl_group.add(arrow)

            # Load Labels
            lbl_8 = Text("8 kN/m", color="#0EA5E9", weight="BOLD").scale(0.22)
            lbl_8.move_to([sx(0), Y_BEAM + 8 * load_scale + 0.2, 0])
            
            lbl_5 = Text("5 kN/m", color="#0EA5E9", weight="BOLD").scale(0.22)
            lbl_5.move_to([sx(1.875), Y_BEAM + 5 * load_scale + 0.2, 0])
            
            udl_group.add(lbl_8, lbl_5)
            return udl_group

        def generate_dimension_lines():
            dims = VGroup()
            y_dim = Y_BEAM - 1.1
            segments = [(0, 1.5, "1.5 m"), (1.5, 2.25, "0.75 m"), (2.25, 3.0, "0.75 m")]
            
            for start, end, label in segments:
                line = Line([sx(start), y_dim, 0], [sx(end), y_dim, 0], color="#64748B", stroke_width=1.5)
                t1 = Line([sx(start), y_dim + 0.1, 0], [sx(start), y_dim - 0.1, 0], color="#64748B", stroke_width=1.5)
                t2 = Line([sx(end), y_dim + 0.1, 0], [sx(end), y_dim - 0.1, 0], color="#64748B", stroke_width=1.5)
                lbl = Text(label, color="#1E293B", weight="BOLD").scale(0.18).next_to(line, UP, buff=0.08)
                dims.add(line, t1, t2, lbl)
            return dims

        self.add(generate_udl_graphics())
        self.add(generate_dimension_lines())

        # ==========================================================
        # DYNAMIC ALIGNMENT LINES & SUPPORTS
        # ==========================================================
        def draw_alignment_lines():
            xB = support_B_x.get_value()
            g = VGroup()
            
            for x_val in [0, L]:
                g.add(DashedLine(start=[sx(x_val), Y_TOP_ALIGN, 0], end=[sx(x_val), Y_BOTTOM_ALIGN, 0],
                                 color="#CBD5E1", stroke_width=1.2, dash_length=0.12))
                
            dynamic_dash = DashedLine(start=[sx(xB), Y_TOP_ALIGN, 0], end=[sx(xB), Y_BOTTOM_ALIGN, 0],
                                      color="#EF4444", stroke_width=1.5, dash_length=0.08)
            g.add(dynamic_dash)
            return g

        self.add(stable_redraw(draw_alignment_lines))

        neutral_axis = DashedLine(start=[sx(0), Y_BEAM, 0], end=[sx(L), Y_BEAM, 0], 
                                  color="#9CA3AF", stroke_width=1.5, dash_length=0.08)
        self.add(neutral_axis)

        def draw_supports():
            xB = support_B_x.get_value()
            g = VGroup()
            
            wall_plate = Rectangle(width=0.06, height=0.6, fill_color="#CBD5E1", stroke_color="#64748B", stroke_width=1).move_to([sx(0) - 0.03, Y_BEAM, 0])
            hinge = Triangle(color="#1E293B", fill_color="#94A3B8", fill_opacity=1).scale(0.14).move_to([sx(0), Y_BEAM - 0.14, 0])
            roller = Circle(color="#1E293B", fill_color="#94A3B8", fill_opacity=1).scale(0.08).move_to([sx(xB), Y_BEAM - 0.08, 0])
            
            g.add(wall_plate, hinge, roller)
            return g

        self.add(stable_redraw(draw_supports))

        # ==========================================================
        # CORRECTED DEFORMATION ENGINE
        # ==========================================================
        def draw_dynamic_beam():
            xs, defs = total_deflection_array()
            
            # The coordinate inversion is fixed: defs is now correctly processed
            # to render downwards smoothly.
            pts = [[sx(x), Y_BEAM - d * DEFLECTION_VISUAL_SCALE, 0] for x, d in zip(xs, defs)]
            curve = VMobject(color="#16A34A", stroke_width=5)
            curve.set_points_smoothly(pts)
            return curve

        self.add(stable_redraw(draw_dynamic_beam))

        def render_reactions():
            xB = support_B_x.get_value()
            RA, RB = reactions()
            t1 = Text(f"RA = {RA:.1f} kN", color="#D97706", weight="BOLD").scale(0.22).move_to([sx(0), Y_BEAM - 0.55, 0])
            t2 = Text(f"RB = {RB:.1f} kN", color="#D97706", weight="BOLD").scale(0.22).move_to([sx(xB), Y_BEAM - 0.55, 0])
            return VGroup(t1, t2)

        self.add(stable_redraw(render_reactions))

        # ==========================================================
        # INFLUENCE LINE TRACKING SYSTEM (DYNAMIC SHAPE)
        # ==========================================================
        def draw_influence_poly():
            xB = support_B_x.get_value()
            def eta(x): return (xB - x) / xB
            
            pts = [
                [sx(0), Y_INF, 0],
                [sx(0), Y_INF + eta(0)*0.8, 0],
                [sx(xB), Y_INF + eta(xB)*0.8, 0],
                [sx(L), Y_INF + eta(L)*0.8, 0],
                [sx(L), Y_INF, 0],
                [sx(0), Y_INF, 0]
            ]
            poly = VMobject(fill_color="#D97706", fill_opacity=0.1, stroke_color="#D97706", stroke_width=1.5)
            poly.set_points_as_corners(pts)
            return poly

        self.add(stable_redraw(draw_influence_poly))

        # ==========================================================
        # ADVANCED CONTINUOUS DIAGRAM ENGINES
        # ==========================================================
        def create_sfd_diagram():
            xB = support_B_x.get_value()
            nodes = sorted(list(set([0.0, 1.5, 2.25, xB, L])))
            clean_nodes = [nodes[0]]
            for n in nodes[1:]:
                if n - clean_nodes[-1] > 1e-3: clean_nodes.append(n)
            nodes = clean_nodes

            outline_pts = []
            for i in range(len(nodes) - 1):
                x_start, x_end = nodes[i], nodes[i+1]
                segment_xs = np.linspace(x_start + 1e-5, x_end - 1e-5, 20)
                for x in segment_xs:
                    outline_pts.append([sx(x), Y_SFD + shear(x) * SHEAR_SCALE, 0])
                
                if i < len(nodes) - 2:
                    node_x = nodes[i+1]
                    outline_pts.append([sx(node_x), Y_SFD + shear(node_x - 1e-5) * SHEAR_SCALE, 0])
                    outline_pts.append([sx(node_x), Y_SFD + shear(node_x + 1e-5) * SHEAR_SCALE, 0])

            outline_pts = [[sx(0), Y_SFD + shear(1e-5) * SHEAR_SCALE, 0]] + outline_pts + [[sx(L), Y_SFD + shear(L - 1e-5) * SHEAR_SCALE, 0]]
            
            fill_pts = [[sx(0), Y_SFD, 0]] + outline_pts + [[sx(L), Y_SFD, 0]]
            fill_obj = VMobject(stroke_width=0, fill_color="#0284C7", fill_opacity=0.15).set_points_as_corners(fill_pts)
            line_obj = VMobject(color="#0284C7", stroke_width=2.5).set_points_as_corners(outline_pts)
            return VGroup(fill_obj, line_obj)

        def create_bmd_diagram():
            xB = support_B_x.get_value()
            nodes = sorted(list(set([0.0, 1.5, 2.25, xB, L])))
            clean_nodes = [nodes[0]]
            for n in nodes[1:]:
                if n - clean_nodes[-1] > 1e-3: clean_nodes.append(n)
            nodes = clean_nodes

            outline_pts = []
            for i in range(len(nodes) - 1):
                x_start, x_end = nodes[i], nodes[i+1]
                segment_xs = np.linspace(x_start, x_end, 20) 
                for x in segment_xs:
                    outline_pts.append([sx(x), Y_BMD + moment(x) * MOMENT_SCALE, 0])

            fill_pts = [[sx(0), Y_BMD, 0]] + outline_pts + [[sx(L), Y_BMD, 0]]
            fill_obj = VMobject(stroke_width=0, fill_color="#BE185D", fill_opacity=0.15).set_points_as_corners(fill_pts)
            line_obj = VMobject(color="#BE185D", stroke_width=2.5).set_points_as_corners(outline_pts)
            return VGroup(fill_obj, line_obj)

        self.add(stable_redraw(create_sfd_diagram))
        self.add(stable_redraw(create_bmd_diagram))

        # ==========================================================
        # ANIMATION SEQUENCE
        # ==========================================================
        self.wait(1.5, frozen_frame=False)

        # Smoothly track Right Support inward by approx 1/5th length (from 3.0m down to 2.4m)
        self.play(
            support_B_x.animate.set_value(2.4), 
            run_time=6.0, 
            rate_func=smooth
        )
        
        self.wait(2.5, frozen_frame=False)

        # ==========================================================
        # OUTRO SEQUENCE
        # ==========================================================
        for mob in self.mobjects:
            mob.clear_updaters()

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.0)
        self.clear() 

        closing_primary = Text("Suka & Bagikan", color="#0369A1", weight="BOLD").scale(0.9)
        closing_secondary = Text("Ikuti @ScanPintar", color="#BE123C", weight="BOLD").scale(0.7)
        outro_group = VGroup(closing_primary, closing_secondary).arrange(DOWN, buff=0.4)

        self.play(Write(outro_group), run_time=1.5)
        self.wait(2.5)