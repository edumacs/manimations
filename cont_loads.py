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
        # STRUCTURAL PROPERTIES
        # ==========================================================
        L = 10.0           # Total length of the beam (m)
        EI = 2.4e5
        beam_len = 6.6     # Visual width scaling on screen
        q_load = 15.0      # Continuous Uniformly Distributed Load (UDL) in kN/m
        
        # Dynamic Tracker: Right support starting at the right end (x = L)
        support_B_x = ValueTracker(10.0)

        # Global Layout Scale Matrix
        Y_BEAM = 3.6
        Y_INF  = 0.8
        Y_SFD  = -2.0
        Y_BMD  = -4.8
        
        Y_TOP_ALIGN = 4.8
        Y_BOTTOM_ALIGN = -6.0
        
        # Visual scaling coefficients
        DEFLECTION_VISUAL_SCALE = 65.0
        SHEAR_SCALE = 0.012
        MOMENT_SCALE = 0.006

        x0 = -beam_len / 2
        x1 = beam_len / 2

        def sx(x):
            return x0 + beam_len * x / L

        # ==========================================================
        # DYNAMIC STRUCTURAL MATH ENGINE (LEFT PINNED, RIGHT MOVES)
        # ==========================================================
        def reactions():
            xB = support_B_x.get_value()
            
            # Superposition: UDL over the entire beam [0, L]
            # Sum M_A = 0 -> RB * xB - q_load * L * (L / 2.0) = 0
            RB = (q_load * (L**2) / 2.0) / xB
            RA = (q_load * L) - RB
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
            
            # Subtract the distributed load linearly
            v -= q_load * max(0.0, x)
            return v

        def moment(x):
            xB = support_B_x.get_value()
            RA, RB = reactions()
            
            m = 0
            if x > 0:
                m += RA * x
            if x > xB:
                m += RB * (x - xB)
                
            # Subtract the distributed load moment
            m -= q_load * (x**2) / 2.0
            return m

        def total_deflection(x):
            xB = support_B_x.get_value()
            RA, RB = reactions()
            
            def mac(val): return max(0.0, val)
            
            # Recalculate integration constants as boundary condition y(xB)=0 moves
            C1 = (q_load * (xB**3) / 24.0) - (RA * (xB**2) / 6.0)
            
            term_RA = RA * (x**3) / 6.0
            term_RB = RB * (mac(x - xB)**3) / 6.0
            term_udl = -q_load * (x**4) / 24.0
            
            y = (term_RA + term_RB + term_udl + C1 * x) / EI
            return -y 

        # ==========================================================
        # ULTRA-STABLE REDRAW WRAPPER (FIXED MULTIPLYING GEOMETRY)
        # ==========================================================
        def stable_redraw(func):
            # Generate the first frame immediately to guarantee Frame 0 visibility
            m = func()
            def updater(mob):
                # .become() entirely overwrites the Mobject, stopping the trailing ghost effect
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
        header_sub = Text("BEBAN MERATA KONTINU DENGAN KONDISI BATAS BERGERAK", color="#BE123C").scale(0.25)
        
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
        # DYNAMIC ALIGNMENT LINES & SUPPORTS
        # ==========================================================
        def draw_alignment_lines():
            xB = support_B_x.get_value()
            g = VGroup()
            
            # Static Ends
            for x_val in [0, L]:
                dash = DashedLine(
                    start=[sx(x_val), Y_TOP_ALIGN, 0],
                    end=[sx(x_val), Y_BOTTOM_ALIGN, 0],
                    color="#CBD5E1",
                    stroke_width=1.2,
                    dash_length=0.12
                )
                g.add(dash)
                
            # Dynamic Support B Line
            dynamic_dash = DashedLine(
                start=[sx(xB), Y_TOP_ALIGN, 0],
                end=[sx(xB), Y_BOTTOM_ALIGN, 0],
                color="#EF4444", 
                stroke_width=1.5,
                dash_length=0.08
            )
            g.add(dynamic_dash)
            return g

        self.add(stable_redraw(draw_alignment_lines))

        neutral_axis = DashedLine(
            start=[sx(0), Y_BEAM, 0], 
            end=[sx(L), Y_BEAM, 0], 
            color="#9CA3AF", stroke_width=1.5, dash_length=0.08
        )
        self.add(neutral_axis)

        def draw_supports():
            xB = support_B_x.get_value()
            g = VGroup()
            hinge = Triangle(color="#1E293B", fill_color="#94A3B8", fill_opacity=1).scale(0.14).move_to([sx(0), Y_BEAM - 0.14, 0])
            roller = Circle(color="#1E293B", fill_color="#94A3B8", fill_opacity=1).scale(0.08).move_to([sx(xB), Y_BEAM - 0.08, 0])
            g.add(hinge, roller)
            return g

        self.add(stable_redraw(draw_supports))

        # ==========================================================
        # STATIC UDL GRAPHICS
        # ==========================================================
        def generate_udl_graphics():
            udl_group = VGroup()
            top_line_y = Y_BEAM + 0.4
            top_line = Line([sx(0), top_line_y, 0], [sx(L), top_line_y, 0], color="#0EA5E9", stroke_width=2)
            udl_group.add(top_line)
            
            num_arrows = int(L * 2) 
            for i in range(num_arrows + 1):
                x_pos = sx(i * (L / num_arrows))
                arrow = Arrow(
                    [x_pos, top_line_y, 0], [x_pos, Y_BEAM + 0.05, 0],
                    buff=0, color="#0EA5E9", stroke_width=2, max_tip_length_to_length_ratio=0.25
                )
                udl_group.add(arrow)
            
            lbl = Text(f"BEBAN MERATA: {q_load} kN/m", color="#0EA5E9", weight="BOLD").scale(0.2)
            lbl.next_to(top_line, UP, buff=0.1)
            udl_group.add(lbl)
            return udl_group

        self.add(generate_udl_graphics())

        # ==========================================================
        # DEFORMATION ENGINE
        # ==========================================================
        def draw_dynamic_beam():
            xs = np.linspace(0, L, 100)
            pts = [[sx(x), Y_BEAM - total_deflection(x) * DEFLECTION_VISUAL_SCALE, 0] for x in xs]
            curve = VMobject(color="#16A34A", stroke_width=5)
            curve.set_points_smoothly(pts)
            return curve

        self.add(stable_redraw(draw_dynamic_beam))

        def render_reactions():
            xB = support_B_x.get_value()
            RA, RB = reactions()
            t1 = Text(f"RA = {RA:.1f} kN", color="#D97706", weight="BOLD").scale(0.22).move_to([sx(0), Y_BEAM - 0.45, 0])
            t2 = Text(f"RB = {RB:.1f} kN", color="#D97706", weight="BOLD").scale(0.22).move_to([sx(xB), Y_BEAM - 0.45, 0])
            return VGroup(t1, t2)

        self.add(stable_redraw(render_reactions))

        # ==========================================================
        # INFLUENCE LINE TRACKING SYSTEM (DYNAMIC SHAPE)
        # ==========================================================
        def draw_influence_poly():
            xB = support_B_x.get_value()
            # Influence line for Reaction A due to a shifting support B
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
            nodes = sorted(list(set([0.0, xB, L])))
            clean_nodes = [nodes[0]]
            for n in nodes[1:]:
                if n - clean_nodes[-1] > 1e-3: clean_nodes.append(n)
            nodes = clean_nodes

            outline_pts = []
            eps = 1e-5
            for i in range(len(nodes) - 1):
                x_start, x_end = nodes[i], nodes[i+1]
                v_start = shear(x_start + eps)
                v_end = shear(x_end - eps)
                
                outline_pts.append([sx(x_start), Y_SFD + v_start * SHEAR_SCALE, 0])
                outline_pts.append([sx(x_end), Y_SFD + v_end * SHEAR_SCALE, 0])
                
            if not outline_pts: return VMobject()

            fill_pts = [[sx(0), Y_SFD, 0]] + outline_pts + [[sx(L), Y_SFD, 0]]
            fill_obj = VMobject(stroke_width=0, fill_color="#0284C7", fill_opacity=0.15).set_points_as_corners(fill_pts)
            line_obj = VMobject(color="#0284C7", stroke_width=2.5).set_points_as_corners(outline_pts)
            return VGroup(fill_obj, line_obj)

        def create_bmd_diagram():
            xB = support_B_x.get_value()
            nodes = sorted(list(set([0.0, xB, L])))
            clean_nodes = [nodes[0]]
            for n in nodes[1:]:
                if n - clean_nodes[-1] > 1e-3: clean_nodes.append(n)
            nodes = clean_nodes

            outline_pts = []
            for i in range(len(nodes) - 1):
                x_start, x_end = nodes[i], nodes[i+1]
                segment_xs = np.linspace(x_start, x_end, 30) 
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
        
        # 1. Initial Frame Hold
        self.wait(1.5, frozen_frame=False)

        # 2. Smoothly track Right Support inward towards Middle (L / 2.0 = 5.0)
        self.play(
            support_B_x.animate.set_value(L / 2.0), 
            run_time=6.0, 
            rate_func=smooth
        )
        
        # 3. Final Frame Hold
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