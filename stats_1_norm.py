from manim import *
import numpy as np

# ==========================================================
# VERTICAL EDUCATION PLATFORM (9:16) - WHITE BACKGROUND
# ==========================================================
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 10.8
config.frame_height = 19.2

class NormalDistributionStory(Scene):
    def construct(self):
        # Clean White Background
        self.camera.background_color = "#FFFFFF"

        # --- TITLES & WATERMARK ---
        watermark = Text("@ScanPintar", font_size=24, color="#E11D48", weight="BOLD")
        title = Text("ORDER FROM CHAOS", font_size=52, color="#0F172A", weight="BOLD")
        sub_title = Text("Why is it called 'Normal'?", font_size=32, color="#334155")
        
        header_group = VGroup(watermark, title, sub_title).arrange(DOWN, buff=0.25)
        header_group.to_edge(UP, buff=1.0)
        
        self.play(Write(header_group), run_time=1.5)

        # --- DATA GENERATION ---
        np.random.seed(42)
        raw_data = np.random.normal(loc=0.02, scale=0.98, size=1000)
        
        actual_mean = np.mean(raw_data)
        actual_median = np.median(raw_data)
        actual_std = np.std(raw_data)

        # --- STATS DASHBOARD (Dark Box for Contrast) ---
        stats_box = RoundedRectangle(
            width=9.0, height=2.0, corner_radius=0.25,
            fill_color="#1E293B", fill_opacity=1, stroke_width=0
        ).next_to(header_group, DOWN, buff=0.8)
        
        stats_title = Text("DATASET STATISTICS", font_size=18, color="#94A3B8", weight="BOLD")
        stats_title.move_to(stats_box.get_top() + DOWN * 0.4)
        
        # Placeholders
        stat_n = Text("N = 0", font_size=32, color=WHITE)
        stat_mean = Text("Mean = --", font_size=32, color="#F59E0B") # Orange
        stat_median = Text("Median = --", font_size=32, color="#14B8A6") # Teal
        stat_std = Text("Std = --", font_size=32, color="#3B82F6") # Blue
        
        stats_group = VGroup(stat_n, stat_mean, stat_median, stat_std).arrange(RIGHT, buff=0.5)
        stats_group.next_to(stats_title, DOWN, buff=0.4)
        
        self.play(FadeIn(stats_box), FadeIn(stats_title), FadeIn(stats_group))

        # --- AXES SETUP ---
        ax = Axes(
            x_range=[-4.5, 4.5, 1],
            y_range=[0, 0.45, 0.1],
            x_length=8.5,
            y_length=6.0,
            axis_config={"color": "#0F172A", "stroke_width": 3, "include_numbers": False},
            tips=True
        ).move_to([0, -1.0, 0])
        
        # Custom Dark Labels for White Background
        x_labels = VGroup(*[
            Text(str(i), font_size=24, color="#0F172A").next_to(ax.c2p(i, 0), DOWN, buff=0.2)
            for i in range(-4, 5)
        ])
        
        y_label = Text("Relative Frequency", font_size=24, color="#0F172A").rotate(PI/2).next_to(ax, LEFT, buff=0.2)
        x_label = Text("Outcome Range", font_size=24, color="#0F172A").next_to(ax, DOWN, buff=0.8)
        
        self.play(Create(ax), FadeIn(x_labels), FadeIn(y_label), FadeIn(x_label))

        # ==========================================================
        # STEP 1 & 2: CHAOS TO HISTOGRAM
        # ==========================================================
        bins = np.linspace(-4, 4, 31)
        hist_counts, _ = np.histogram(raw_data, bins=bins, density=True)
        
        bars = VGroup()
        for i in range(len(hist_counts)):
            x_start = ax.c2p(bins[i], 0)[0]
            x_end = ax.c2p(bins[i+1], 0)[0]
            bar_width = x_end - x_start
            
            bar = Rectangle(
                width=bar_width * 0.9, height=0.001,
                fill_color="#60A5FA", fill_opacity=0.8, stroke_color="#2563EB", stroke_width=1
            ).move_to(ax.c2p(bins[i] + (bins[i+1]-bins[i])/2, 0), aligned_edge=DOWN)
            bars.add(bar)

        self.add(bars)
        
        # Animated Counter
        def update_n(mob, alpha):
            current_n = int(alpha * 1000)
            mob.become(Text(f"N = {current_n}", font_size=32, color=WHITE).move_to(stat_n))

        # Grow bars
        animations = [
            bar.animate.stretch_to_fit_height(
                max(ax.c2p(0, hist_counts[i])[1] - ax.c2p(0, 0)[1], 0.001)
            ).move_to(ax.c2p(bins[i] + (bins[i+1]-bins[i])/2, 0), aligned_edge=DOWN)
            for i, bar in enumerate(bars)
        ]
        
        self.play(AnimationGroup(*animations, lag_ratio=0.02), UpdateFromAlphaFunc(stat_n, update_n), run_time=3.0)
        self.wait(1)

        # ==========================================================
        # STEP 3: PREDICTABLE CENTER (Mean vs Median)
        # ==========================================================
        new_mean = Text(f"Mean = {actual_mean:.2f}", font_size=32, color="#F59E0B").move_to(stat_mean)
        new_median = Text(f"Median = {actual_median:.2f}", font_size=32, color="#14B8A6").move_to(stat_median)
        new_std = Text(f"Std = {actual_std:.2f}", font_size=32, color="#3B82F6").move_to(stat_std)

        # Orange Mean Line
        mean_line = ax.get_vertical_line(ax.c2p(actual_mean, 0.42), color="#F59E0B", stroke_width=5)
        mean_label = Text("Mean", font_size=28, color="#F59E0B", weight="BOLD").next_to(mean_line, UP, buff=0.1).shift(LEFT*0.6)
        
        # Teal Dashed Median Line
        median_line = DashedLine(
            start=ax.c2p(actual_median, 0), end=ax.c2p(actual_median, 0.42), 
            color="#14B8A6", stroke_width=5, dash_length=0.1
        )
        median_label = Text("Median", font_size=28, color="#14B8A6", weight="BOLD").next_to(median_line, UP, buff=0.1).shift(RIGHT*0.7)

        self.play(Transform(stat_mean, new_mean), Transform(stat_median, new_median), Transform(stat_std, new_std))
        self.play(Create(mean_line), FadeIn(mean_label))
        self.play(Create(median_line), FadeIn(median_label))
        self.wait(1.5)

        # ==========================================================
        # STEP 4: THE NORMAL CURVE
        # ==========================================================
        def pdf(x):
            return (1 / (actual_std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - actual_mean) / actual_std) ** 2)
        
        # Red Curve
        theoretical_curve = ax.plot(pdf, x_range=[-4.2, 4.2], color="#E11D48", stroke_width=6)
        
        self.play(Create(theoretical_curve), bars.animate.set_opacity(0.4), run_time=2.5)
        self.wait(2)

        # --- EXPLANATION TEXT (Bottom) ---
        footer_bg = Rectangle(width=10.8, height=4.5, fill_color="#F8FAFC", fill_opacity=1, stroke_width=0).to_edge(DOWN, buff=0)
        self.play(FadeIn(footer_bg))

        exp_1 = Text("1. RANDOM DATA (Chaos) forms the blue bars.", font_size=22, color="#0F172A")
        exp_2 = Text("2. ORDER EMERGES: The data clumps in the middle.", font_size=22, color="#0F172A")
        exp_3 = Text("3. PREDICTABLE CENTER: Mean and Median overlap.", font_size=22, color="#0F172A")
        exp_4 = Text("4. THE PATTERN: Extreme highs/lows are perfectly rare.", font_size=22, color="#0F172A")
        exp_5 = Text("This predictable shape is the 'Normal Distribution'.", font_size=24, color="#E11D48", weight="BOLD")

        exp_group = VGroup(exp_1, exp_2, exp_3, exp_4, exp_5).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        exp_group.move_to(footer_bg.get_center())

        self.play(Write(exp_group), run_time=3)
        self.wait(3)