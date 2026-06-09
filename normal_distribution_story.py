from manim import *
import numpy as np

# Set vertical video aspect ratio (9:16)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 10.8
config.frame_height = 19.2

class NormalDistributionStory(Scene):
    """
    Vertical 9:16 educational story for Normal Distribution.
    Render command:
        manim -pqh normal_distribution_story.py NormalDistributionStory
    """

    def construct(self):
        self.camera.background_color = WHITE

        # -------------------------------------------------
        # DATA GENERATION & CALCULATIONS
        # -------------------------------------------------
        np.random.seed(42)
        n_points = 350
        data = np.random.normal(0.0, 1.0, n_points)
        
        # Calculate actual statistics
        actual_mean = np.mean(data)
        actual_median = np.median(data)
        actual_std = np.std(data)
        
        # Measure of Normality
        skewness = np.mean(((data - actual_mean) / actual_std) ** 3)
        excess_kurtosis = np.mean(((data - actual_mean) / actual_std) ** 4) - 3

        # -------------------------------------------------
        # SCENE 1 - THE HOOK (CHAOS)
        # -------------------------------------------------
        title = Text("ORDER FROM CHAOS", color=BLACK, weight=BOLD, font_size=55)
        subtitle = Text("Can pure randomness create a pattern?", color=DARK_GRAY, font_size=32)

        header = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        header.to_edge(UP, buff=1.0)

        self.play(Write(header))

        # Scatter random dots
        dots = VGroup()
        for i in range(n_points):
            d = Dot(
                radius=0.035,
                color=interpolate_color(BLUE_E, BLUE_B, np.random.random()),
            )
            # Randomly place them around the screen initially
            d.move_to([
                np.random.uniform(-4.5, 4.5),
                np.random.uniform(-5, 4),
                0,
            ])
            dots.add(d)

        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.005), run_time=2)
        self.wait(1)

        # -------------------------------------------------
        # SCENE 2 - THE CONNECTION (DOTS TO BINS)
        # -------------------------------------------------
        pattern_text = Text("Data falls to its true value...", color=BLACK, font_size=36)
        pattern_text.next_to(header, DOWN, buff=0.8)

        # Create Axes
        ax = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=9,
            y_length=6,
            axis_config={"color": BLACK, "include_numbers": False},
        ).shift(DOWN * 2)

        x_labels = ax.get_x_axis().add_numbers(
            [-3, -2, -1, 0, 1, 2, 3], 
            font_size=24, 
            color=BLACK
        )

        self.play(
            Transform(subtitle, pattern_text),
            Create(ax), 
            Write(x_labels)
        )

        # Animate dots falling to their actual X-coordinates on the axis
        # We give them a tiny random Y offset so they stack nicely into a "pile"
        drop_animations = []
        for i, d in enumerate(dots):
            target_pos = ax.c2p(data[i], np.random.uniform(0.01, 0.08))
            drop_animations.append(d.animate.move_to(target_pos))
        
        self.play(AnimationGroup(*drop_animations, lag_ratio=0.005), run_time=2.5)
        self.wait(0.5)

        # Create Histogram Bars
        bins = np.linspace(-4, 4, 31)
        hist, _ = np.histogram(data, bins=bins, density=True)
        bars = VGroup()

        for i, h in enumerate(hist):
            x = (bins[i] + bins[i + 1]) / 2
            r = Rectangle(
                width=ax.x_length / len(hist) * 0.9,
                height=max(ax.c2p(0, h)[1] - ax.c2p(0, 0)[1], 0.01),
                fill_color=BLUE_C,
                fill_opacity=0.8,
                stroke_width=1,
                stroke_color=BLUE_E
            )
            r.move_to(ax.c2p(x, 0), aligned_edge=DOWN)
            bars.add(r)

        # Morph the clustered dots directly into the histogram bars
        self.play(
            Transform(dots, bars),
            run_time=2
        )
        self.wait(1)

        # -------------------------------------------------
        # SCENE 3 - THE ABSTRACTION (BELL CURVE)
        # -------------------------------------------------
        curve_text = Text("The underlying Normal Distribution", color=RED_E, font_size=36, weight=BOLD)
        curve_text.move_to(pattern_text)

        def pdf(x):
            return (1 / (actual_std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - actual_mean) / actual_std) ** 2)

        curve = ax.plot(pdf, x_range=[-4, 4], color=RED_E, stroke_width=6)

        self.play(
            Transform(subtitle, curve_text),
            Create(curve),
            dots.animate.set_opacity(0.3), # dots are now the bars due to Transform
            run_time=2
        )
        self.wait(1)

        # -------------------------------------------------
        # SCENE 4 - CALCULATIONS & NORMALITY MEASURE
        # -------------------------------------------------
        self.play(FadeOut(header), FadeOut(subtitle))

        # Dashboard UI
        dash_rect = RoundedRectangle(
            width=9.5, height=3.5, corner_radius=0.2, 
            fill_color="#F8FAFC", fill_opacity=1, stroke_color=DARK_GRAY
        ).to_edge(UP, buff=0.8)

        dash_title = Text("Diagnostics & Normality", color=BLACK, font_size=32, weight=BOLD)
        dash_title.next_to(dash_rect.get_top(), DOWN, buff=0.2)

        # Statistics Text
        col1 = VGroup(
            Text(f"Mean: {actual_mean:.3f}", color=DARK_BROWN, font_size=28),
            Text(f"Median: {actual_median:.3f}", color=TEAL_E, font_size=28),
            Text(f"Std Dev (\u03c3): {actual_std:.3f}", color=RED_E, font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        col2 = VGroup(
            Text(f"Skewness: {skewness:.3f}", color=BLACK, font_size=28),
            Text("(Ideal Normal = 0.0)", color=DARK_GRAY, font_size=22),
            Text(f"Exc. Kurtosis: {excess_kurtosis:.3f}", color=BLACK, font_size=28),
            Text("(Ideal Normal = 0.0)", color=DARK_GRAY, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        stats_group = VGroup(col1, col2).arrange(RIGHT, buff=0.8).next_to(dash_title, DOWN, buff=0.3)
        dashboard = VGroup(dash_rect, dash_title, stats_group)

        self.play(FadeIn(dash_rect), Write(dash_title))
        self.play(Write(col1), Write(col2))

        # Visualize Mean vs Median alignment
        mean_line = ax.get_vertical_line(ax.c2p(actual_mean, pdf(actual_mean)), color=DARK_BROWN, stroke_width=4)
        median_line = ax.get_vertical_line(ax.c2p(actual_median, pdf(actual_median)), color=TEAL_E, stroke_width=4, line_func=DashedLine)
        
        # They will overlap almost perfectly, proving the distribution is not skewed
        self.play(Create(mean_line))
        self.play(Create(median_line))
        
        overlap_note = Text("Mean ≈ Median (Zero Skew)", color=BLACK, font_size=28)
        overlap_note.next_to(ax, DOWN, buff=0.8)
        self.play(Write(overlap_note))
        self.wait(3)

        # -------------------------------------------------
        # SCENE 5 - OUTRO
        # -------------------------------------------------
        outro_text = Text("Perfect order, proven by numbers.", color=BLACK, font_size=40, weight=BOLD)
        outro_text.to_edge(DOWN, buff=1.0)

        self.play(Transform(overlap_note, outro_text))
        self.wait(3)