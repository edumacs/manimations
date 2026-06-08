from manim import *
import numpy as np

# =========================
# KONFIGURASI VIDEO 9:16
# =========================
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920

class FractionAdditionVertical(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # =========================
        # TITLE
        # =========================
        title = Text("Penjumlahan Pecahan", color=BLACK, weight=BOLD).scale(0.7).to_edge(UP, buff=0.6)
        self.play(Write(title))

        # ==========================================
        # SCENE AWAL: TAMPILKAN SOAL
        # ==========================================
        question = MathTex(
            r"\frac{2}{7} + \frac{1}{3} = \dots", 
            color=BLACK
        ).scale(1.8)
        
        self.play(Write(question))
        self.wait(1.5)
        self.play(FadeOut(question))
        self.wait(0.5)

        # =========================
        # KONFIGURASI VISUAL
        # =========================
        RADIUS = 2
        VERTICAL_GAP = 1.0  
        TOP_POS = UP * (RADIUS + VERTICAL_GAP)
        MID_POS = DOWN * (RADIUS + VERTICAL_GAP)
        SW = 2
        LABEL_RES = 0.35

        def get_sector_center_pos(n, i, start_idx, radius_offset, base_pos):
            angle = (i + start_idx + 0.5) * (TAU / n)
            rel_pos = np.array([np.cos(angle) * RADIUS * radius_offset, np.sin(angle) * RADIUS * radius_offset, 0])
            return base_pos + rel_pos

        def create_sectors(n, fill_count, color, pos, start_idx=0):
            group = VGroup()
            for i in range(n):
                is_filled = i < fill_count
                s = Sector(
                    radius=RADIUS,
                    start_angle=(i + start_idx) * TAU / n,
                    angle=TAU / n,
                    stroke_color=BLACK,
                    stroke_width=SW,
                    fill_color=color if is_filled else WHITE,
                    fill_opacity=0.8 if is_filled else 1
                ).shift(pos)
                group.add(s)
            return group

        # =========================
        # STEP 1 & 2 — Tampilkan 2/7 dan 1/3
        # =========================
        frac1 = MathTex(r"\frac{2}{7}", color=BLACK).next_to(TOP_POS, UP)
        circle1 = Circle(radius=RADIUS, color=BLACK, stroke_width=SW).shift(TOP_POS)
        sectors_7 = create_sectors(7, 2, YELLOW, TOP_POS)

        frac2 = MathTex(r"\frac{1}{3}", color=BLACK).next_to(MID_POS, UP)
        circle2 = Circle(radius=RADIUS, color=BLACK, stroke_width=SW).shift(MID_POS)
        sectors_3 = create_sectors(3, 1, PURPLE, MID_POS)

        self.play(Create(circle1), Create(circle2))
        self.play(
            LaggedStart(*[Create(s) for s in sectors_7], lag_ratio=0.1),
            LaggedStart(*[Create(s) for s in sectors_3], lag_ratio=0.1)
        )
        self.play(Write(frac1), Write(frac2))
        self.wait(1)

        # ==========================================
        # STEP 3 — SAMAKAN PENYEBUT & UPDATE LABEL
        # ==========================================
        subtitle = Text("Samakan penyebut → 21", color=GRAY_D).scale(0.5).next_to(title, DOWN)
        self.play(FadeIn(subtitle))

        sectors_21_top = create_sectors(21, 6, YELLOW, TOP_POS)
        sectors_21_mid = create_sectors(21, 7, PURPLE, MID_POS, start_idx=6)
        
        # New Labels
        frac1_new = MathTex(r"\frac{6}{21}", color=BLACK).move_to(frac1.get_center())
        frac2_new = MathTex(r"\frac{7}{21}", color=BLACK).move_to(frac2.get_center())

        self.play(
            ReplacementTransform(sectors_7, sectors_21_top),
            ReplacementTransform(sectors_3, sectors_21_mid),
            ReplacementTransform(frac1, frac1_new),
            ReplacementTransform(frac2, frac2_new),
            run_time=2
        )

        # =========================
        # STEP 4 — NOMOR
        # =========================
        numbers = VGroup()
        for i in range(6):
            pos = get_sector_center_pos(21, i, 0, 0.7, TOP_POS)
            numbers.add(Text(str(i + 1), color=BLACK).scale(LABEL_RES).move_to(pos))
        for i in range(7):
            pos = get_sector_center_pos(21, i, 6, 0.7, MID_POS)
            numbers.add(Text(str(i + 7), color=BLACK).scale(LABEL_RES).move_to(pos))

        self.play(LaggedStart(*[FadeIn(n) for n in numbers], lag_ratio=0.1))
        self.wait(0.8)

        # ==========================================
        # STEP 5 — GABUNGKAN & BERSIHKAN LABEL LAMA
        # ==========================================
        purple_parts = VGroup(*sectors_21_mid[:7], *numbers[6:])

        self.play(
            purple_parts.animate.shift(TOP_POS - MID_POS),
            FadeOut(sectors_21_mid[7:]),
            FadeOut(circle2),
            FadeOut(frac2_new), # Remove the middle label
            FadeOut(frac1_new), # Remove the top label to make room for result
            run_time=2
        )

        # =========================
        # STEP 6 — HASIL AKHIR
        # =========================
        result = MathTex(
            r"\frac{6}{21} + \frac{7}{21} = \frac{13}{21}",
            color=BLACK
        ).scale(0.9).to_edge(DOWN, buff=1)

        self.play(Write(result))
        self.play(Create(SurroundingRectangle(result, color=BLUE)))
        self.wait(2)