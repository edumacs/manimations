from manim import *
import numpy as np

# ---------------------------------------------------------
# GLOBAL CONFIG (VERTICAL VIDEO)
# ---------------------------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#0e0e11"


class ScanPintarBrandVideo(Scene):
    def construct(self):

        # =====================================================
        # SCENE 3 — CLARITY (INSTANT INSIGHT)
        # =====================================================
        insight = Text(
            "Oh… jadi begitu!",
            font_size=56,
            gradient=(BLUE_B, TEAL_B),
            weight=BOLD
        ).shift(UP * 1.2)

        check = Text(
            "✔",
            font_size=140,
            color=GREEN_C
        ).next_to(insight, DOWN, buff=0.3)

        glow_circle = Circle(
            radius=2.4,
            stroke_color=BLUE_C,
            stroke_width=6
        ).set_opacity(0.4)

        self.play(
            FadeIn(insight, scale=0.9),
            Create(glow_circle),
            run_time=1.2
        )
        self.play(
            FadeIn(check, scale=0.5),
            glow_circle.animate.scale(1.1),
            run_time=0.8
        )

        self.wait(1.2)

        self.play(
            FadeOut(insight),
            FadeOut(check),
            FadeOut(glow_circle)
        )

        # =====================================================
        # SCENE 4 — BRAND REVEAL
        # =====================================================
        logo = Text(
            "ScanPintar",
            font_size=104,
            weight=BOLD,
            gradient=(BLUE_B, TEAL_B)
        ).shift(UP * 1.5)

        tagline = Text(
            "Scan • Paham • Naik Level",
            font_size=36,
            color=GREY_A
        ).next_to(logo, DOWN, buff=0.4)

        underline = Line(
            logo.get_left(),
            logo.get_right(),
            stroke_width=6,
            color=BLUE_C
        ).next_to(logo, DOWN, buff=0.15)

        self.play(
            FadeIn(logo, shift=UP),
            Create(underline),
            FadeIn(tagline),
            run_time=1.5
        )

        self.wait(2)

        # =====================================================
        # SCENE 5 — CTA
        # =====================================================
        cta = Text(
            "Follow untuk belajar\nlebih cerdas\ntanpa ribet",
            font_size=44,
            color=YELLOW
        ).next_to(tagline, DOWN, buff=1)

        icons = VGroup(
            Text("📘", font_size=72),
            Text("🧠", font_size=72),
            Text("🚀", font_size=72),
        ).arrange(RIGHT, buff=0.8)

        icons.next_to(cta, DOWN, buff=0.6)

        self.play(Write(cta))
        self.play(FadeIn(icons, shift=UP))
        self.wait(2.5)

        self.play(
            FadeOut(cta),
            FadeOut(icons),
            logo.animate.scale(1.05),
            run_time=1.5
        )

        self.wait(1)
