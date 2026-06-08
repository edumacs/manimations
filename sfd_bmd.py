from manim import *
import numpy as np

# ==========================================================
# ADVANCED STRUCTURAL ANALYSIS PLATFORM ENGINE (DARK MODE)
# ==========================================================

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8

class MovingTruckBeam(Scene):
    def construct(self):
        # Premium dark slate workspace background
        self.camera.background_color = "#0F172A"

        # Structural Properties
        L = 10.0
        EI = 2.4e5
        beam_len = 6.6

        # Fixed Global Layout Scale Matrix (Prevents layout jumping)
        Y_BEAM = 4.2
        Y_INF  = 1.4
        Y_SFD  = -1.4
        Y_BMD  = -4.2
        
        # Scaling coefficients for stable visual sizing
        DEFLECTION_VISUAL_SCALE = 35.0
        SHEAR_SCALE = 0.0025
        MOMENT_SCALE = 0.0012

        x0 = -beam_len / 2
        x1 = beam_len / 2

        # ValueTracker for linear vehicle movement
        truck_x = ValueTracker(-4.5)

        axles = [
            (80, 0.0),   # (Axle Load kN, Distance from Rear Axle m)
            (120, 1.4),
            (120, 2.8),
            (80, 4.2),
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
            RB = sum(P * x / L for P, x in loads)
            RA = sum(P for P, _ in loads) - RB
            return RA, RB

        def shear(x):
            RA, _ = reactions()
            v = RA
            for P, xp in active_loads():
                if x >= xp:
                    v -= P
            return v

        def moment(x):
            RA, _ = reactions()
            m = RA * x
            for P, xp in active_loads():
                if x >= xp:
                    m -= P * (x - xp)
            return m

        def compute_single_deflection(x, P, a):
            b = L - a
            if x <= a:
                return P * b * x * (L**2 - b**2 - x**2) / (6 * L * EI)
            else:
                return P * a * (L - x) * (L**2 - a**2 - (L - x)**2) / (6 * L * EI)

        def total_deflection(x):
            return sum(compute_single_deflection(x, P, a) for P, a in active_loads())

        # ==========================================================
        # ULTRA-STABLE HIGH PERFORMANCE REDRAW ENGINE
        # ==========================================================
        def stable_redraw(func):
            """Bypasses .become() structural mismatch errors by clearing 
            and rebuilding the VGroup array pipeline explicitly every frame."""
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
        # MODERN COMPONENT UI FRAMES
        # ==========================================================
        def create_plot_frame(center_y, label, accent_color):
            frame = RoundedRectangle(
                width=7.4, height=2.4, corner_radius=0.12,
                stroke_color="#334155", stroke_width=1.5,
                fill_color="#1E293B", fill_opacity=0.9
            ).move_to([0, center_y, 0])
            
            accent_tag = Rectangle(
                width=0.08, height=0.35,
                fill_color=accent_color, fill_opacity=1, stroke_width=0
            ).move_to([x0 - 0.25, center_y + 0.95, 0], aligned_edge=LEFT)

            title_text = Text(label, color="#94A3B8", weight="BOLD").scale(0.18)
            title_text.move_to([x0 - 0.1, center_y + 0.95, 0], aligned_edge=LEFT)
            
            axis_line = Line([x0, center_y, 0], [x1, center_y, 0], color="#475569", stroke_width=1.5)
            return VGroup(frame, accent_tag, title_text, axis_line)

        # Main Header (Shifted Down & Radiant Neon Aesthetics)
        header_title = Text("LIVE LOAD FINITE ELEMENT METRICS", color="#00F2FF", weight="BOLD").scale(0.38)
        header_sub = Text("REAL-TIME MOVING LOAD ANALYSIS", color="#FF007F").scale(0.22)
        
        header_title.to_edge(UP, buff=0.8) 
        header_sub.next_to(header_title, DOWN, buff=0.1)
        self.add(header_title, header_sub)

        # Watermark Label @ScanPintar (Vibrant Electric Cyan)
        watermark = Text("@ScanPintar", color="#00F2FF", weight="BOLD").scale(0.25)
        watermark.to_corner(DR, buff=0.4)
        self.add(watermark)

        # Inject Dashboard Components
        self.add(create_plot_frame(Y_BEAM, "STRUCTURE DEFORMATION SYSTEM", "#10B981"))
        self.add(create_plot_frame(Y_INF, "INFLUENCE LINE DESIGN MATRIX (RA)", "#F59E0B"))
        self.add(create_plot_frame(Y_SFD, "SHEAR FORCE DIAGRAM (SFD)", "#0EA5E9"))
        self.add(create_plot_frame(Y_BMD, "BENDING MOMENT DIAGRAM (BMD)", "#EC4899"))

        # Reference Neutral Axis
        neutral_axis = DashedLine(
            start=[x0, Y_BEAM, 0], 
            end=[x1, Y_BEAM, 0], 
            color="#475569", 
            stroke_width=1.5, 
            dash_length=0.08
        )
        self.add(neutral_axis)

        # ==========================================================
        # DYNAMIC DEFORMING STRUCTURAL ELEMENT & PEAK CALLOUT
        # ==========================================================
        def draw_dynamic_beam():
            xs = np.linspace(0, L, 60)
            pts = [[sx(x), Y_BEAM - total_deflection(x) * DEFLECTION_VISUAL_SCALE, 0] for x in xs]
            curve = VMobject(color="#10B981", stroke_width=5)
            curve.set_points_smoothly(pts)
            return curve

        def draw_peak_deflection_label():
            xs = np.linspace(0, L, 100)
            defs = [total_deflection(x) for x in xs]
            max_idx = np.argmax(defs)
            max_x = xs[max_idx]
            max_def_m = defs[max_idx]
            max_def_mm = max_def_m * 1000  # Convert to mm

            if max_def_mm > 0.1:
                y_pos = Y_BEAM - max_def_m * DEFLECTION_VISUAL_SCALE
                dot = Dot([sx(max_x), y_pos, 0], radius=0.04, color="#34D399")
                lbl = Text(f"{max_def_mm:.1f} mm", color="#34D399", weight="BOLD").scale(0.14)
                lbl.next_to(dot, DOWN, buff=0.08)
                return VGroup(dot, lbl)
            return VMobject()

        self.add(stable_redraw(draw_dynamic_beam))
        self.add(stable_redraw(draw_peak_deflection_label))

        # Modern Minimal Boundary Support Icons
        hinge = Triangle(color="#64748B", fill_color="#334155", fill_opacity=1).scale(0.14).move_to([x0, Y_BEAM - 0.14, 0])
        roller = Circle(color="#64748B", fill_color="#334155", fill_opacity=1).scale(0.08).move_to([x1, Y_BEAM - 0.08, 0])
        self.add(hinge, roller)

        # ==========================================================
        # KINEMATIC VEHICLE BLUEPRINT ASSET (STRAIGHT HORIZONTAL)
        # ==========================================================
        def draw_truck():
            g = VGroup()
            t_x = truck_x.get_value()
            
            rear_screen_x = sx(t_x - 0.3)
            front_screen_x = sx(t_x + 4.5)
            cabin_screen_x = sx(t_x + 3.2)
            
            base_y = Y_BEAM

            # Elegant Flat Chassis Blueprint Design
            bed = Rectangle(
                width=cabin_screen_x - rear_screen_x, height=0.5,
                fill_color="#334155", fill_opacity=0.85,
                stroke_color="#64748B", stroke_width=1.5
            ).move_to([(cabin_screen_x + rear_screen_x) / 2, base_y + 0.4, 0])

            cabin = Rectangle(
                width=front_screen_x - cabin_screen_x, height=0.8,
                fill_color="#475569", fill_opacity=0.9,
                stroke_color="#94A3B8", stroke_width=1.5
            ).move_to([(front_screen_x + cabin_screen_x) / 2, base_y + 0.55, 0])
            
            window = Rectangle(
                width=0.4, height=0.35, fill_color="#0F172A", fill_opacity=1, stroke_width=0
            ).move_to([front_screen_x - 0.35, base_y + 0.7, 0])
            
            g.add(bed, cabin, window)

            # Wheels and Vector Point Loads Placement Engine
            for P, off in axles:
                axle_pos = t_x + off
                wheel_x = sx(axle_pos)
                wheel_y = Y_BEAM

                wheel = Circle(radius=0.1, color="#1E293B", fill_color="#0F172A", fill_opacity=1, stroke_width=2)
                wheel.move_to([wheel_x, wheel_y + 0.05, 0])
                center_dot = Circle(radius=0.02, color="#94A3B8", fill_color="#94A3B8", fill_opacity=1)
                center_dot.move_to(wheel.get_center())
                g.add(wheel, center_dot)

                if 0 <= axle_pos <= L:
                    arrow = Arrow(
                        [wheel_x, wheel_y + 1.2, 0],
                        [wheel_x, wheel_y + 0.16, 0],
                        buff=0, color="#EF4444", stroke_width=4, max_tip_length_to_length_ratio=0.15
                    )
                    txt = Text(f"{P}k", color="#EF4444", weight="BOLD").scale(0.12)
                    txt.next_to(arrow, UP, buff=0.04)
                    g.add(arrow, txt)

            return g

        self.add(stable_redraw(draw_truck))

        # ==========================================================
        # REAL-TIME LIVE BOUNDARY TELEMETRY
        # ==========================================================
        def render_reactions():
            RA, RB = reactions()
            t1 = Text(f"RA = {RA:.1f} kN", color="#F59E0B", weight="BOLD").scale(0.16).move_to([x0 + 0.5, Y_BEAM - 0.45, 0])
            t2 = Text(f"RB = {RB:.1f} kN", color="#F59E0B", weight="BOLD").scale(0.16).move_to([x1 - 0.5, Y_BEAM - 0.45, 0])
            return VGroup(t1, t2)

        self.add(stable_redraw(render_reactions))

        # ==========================================================
        # INFLUENCE LINE TRACKING SYSTEM
        # ==========================================================
        infl_poly = Polygon(
            [x0, Y_INF, 0], [x0, Y_INF + 0.8, 0], [x1, Y_INF, 0],
            fill_color="#F59E0B", fill_opacity=0.1, stroke_color="#F59E0B", stroke_width=1.5
        )
        self.add(infl_poly)

        def draw_influence_marker():
            loads = active_loads()
            if not loads:
                return VMobject()
            leading_x = loads[0][1]
            y_val = (1 - leading_x / L) * 0.8
            dot = Dot([sx(leading_x), Y_INF + y_val, 0], color="#F59E0B", radius=0.05)
            val_lbl = Text(f"η = {1-(leading_x/L):.2f}", color="#F59E0B", weight="BOLD").scale(0.14)
            val_lbl.next_to(dot, UP, buff=0.06)
            return VGroup(dot, val_lbl)

        self.add(stable_redraw(draw_influence_marker))

        # ==========================================================
        # VECTOR STEP-DIAGRAM AND SHARP PEAK ENGINES
        # ==========================================================
        def create_sfd_diagram():
            loads = active_loads()
            nodes = [0]
            for _, xp in loads:
                if 0 < xp < L:
                    nodes.append(xp)
            nodes.append(L)
            nodes = sorted(list(set(nodes)))

            outline_pts = []
            for i in range(len(nodes) - 1):
                x_start, x_end = nodes[i], nodes[i+1]
                v = shear((x_start + x_end) / 2)
                outline_pts.append([sx(x_start), Y_SFD + v * SHEAR_SCALE, 0])
                outline_pts.append([sx(x_end), Y_SFD + v * SHEAR_SCALE, 0])

            if not outline_pts:
                return VMobject()

            fill_pts = [[sx(0), Y_SFD, 0]] + outline_pts + [[sx(L), Y_SFD, 0]]
            fill_obj = VMobject(stroke_width=0, fill_color="#0EA5E9", fill_opacity=0.15).set_points_as_corners(fill_pts)
            line_obj = VMobject(color="#0EA5E9", stroke_width=2.5).set_points_as_corners(outline_pts)
            g = VGroup(fill_obj, line_obj)

            # Max Absolute Value Tracker Callout
            xs_eval = np.linspace(0, L, 100)
            v_eval = [shear(x) for x in xs_eval]
            p_idx = np.argmax([abs(v) for v in v_eval])
            if abs(v_eval[p_idx]) > 2.0:
                dot = Dot([sx(xs_eval[p_idx]), Y_SFD + v_eval[p_idx] * SHEAR_SCALE, 0], radius=0.04, color="#FFFFFF")
                lbl = Text(f"{v_eval[p_idx]:.1f} kN", color="#F8FAFC", weight="BOLD").scale(0.14)
                lbl.next_to(dot, UP if v_eval[p_idx] >= 0 else DOWN, buff=0.08)
                g.add(dot, lbl)
            return g

        def create_bmd_diagram():
            loads = active_loads()
            nodes = [0]
            for _, xp in loads:
                if 0 < xp < L:
                    nodes.append(xp)
            nodes.append(L)
            nodes = sorted(list(set(nodes)))

            outline_pts = [[sx(x), Y_BMD + moment(x) * MOMENT_SCALE, 0] for x in nodes]
            fill_pts = [[sx(0), Y_BMD, 0]] + outline_pts + [[sx(L), Y_BMD, 0]]
            
            fill_obj = VMobject(stroke_width=0, fill_color="#EC4899", fill_opacity=0.15).set_points_as_corners(fill_pts)
            line_obj = VMobject(color="#EC4899", stroke_width=2.5).set_points_as_corners(outline_pts)
            g = VGroup(fill_obj, line_obj)

            vals = [moment(x) for x in nodes]
            if vals:
                p_idx = np.argmax([abs(v) for v in vals])
                if abs(vals[p_idx]) > 2.0:
                    dot = Dot([sx(nodes[p_idx]), Y_BMD + vals[p_idx] * MOMENT_SCALE, 0], radius=0.04, color="#FFFFFF")
                    lbl = Text(f"{vals[p_idx]:.1f} kNm", color="#F8FAFC", weight="BOLD").scale(0.14)
                    lbl.next_to(dot, UP if vals[p_idx] >= 0 else DOWN, buff=0.08)
                    g.add(dot, lbl)
            return g

        # Stable and responsive diagram injection pipeline
        self.add(stable_redraw(create_sfd_diagram))
        self.add(stable_redraw(create_bmd_diagram))

        # ==========================================================
        # ANIMATION SEQUENCE PLAYBACK EXECUTION
        # ==========================================================
        self.wait(0.5)
        self.play(
            truck_x.animate.set_value(L + 0.2),
            run_time=14,
            rate_func=linear
        )
        self.wait(1.0)