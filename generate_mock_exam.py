"""
Generates:
  Karnika_Mock_Exam.pdf         - student copy (no answers)
  Karnika_Mock_Exam_Answers.pdf - teacher answer key
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Colour palette (RGB)
C_BLUE   = (30,  80, 160)
C_LBLUE  = (220, 232, 255)
C_GREEN  = (20, 130,  60)
C_LGREEN = (220, 245, 225)
C_ORANGE = (200,  80,   0)
C_LORANG = (255, 235, 210)
C_GRAY   = (50,  50,  50)
C_LGRAY  = (240, 240, 240)
C_WHITE  = (255, 255, 255)
C_YELLOW = (255, 250, 220)
LM = 20   # left margin
RM = 20   # right margin
PW = 170  # printable width


class ExamPDF(FPDF):
    def __init__(self, answers=False):
        super().__init__()
        self.answers = answers
        self.set_margins(LM, 25, RM)
        self.set_auto_page_break(True, margin=20)

    def header(self):
        self.set_fill_color(*C_BLUE)
        self.rect(0, 0, 210, 20, "F")
        self.set_xy(0, 3)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*C_WHITE)
        self.cell(210, 7, "Grade 5 Mathematics - Mock Exam", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 9)
        tag = "ANSWER KEY" if self.answers else "Term 2 | Measurements, Conversions & Problem Solving"
        self.cell(210, 5, tag, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*C_GRAY)
        self.set_y(26)

    def footer(self):
        self.set_y(-13)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        note = "  ANSWER KEY - Not for student distribution" if self.answers else ""
        self.cell(0, 5, f"Page {self.page_no()}{note}", align="C")
        self.set_text_color(*C_GRAY)

    # ── helpers ───────────────────────────────────────────────────────────────

    def section_heading(self, text):
        self.ln(3)
        self.set_fill_color(*C_LBLUE)
        self.set_draw_color(*C_BLUE)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*C_BLUE)
        self.cell(PW, 9, "  " + text, border="LB", fill=True,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*C_GRAY)
        self.ln(3)

    def italic_note(self, text):
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(PW, 5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*C_GRAY)
        self.ln(1)

    def dotted_line(self, w=PW):
        self.set_draw_color(160, 160, 160)
        self.set_font("Helvetica", "", 11)
        self.cell(w, 7, "", border="B", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def answer_cell(self, text, w=60):
        """Green highlighted answer (teacher version)."""
        self.set_fill_color(*C_YELLOW)
        self.set_draw_color(*C_GREEN)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*C_GREEN)
        self.cell(w, 7, "  " + text, border=1, fill=True,
                  new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.set_text_color(*C_GRAY)

    def blank_cell(self, w=60):
        """Dotted blank line (student version)."""
        dots = "." * max(1, int(w * 0.65))
        self.set_font("Helvetica", "", 11)
        self.cell(w, 7, dots, new_x=XPos.RIGHT, new_y=YPos.LAST)

    def work_box(self, h=30):
        self.ln(1)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(140, 140, 140)
        self.cell(PW, 4, "Working space:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(200, 200, 200)
        self.set_fill_color(252, 252, 252)
        y0 = self.get_y()
        self.rect(LM, y0, PW, h, "FD")
        # faint ruling lines
        self.set_draw_color(230, 230, 230)
        for i in range(1, int(h / 6)):
            self.line(LM, y0 + i * 6, LM + PW, y0 + i * 6)
        self.set_y(y0 + h + 2)
        self.set_text_color(*C_GRAY)

    def solution_block(self, steps):
        self.ln(1)
        h = 6 * len(steps) + 6
        self.set_fill_color(*C_YELLOW)
        self.set_draw_color(*C_GREEN)
        y0 = self.get_y()
        self.rect(LM, y0, PW, h, "FD")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*C_GREEN)
        self.set_xy(LM + 3, y0 + 2)
        self.cell(PW - 6, 5, "SOLUTION:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 9)
        for step in steps:
            self.set_x(LM + 5)
            self.cell(PW - 10, 6, step, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*C_GRAY)
        self.ln(3)

    def answer_line_row(self, label="Answer:", w=120):
        self.set_font("Helvetica", "B", 10)
        self.cell(35, 7, label)
        if self.answers:
            pass   # solution block already shown above
        else:
            self.set_draw_color(160, 160, 160)
            self.cell(w, 7, "", border="B")
        self.ln(10)

    def conv_row(self, letter, qty, unit, ans):
        self.set_font("Helvetica", "B", 11)
        self.cell(9, 8, letter + ")")
        self.set_font("Helvetica", "", 11)
        self.cell(70, 8, qty + "  =")
        if self.answers:
            self.answer_cell(ans, 75)
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(100, 100, 100)
            self.cell(16, 8, "  " + unit)
            self.set_text_color(*C_GRAY)
        else:
            self.blank_cell(60)
            self.set_font("Helvetica", "", 11)
            self.cell(20, 8, "  " + unit)
        self.ln(10)

    def word_problem(self, number, q_lines, steps, ans_label, work_h=30):
        # question box
        self.set_fill_color(245, 248, 255)
        self.set_draw_color(*C_BLUE)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*C_BLUE)
        self.cell(PW, 7, f"  Question {number}", border="TLR", fill=True,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*C_GRAY)
        self.set_font("Helvetica", "", 11)
        for line in q_lines:
            self.set_x(LM)
            self.set_fill_color(245, 248, 255)
            self.set_draw_color(*C_BLUE)
            self.multi_cell(PW, 6, "  " + line, border="LR", fill=True)
        self.set_fill_color(245, 248, 255)
        self.set_draw_color(*C_BLUE)
        self.cell(PW, 3, "", border="BLR", fill=True,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

        if self.answers:
            self.solution_block(steps)
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*C_GREEN)
            self.cell(PW, 6, "  => " + ans_label,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_text_color(*C_GRAY)
        else:
            self.work_box(work_h)
            self.answer_line_row()

        self.ln(2)

    def ordering_row(self, letter, q_text, ans_text):
        self.set_font("Helvetica", "B", 11)
        self.cell(9, 7, letter + ")")
        self.set_font("Helvetica", "", 11)
        self.cell(PW - 9, 7, q_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        self.cell(28, 7, "   Order:")
        if self.answers:
            self.set_fill_color(*C_YELLOW)
            self.set_draw_color(*C_GREEN)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*C_GREEN)
            self.multi_cell(PW - 28, 7, ans_text, border=1, fill=True)
            self.set_text_color(*C_GRAY)
        else:
            self.set_draw_color(160, 160, 160)
            self.cell(PW - 28, 7, "", border="B")
            self.ln(9)
            self.cell(28, 7, "")
            self.cell(PW - 28, 7, "", border="B")
        self.ln(12)


# ── Build the exam ────────────────────────────────────────────────────────────

def build(answers=False):
    pdf = ExamPDF(answers=answers)
    pdf.add_page()

    # ── Name / date bar ───────────────────────────────────────────────────────
    if not answers:
        pdf.set_fill_color(240, 245, 255)
        pdf.set_draw_color(*C_BLUE)
        pdf.rect(LM, pdf.get_y(), PW, 13, "FD")
        pdf.set_font("Helvetica", "", 11)
        y = pdf.get_y() + 3
        pdf.set_xy(LM + 3, y)
        pdf.cell(90, 7, "Name: ___________________________________")
        pdf.cell(77, 7, "Date: ___________________")
        pdf.ln(17)

        pdf.set_fill_color(*C_LORANG)
        pdf.set_draw_color(*C_ORANGE)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*C_ORANGE)
        pdf.cell(PW, 8, "  ! SHOW YOUR WORK for every question  (arrows, operations, sentences)",
                 border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(*C_GRAY)
        pdf.ln(5)

    # ══ Section 1 - Unit Conversions ══════════════════════════════════════════
    pdf.section_heading("Section 1 - Unit Conversions   (1 mark each = 18 marks)")
    pdf.italic_note("Convert each measurement. Write your answer on the line.")

    convs = [
        ("a", "56 m",       "cm",  "5,600 cm"),
        ("b", "3.2 km",     "m",   "3,200 m"),
        ("c", "8,000 mm",   "m",   "8 m"),
        ("d", "4,200 cm",   "m",   "42 m"),
        ("e", "0.75 km",    "mm",  "750,000 mm"),
        ("f", "7.5 m",      "cm",  "750 cm"),
        ("g", "9,300 g",    "kg",  "9.3 kg"),
        ("h", "0.6 kg",     "g",   "600 g"),
        ("i", "4 kg 250 g", "g",   "4,250 g"),
        ("j", "85 L",       "mL",  "85,000 mL"),
        ("k", "3,600 mL",   "L",   "3.6 L"),
        ("l", "0.5 L",      "mL",  "500 mL"),
        ("m", "2.4 cm",     "mm",  "24 mm"),
        ("n", "1.8 kg",     "g",   "1,800 g"),
        ("o", "12,000 m",   "km",  "12 km"),
        ("p", "0.08 km",    "cm",  "8,000 cm"),
        ("q", "6 L 750 mL", "mL",  "6,750 mL"),
        ("r", "5,050 g",    "kg",  "5.05 kg"),
    ]
    for args in convs:
        pdf.conv_row(*args)

    # ══ Section 2 - Ordering ══════════════════════════════════════════════════
    pdf.section_heading("Section 2 - Ordering Measurements   (2 marks each = 8 marks)")
    pdf.italic_note("Rewrite each set in ascending order (smallest to largest).")

    ordering = [
        ("a", "45 m,   4,500 cm,   45,000 mm",
         "All equal: 45 m = 4,500 cm = 45,000 mm  (same size)"),
        ("b", "3.2 km,   3,150 m,   320,000 cm",
         "3,150 m (3.15 km)  <  3.2 km  <  320,000 cm (3,200 m = 3.2 km) -> 3,150 m = 3.2 km = 320,000 cm"),
        ("c", "1,800 g,   1.75 kg,   1,850 g",
         "1.75 kg = 1,750 g  -> 1,750 g  <  1,800 g  <  1,850 g"),
        ("d", "0.5 L,   450 mL,   5,000 mL",
         "0.5 L = 500 mL  -> 450 mL  <  0.5 L (500 mL)  <  5,000 mL"),
    ]
    for args in ordering:
        pdf.ordering_row(*args)

    # ══ Section 3 - Area & Perimeter ══════════════════════════════════════════
    pdf.add_page()
    pdf.section_heading("Section 3 - Area & Perimeter   (3 marks each = 15 marks)")

    area_qs = [
        (1,
         ["A rectangular swimming pool is 25 m long and 12 m wide.",
          "a)  What is its area?",
          "b)  What is its perimeter?"],
         ["a) Area = length x width = 25 x 12 = 300 m2",
          "b) Perimeter = 2 x (25 + 12) = 2 x 37 = 74 m"],
         "a) 300 m2   b) 74 m", 28),
        (2,
         ["A square courtyard has a perimeter of 36 m.",
          "What is the area of the courtyard?"],
         ["Side = 36 : 4 = 9 m",
          "Area = 9 x 9 = 81 m2"],
         "Area = 81 m2", 24),
        (3,
         ["A rectangular room has an area of 72 m2 and a width of 8 m.",
          "a)  What is its length?",
          "b)  What is its perimeter?"],
         ["a) Length = Area : width = 72 : 8 = 9 m",
          "b) Perimeter = 2 x (9 + 8) = 2 x 17 = 34 m"],
         "a) 9 m   b) 34 m", 28),
        (4,
         ["A school hall is 18 m long and 11 m wide.",
          "New carpet tiles measure 50 cm x 50 cm.",
          "How many tiles are needed to cover the entire floor?"],
         ["Convert: 18 m = 1,800 cm   11 m = 1,100 cm",
          "Floor area = 1,800 x 1,100 = 1,980,000 cm2",
          "Tile area = 50 x 50 = 2,500 cm2",
          "Tiles = 1,980,000 : 2,500 = 792 tiles"],
         "792 tiles", 32),
        (5,
         ["A rectangular garden (14 m x 9 m) has a 1 m wide path running all around the outside.",
          "What is the area of the path only?"],
         ["Outer area = (14+2) x (9+2) = 16 x 11 = 176 m2",
          "Inner garden = 14 x 9 = 126 m2",
          "Path area = 176 - 126 = 50 m2"],
         "Path area = 50 m2", 28),
    ]
    for args in area_qs:
        pdf.word_problem(*args)

    # ══ Section 4 - Word Problems ══════════════════════════════════════════════
    pdf.add_page()
    pdf.section_heading("Section 4 - Word Problems   (4 marks each = 28 marks)")
    pdf.italic_note("Read each problem carefully. Show ALL working clearly.")

    word_qs = [
        (1,
         ["A car uses 6 L of petrol every 100 km.",
          "How much petrol is needed for a 450 km journey?"],
         ["Petrol per km = 6 : 100 = 0.06 L/km",
          "Total = 0.06 x 450 = 27 L"],
         "27 L", 28),
        (2,
         ["One student has 4.2 kg of sand and another has 1,750 g.",
          "What is the total weight in kilograms?"],
         ["Convert: 1,750 g = 1.75 kg",
          "Total = 4.2 + 1.75 = 5.95 kg"],
         "5.95 kg", 26),
        (3,
         ["A recipe for 8 people needs 600 g of butter.",
          "How many grams of butter are needed for 14 people?"],
         ["Per person = 600 : 8 = 75 g",
          "For 14 people = 75 x 14 = 1,050 g"],
         "1,050 g", 26),
        (4,
         ["A water tank holds 250 L. A pump removes 4,500 mL per minute.",
          "How many litres remain after 8 minutes?"],
         ["Removed per min = 4,500 mL = 4.5 L",
          "Total removed = 4.5 x 8 = 36 L",
          "Remaining = 250 - 36 = 214 L"],
         "214 L", 30),
        (5,
         ["A roll of wire is 15 m long. Pieces of 35 cm are cut from it.",
          "a)  How many complete pieces can be cut?",
          "b)  How much wire is left over (in cm)?"],
         ["Convert: 15 m = 1,500 cm",
          "a) Pieces = 1,500 : 35 = 42 complete pieces",
          "b) Remainder = 1,500 - (42 x 35) = 1,500 - 1,470 = 30 cm"],
         "a) 42 pieces   b) 30 cm left over", 32),
        (6,
         ["A shop sells juice in 1.5 L bottles for EUR 2.10 and in 250 mL cartons for EUR 0.45.",
          "Which is better value per mL? Show your calculation."],
         ["1.5 L bottle: EUR 2.10 : 1,500 mL = EUR 0.0014 per mL",
          "250 mL carton: EUR 0.45 : 250 mL = EUR 0.0018 per mL",
          "The 1.5 L bottle is better value (cheaper per mL)."],
         "1.5 L bottle is better value", 32),
        (7,
         ["Tom walks 1.6 km to school and back every day, 5 days a week.",
          "In 4 weeks, how many metres does he walk in total?"],
         ["Daily = 1.6 x 2 = 3.2 km",
          "Weekly = 3.2 x 5 = 16 km",
          "4 weeks = 16 x 4 = 64 km = 64,000 m"],
         "64,000 m", 30),
    ]
    for args in word_qs:
        pdf.word_problem(*args)

    # ══ Section 5 - Challenge ══════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_heading("Section 5 - Challenge Problems   (5 marks each = 10 marks)")
    pdf.italic_note("Multi-step problems. Show every step of your working.")

    challenge_qs = [
        (1,
         ["A swimming pool is 50 m long, 20 m wide, and 2 m deep.",
          "It is currently filled to 3/4 of its capacity.  (1 m3 = 1,000 L)",
          "a)  What is the total capacity of the pool in litres?",
          "b)  How many litres of water are currently in the pool?",
          "c)  How many more litres are needed to completely fill it?"],
         ["a) Volume = 50 x 20 x 2 = 2,000 m3  => capacity = 2,000,000 L",
          "b) Water in pool = (3/4) x 2,000,000 = 1,500,000 L",
          "c) To fill = 2,000,000 - 1,500,000 = 500,000 L"],
         "a) 2,000,000 L   b) 1,500,000 L   c) 500,000 L", 42),
        (2,
         ["A farmer has a rectangular field 240 m x 150 m.",
          "He builds a fence along the entire perimeter.",
          "Fence posts are placed every 6 m, including at each corner.",
          "a)  What is the perimeter of the field?",
          "b)  How many fence posts does he need?",
          "c)  If each post costs EUR 8.50, what is the total cost?"],
         ["a) Perimeter = 2 x (240 + 150) = 2 x 390 = 780 m",
          "b) Posts = 780 : 6 = 130 posts",
          "c) Cost = 130 x EUR 8.50 = EUR 1,105"],
         "a) 780 m   b) 130 posts   c) EUR 1,105", 42),
    ]
    for args in challenge_qs:
        pdf.word_problem(*args)

    # ── Score table (student only) ────────────────────────────────────────────
    if not answers:
        pdf.ln(4)
        pdf.section_heading("Score Summary")
        sections = [
            ("Section 1\nConversions", 18),
            ("Section 2\nOrdering", 8),
            ("Section 3\nArea", 15),
            ("Section 4\nWord Probs", 28),
            ("Section 5\nChallenge", 10),
            ("TOTAL", 79),
        ]
        cw = PW // len(sections)
        pdf.set_fill_color(*C_LBLUE)
        pdf.set_draw_color(*C_BLUE)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*C_BLUE)
        for name, _ in sections:
            pdf.cell(cw, 10, name.replace("\n", "/"), border=1, fill=True, align="C")
        pdf.ln(10)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*C_GRAY)
        for _, marks in sections:
            pdf.cell(cw, 10, f"/ {marks}", border=1, align="C")
        pdf.ln(12)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(PW, 8, "Well done, Karnika!  Keep up the great work!", align="C")

    return pdf


if __name__ == "__main__":
    build(answers=False).output("Karnika_Mock_Exam.pdf")
    print("Created: Karnika_Mock_Exam.pdf")

    build(answers=True).output("Karnika_Mock_Exam_Answers.pdf")
    print("Created: Karnika_Mock_Exam_Answers.pdf")
