from manim import *
import numpy as np

# ==========================================================
# ADVANCED STRUCTURAL ANALYSIS PLATFORM ENGINE (CANTILEVER MODE)
# ==========================================================

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8

class VariableLoadPeakCantilever(Scene):
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
        EI = 2.4e5         # Flexible visual EI
        beam_len = 5.8     # Visual width scaling on screen (Reduced to add left/right margin)
        
        # Dynamic Tracker: Horizontal position of the peak of the triangle load (starting at L/2 = 1.5m)
        v_peak_x = ValueTracker(1.5)

        # Global Layout Scale Matrix (Adjusted vertically to prevent cramping and overlapping)
        Y_BEAM = 3.6
        Y_SFD  = 0.0      # Moved UP from -2.0 to utilize space and prevent cramping
        Y_BMD  = -3.6     # Moved UP from -4.8 to keep legible separation with Y_SFD
        
        Y_TOP_ALIGN = 4.8
        Y_BOTTOM_ALIGN = -6.0
        
        # Visual scaling coefficients
        DEFLECTION_VISUAL_SCALE = 500.0   # Cantilever deflections are large, use small scale
        SHEAR_SCALE = 0.12     # Reduced from 0.15 to prevent labels/diagram internal overflow
        MOMENT_SCALE = 0.05    # Reduced from 0.15 to prevent labels/diagram internal overflow

        x0 = -beam_len / 2
        x1 = beam_len / 2

        def sx(x):
            return x0 + beam_len * x / L

        # ==========================================================
        # LOAD CALCULUS ENGINE FOR CANTILEVER BEAM
        # ==========================================================
        
        # Point load at free end
        F_point = 3.0 # kN (downward)
        
        # Triangular distributed load properties
        q_max = 6.0 # kN/m (at peak)

        # Q_val(x, xp): Integral of load q(t) dt from 0 to x (Total force up to x)
        def Q_val(x, xp):
            if x <= 0: return 0.0
            eps = 1e-9 # avoid division by zero at boundary cases for peak
            safe_xp = max(xp, eps)
            safe_L_minus_xp = max(3.0 - xp, eps)
            
            if x <= xp:
                return (3.0 / safe_xp) * (x**2)
            elif x <= 3.0:
                t = x
                return 3.0 * xp + (3.0 / safe_L_minus_xp) * (6.0*t - t**2 - 6.0*xp + xp**2)
            else:
                return 9.0 # Total triangle force

        # Iq_val(x, xp): Integral of t * q(t) dt from 0 to x (Moment of load up to x about origin)
        def Iq_val(x, xp):
            if x <= 0: return 0.0
            eps = 1e-9 # avoid division by zero
            safe_xp = max(xp, eps)
            safe_L_minus_xp = max(3.0 - xp, eps)
            
            if x <= xp:
                return (2.0 / safe_xp) * (x**3)
            elif x <= 3.0:
                t = x
                return 2.0 * (xp**2) + (1.0 / safe_L_minus_xp) * (9.0*(t**2) - 2.0*(t**3) - 9.0*(xp**2) + 2.0*(xp**3))
            else:
                return 3.0 * xp + 9.0 # Total moment of triangle about origin (A)

        # Total load moment about origin (A) for current peak position
        def M_total_O(xp):
            return 3.0 * xp + 9.0 + F_point * 3.0 # Triangle moment + point load moment (A=origin)

        # ==========================================================
        # DYNAMIC STRUCTURAL MATH ENGINE
        # ==========================================================
        
        def reactions():
            xp = v_peak_x.get_value()
            F_total = 12.0 # Fixed: F_triangle=9 + F_point=3
            
            # Counter-clockwise reaction moment required
            MA_react = M_total_O(xp) 
            RA_react = F_total
            return RA_react, MA_react

        def shear(x):
            xp = v_peak_x.get_value()
            RA, MA = reactions()
            
            # Internal Shear force (sum of forces to left)
            v = RA - Q_val(x, xp)
            return v

        def moment(x):
            xp = v_peak_x.get_value()
            RA, MA = reactions()
            
            # Internal Moment (sum of moments to left about x)
            Mq_at_x = x * Q_val(x, xp) - Iq_val(x, xp)
            m = RA * x - MA - Mq_at_x
            return m

        # Precise Cantilever Double Integration for visual deflection (v'' = M/EI)
        def total_deflection_array():
            xs = np.linspace(0, L, 250)
            dx = xs[1] - xs[0]
            
            M_vals = np.array([moment(x) for x in xs])
            
            # Fast cumulative trapezoidal integration (EI y'' = M(x))
            theta_raw = np.zeros_like(M_vals)
            theta_raw[1:] = np.cumsum(0.5 * (M_vals[:-1] + M_vals[1:]) * dx)
            
            y_raw = np.zeros_like(theta_raw)
            y_raw[1:] = np.cumsum(0.5 * (theta_raw[:-1] + theta_raw[1:]) * dx)
            
            y_upward = y_raw / EI
            
            # Return inverted positive values so the visual renderer correctly pushes coordinates DOWN smoothly
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
                width=7.4, height=3.0, corner_radius=0.12,
                stroke_color="#94A3B8", stroke_width=1.5,
                fill_color="#F8FAFC", fill_opacity=0.9
            ).move_to([0, center_y, 0])
            
            accent_tag = Rectangle(
                width=0.08, height=0.35,
                fill_color=accent_color, fill_opacity=1, stroke_width=0
            ).move_to([x0 - 0.25, center_y + 1.25, 0], aligned_edge=LEFT)

            title_text = Text(label, color="#1E293B", weight="BOLD").scale(0.24)
            title_text.move_to([x0 - 0.1, center_y + 1.25, 0], aligned_edge=LEFT)
            
            axis_line = Line([x0, center_y, 0], [x1, center_y, 0], color="#94A3B8", stroke_width=1.5)
            return VGroup(frame, accent_tag, title_text, axis_line)

        header_title = Text("SIMULASI BEBAN TERDISTRIBUSI DINAMIS", color="#0369A1", weight="BOLD").scale(0.40)
        header_sub = Text("ANALISIS KANTILEVER DENGAN PEAK BEBAN BERGERAK", color="#BE123C").scale(0.25)
        
        header_title.to_edge(UP, buff=0.8) 
        header_sub.next_to(header_title, DOWN, buff=0.15)
        self.add(header_title, header_sub)

        watermark = Text("@ScanPintar", color="#64748B", weight="BOLD").scale(0.30)
        watermark.next_to(header_sub, DOWN, buff=0.4)
        self.add(watermark)

        self.add(create_plot_frame(Y_BEAM, "SISTEM BEBAN & DEFORMASI STRUKTUR", "#16A34A"))
        self.add(create_plot_frame(Y_SFD, "DIAGRAM GAYA GESER (SFD)", "#0284C7"))
        self.add(create_plot_frame(Y_BMD, "DIAGRAM MOMEN LENTUR (BMD)", "#BE185D"))

        # ==========================================================
        # DYNAMIC UDL GRAPHICS & DIMENSIONS
        # ==========================================================
        def generate_udl_graphics():
            xp = v_peak_x.get_value()
            udl_group = VGroup()
            load_scale = 0.15 # Visually scaled height for arrows
            
            # Load Labels for triangle. Added early to keep rendering z-order clean
            lbl_peak = Text(f"{q_max:.0f} kN/m", color="#0EA5E9", weight="BOLD").scale(0.22)
            lbl_peak.move_to([sx(xp), Y_BEAM + q_max * load_scale + 0.3, 0])
            udl_group.add(lbl_peak)

            # Envelope Polygon for triangle load
            if abs(xp) < 1e-4: # Pure triangle starting from end (q(0)=6, q(3)=0)
                pts = [[sx(0), Y_BEAM + q_max*load_scale, 0], [sx(3), Y_BEAM, 0], [sx(0), Y_BEAM, 0]]
            elif abs(xp - 3.0) < 1e-4: # Pure triangle ending at end (q(0)=0, q(3)=6)
                pts = [[sx(0), Y_BEAM, 0], [sx(3), Y_BEAM + q_max*load_scale, 0], [sx(0), Y_BEAM, 0]]
            else: # Standard triangle
                pts = [
                    [sx(0), Y_BEAM, 0],
                    [sx(xp), Y_BEAM + q_max * load_scale, 0],
                    [sx(3.0), Y_BEAM, 0],
                    [sx(0), Y_BEAM, 0] # Close path
                ]
            
            top_line = Polygon(*pts, fill_color="#0EA5E9", fill_opacity=0.1, stroke_color="#0EA5E9", stroke_width=1.5)
            udl_group.add(top_line)
            
            # Triangle segment arrows
            # Left part: 0 to xp
            if xp > 1e-4:
                for x in np.linspace(0, xp, 10):
                    q_val = (q_max / xp) * x
                    arrow = Arrow([sx(x), Y_BEAM + q_val * load_scale, 0], [sx(x), Y_BEAM + 0.05, 0],
                                  buff=0, color="#0EA5E9", stroke_width=1.5, max_tip_length_to_length_ratio=0.25)
                    udl_group.add(arrow)
                
            # Right part: xp to 3.0
            if (3.0 - xp) > 1e-4:
                for x in np.linspace(xp, 3.0, 10)[1:]:
                    q_val = q_max * (3.0 - x) / (3.0 - xp)
                    arrow = Arrow([sx(x), Y_BEAM + q_val * load_scale, 0], [sx(x), Y_BEAM + 0.05, 0],
                                  buff=0, color="#0EA5E9", stroke_width=1.5, max_tip_length_to_length_ratio=0.25)
                    udl_group.add(arrow)

            # Point load graphic at end B
            p_arrow = Arrow([sx(3.0), Y_BEAM + 0.9, 0], [sx(3.0), Y_BEAM + 0.1, 0], 
                            color="#EF4444", stroke_width=3, tip_length=0.2, buff=0)
            lbl_p = Text(f"{F_point:.0f} kN", color="#EF4444", weight="BOLD").scale(0.25)
            lbl_p.move_to([sx(3.0) + 0.2, Y_BEAM + 0.9 + 0.15, 0], aligned_edge=LEFT)
            udl_group.add(p_arrow, lbl_p)
            
            return udl_group

        def generate_dimension_lines():
            xp = v_peak_x.get_value()
            dims = VGroup()
            y_dim = Y_BEAM - 1.1
            
            # Static overall dimension
            line_total = Line([sx(0), y_dim, 0], [sx(3.0), y_dim, 0], color="#64748B", stroke_width=1.5)
            t1 = Line([sx(0), y_dim + 0.1, 0], [sx(0), y_dim - 0.1, 0], color="#64748B", stroke_width=1.5)
            t2 = Line([sx(3.0), y_dim + 0.1, 0], [sx(3.0), y_dim - 0.1, 0], color="#64748B", stroke_width=1.5)
            lbl_total = Text("3.0 m", color="#1E293B", weight="BOLD").scale(0.18).next_to(line_total, UP, buff=0.08)
            dims.add(line_total, t1, t2, lbl_total)
            
            # Dynamic dimension for peak position
            if xp > 0.1:
                line_xp = DashedLine([sx(xp), Y_BEAM, 0], [sx(xp), y_dim - 0.5, 0], color="#9CA3AF", stroke_width=1.2, dash_length=0.1)
                t_xp = Line([sx(xp), y_dim - 0.5 + 0.1, 0], [sx(xp), y_dim - 0.5 - 0.1, 0], color="#9CA3AF", stroke_width=1.5)
                line_dim_xp = Line([sx(0), y_dim - 0.5, 0], [sx(xp), y_dim - 0.5, 0], color="#9CA3AF", stroke_width=1.2)
                lbl_xp = Text(f"{xp:.1f} m", color="#1E293B", weight="BOLD").scale(0.18).next_to(line_dim_xp, DOWN, buff=0.08)
                dims.add(line_xp, t_xp, line_dim_xp, lbl_xp)
            
            return dims

        self.add(stable_redraw(generate_udl_graphics))
        self.add(stable_redraw(generate_dimension_lines))

        # ==========================================================
        # ALIGNMENT LINES & FIXED SUPPORT
        # ==========================================================
        def draw_alignment_lines():
            g = VGroup()
            # Fixed supports at 0, free at L
            for x_val in [0, L]:
                g.add(DashedLine(start=[sx(x_val), Y_TOP_ALIGN, 0], end=[sx(x_val), Y_BOTTOM_ALIGN, 0],
                                 color="#CBD5E1", stroke_width=1.2, dash_length=0.12))
            return g

        self.add(draw_alignment_lines())

        def draw_fixed_support():
            # Wall visualization
            wall = Polygon(
                [sx(0) - 0.1, Y_BEAM + 0.6, 0], [sx(0), Y_BEAM + 0.6, 0],
                [sx(0), Y_BEAM - 0.6, 0], [sx(0) - 0.1, Y_BEAM - 0.6, 0],
                fill_color="#E2E8F0", fill_opacity=1, stroke_width=0
            )
            # Support plate
            wall_plate = Rectangle(width=0.08, height=1.2, fill_color="#CBD5E1", stroke_color="#64748B", stroke_width=1).move_to([sx(0) - 0.04, Y_BEAM, 0])
            # Connection dots
            dots = VGroup(*[Circle(radius=0.02, color="#1E293B", fill_opacity=1) for _ in range(4)])
            dots.arrange_in_grid(2, 2, buff=0.1).move_to([sx(0) - 0.04, Y_BEAM, 0])
            
            g = VGroup(wall, wall_plate, dots)
            return g

        self.add(draw_fixed_support())

        neutral_axis = DashedLine(start=[sx(0), Y_BEAM, 0], end=[sx(L), Y_BEAM, 0], 
                                 color="#9CA3AF", stroke_width=1.5, dash_length=0.08)
        self.add(neutral_axis)

        # ==========================================================
        # DEFORMATION ENGINE
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
            xp = v_peak_x.get_value()
            RA, MA = reactions()
            # Show dynamic RA and clockwise Moment MA
            t1 = Text(f"RA = {RA:.1f} kN", color="#D97706", weight="BOLD").scale(0.25).move_to([sx(0) - 0.5, Y_BEAM + 0.5, 0], aligned_edge=RIGHT)
            
            # Reaction moment label. Clockwise MA
            m_arrow = Arc(radius=0.35, start_angle=-20*DEGREES, angle=220*DEGREES, color="#D97706", stroke_width=2.5)
            m_arrow.add_tip(tip_shape=StealthTip, tip_length=0.2).move_to([sx(0), Y_BEAM, 0])
            
            t2 = Text(f"MA = {MA:.1f} kNm", color="#D97706", weight="BOLD").scale(0.25).next_to(m_arrow, LEFT, buff=0.1).set_y(Y_BEAM-0.4)
            
            # Point load RA visualization
            ra_arrow = Arrow([sx(0), Y_BEAM - 0.9, 0], [sx(0), Y_BEAM - 0.1, 0], 
                            color="#D97706", stroke_width=3, tip_length=0.2, buff=0)
            
            return VGroup(t1, t2, m_arrow, ra_arrow)

        self.add(stable_redraw(render_reactions))

        # ==========================================================
        # DIAGRAM ENGINES
        # ==========================================================
        
        def create_sfd_diagram():
            xp = v_peak_x.get_value()
            nodes = sorted(list(set([0.0, xp, 3.0])))
            clean_nodes = [nodes[0]]
            for n in nodes[1:]:
                if n - clean_nodes[-1] > 1e-3: clean_nodes.append(n)
            nodes = clean_nodes

            outline_pts = []
            for i in range(len(nodes) - 1):
                x_start, x_end = nodes[i], nodes[i+1]
                segment_xs = np.linspace(x_start, x_end, 30)
                for x in segment_xs:
                    outline_pts.append([sx(x), Y_SFD + shear(x) * SHEAR_SCALE, 0])
                
                # Check for point load at end B (F_point = 3.0)
                if x_end >= 3.0 - 1e-5:
                    outline_pts.append([sx(3.0), Y_SFD + shear(3.0) * SHEAR_SCALE, 0]) # continuous decrease to 3
                    # Manual jump due to point load drop at free end
                    outline_pts.append([sx(3.0), Y_SFD + (shear(3.0) - F_point) * SHEAR_SCALE, 0]) # drop to 0

            # Fill shape definition
            fill_pts = [[sx(0), Y_SFD, 0]] + outline_pts + [[sx(3.0), Y_SFD, 0]]
            fill_obj = Polygon(*fill_pts, stroke_width=0, fill_color="#0284C7", fill_opacity=0.15)
            
            # Diagram Outline (with jump for standard display)
            diagram_line_pts = outline_pts
            line_obj = VMobject(color="#0284C7", stroke_width=2.5).set_points_as_corners(diagram_line_pts)
            
            # Value Labels
            lbl_start = Text(f"12.0", color="#0284C7", weight="BOLD").scale(0.18).next_to(line_obj, UP, buff=0.1).set_x(sx(0))
            lbl_end = Text(f"{3.0:.1f}", color="#0284C7", weight="BOLD").scale(0.18).next_to(line_obj, UP, buff=0.1).set_x(sx(3.0))
            
            return VGroup(fill_obj, line_obj, lbl_start, lbl_end)

        def create_bmd_diagram():
            xp = v_peak_x.get_value()
            nodes = sorted(list(set([0.0, xp, 3.0])))
            clean_nodes = [nodes[0]]
            for n in nodes[1:]:
                if n - clean_nodes[-1] > 1e-3: clean_nodes.append(n)
            nodes = clean_nodes

            outline_pts = []
            for i in range(len(nodes) - 1):
                x_start, x_end = nodes[i], nodes[i+1]
                segment_xs = np.linspace(x_start, x_end, 30)
                for x in segment_xs:
                    # Renders upward for standard negative cantilever bending moment
                    outline_pts.append([sx(x), Y_BMD + moment(x) * MOMENT_SCALE, 0])

            # Fill shape definition.
            fill_pts = [[sx(0), Y_BMD, 0]] + outline_pts + [[sx(3.0), Y_BMD, 0]]
            fill_obj = Polygon(*fill_pts, stroke_width=0, fill_color="#BE185D", fill_opacity=0.15)
            
            diagram_line_pts = outline_pts
            line_obj = VMobject(color="#BE185D", stroke_width=2.5).set_points_as_corners(diagram_line_pts)
            
            # Value Labels
            M_at_0 = moment(0) # e.g., -22.5
            lbl_start = Text(f"{M_at_0:.1f}", color="#BE185D", weight="BOLD").scale(0.18).next_to(line_obj, DOWN, buff=0.1).set_x(sx(0))
            
            return VGroup(fill_obj, line_obj, lbl_start)

        self.add(stable_redraw(create_sfd_diagram))
        self.add(stable_redraw(create_bmd_diagram))

        # ==========================================================
        # ANIMATION SEQUENCE
        # ==========================================================
        self.wait(1.5, frozen_frame=False)

        # Smoothly move peak position from midpoint (1.5m) to near-end (2.5m)
        self.play(
            v_peak_x.animate.set_value(2.5), 
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