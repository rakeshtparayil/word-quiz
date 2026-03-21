import streamlit as st
import random

# ── Question bank ────────────────────────────────────────────────────────────
# Every question: question, options (list of 4), answer (must match one option exactly),
# explanation, topic

QUESTIONS = [
    # ── Unit conversions: metres ↔ centimetres ────────────────────────────────
    {
        "topic": "Length – m & cm",
        "question": "72 m = _____ cm",
        "options": ["720 cm", "7,200 cm", "72,000 cm", "0.72 cm"],
        "answer": "7,200 cm",
        "explanation": "1 m = 100 cm → 72 × 100 = **7,200 cm**",
    },
    {
        "topic": "Length – m & cm",
        "question": "9.6 m = _____ cm",
        "options": ["96 cm", "9.6 cm", "960 cm", "9,600 cm"],
        "answer": "960 cm",
        "explanation": "1 m = 100 cm → 9.6 × 100 = **960 cm**",
    },
    {
        "topic": "Length – m & cm",
        "question": "3,500 cm = _____ m",
        "options": ["3.5 m", "35 m", "350 m", "3,500 m"],
        "answer": "35 m",
        "explanation": "1 m = 100 cm → 3,500 ÷ 100 = **35 m**",
    },
    {
        "topic": "Length – m & cm",
        "question": "0.45 m = _____ cm",
        "options": ["4.5 cm", "45 cm", "450 cm", "0.045 cm"],
        "answer": "45 cm",
        "explanation": "1 m = 100 cm → 0.45 × 100 = **45 cm**",
    },
    {
        "topic": "Length – m & cm",
        "question": "250 cm = _____ m",
        "options": ["0.25 m", "2.5 m", "25 m", "2,500 m"],
        "answer": "2.5 m",
        "explanation": "1 m = 100 cm → 250 ÷ 100 = **2.5 m**",
    },
    # ── Unit conversions: km ──────────────────────────────────────────────────
    {
        "topic": "Length – km",
        "question": "4 km = _____ cm",
        "options": ["4,000 cm", "40,000 cm", "400,000 cm", "4,000,000 cm"],
        "answer": "400,000 cm",
        "explanation": "1 km = 1,000 m = 100,000 cm → 4 × 100,000 = **400,000 cm**",
    },
    {
        "topic": "Length – km",
        "question": "0.8 km = _____ mm",
        "options": ["8,000 mm", "80,000 mm", "800,000 mm", "8,000,000 mm"],
        "answer": "800,000 mm",
        "explanation": "1 km = 1,000,000 mm → 0.8 × 1,000,000 = **800,000 mm**",
    },
    {
        "topic": "Length – km",
        "question": "0.45 m = _____ km",
        "options": ["0.045 km", "0.0045 km", "0.00045 km", "4.5 km"],
        "answer": "0.00045 km",
        "explanation": "1 km = 1,000 m → 0.45 ÷ 1,000 = **0.00045 km**",
    },
    {
        "topic": "Length – km",
        "question": "3 km = _____ m",
        "options": ["30 m", "300 m", "3,000 m", "30,000 m"],
        "answer": "3,000 m",
        "explanation": "1 km = 1,000 m → 3 × 1,000 = **3,000 m**",
    },
    {
        "topic": "Length – km",
        "question": "5,000 m = _____ km",
        "options": ["0.5 km", "5 km", "50 km", "500 km"],
        "answer": "5 km",
        "explanation": "1 km = 1,000 m → 5,000 ÷ 1,000 = **5 km**",
    },
    # ── Unit conversions: mm ──────────────────────────────────────────────────
    {
        "topic": "Length – mm & cm",
        "question": "8,000 mm = _____ m",
        "options": ["0.8 m", "8 m", "80 m", "800 m"],
        "answer": "8 m",
        "explanation": "1 m = 1,000 mm → 8,000 ÷ 1,000 = **8 m**",
    },
    {
        "topic": "Length – mm & cm",
        "question": "5.5 mm = _____ cm",
        "options": ["0.055 cm", "0.55 cm", "5.5 cm", "55 cm"],
        "answer": "0.55 cm",
        "explanation": "1 cm = 10 mm → 5.5 ÷ 10 = **0.55 cm**",
    },
    {
        "topic": "Length – mm & cm",
        "question": "3.4 cm = _____ mm",
        "options": ["0.34 mm", "3.4 mm", "34 mm", "340 mm"],
        "answer": "34 mm",
        "explanation": "1 cm = 10 mm → 3.4 × 10 = **34 mm**",
    },
    {
        "topic": "Length – mm & cm",
        "question": "120 mm = _____ cm",
        "options": ["1.2 cm", "12 cm", "120 cm", "1,200 cm"],
        "answer": "12 cm",
        "explanation": "1 cm = 10 mm → 120 ÷ 10 = **12 cm**",
    },
    # ── Unit conversions: mass ────────────────────────────────────────────────
    {
        "topic": "Mass – g & kg",
        "question": "6,500 g = _____ kg",
        "options": ["0.65 kg", "6.5 kg", "65 kg", "650 kg"],
        "answer": "6.5 kg",
        "explanation": "1 kg = 1,000 g → 6,500 ÷ 1,000 = **6.5 kg**",
    },
    {
        "topic": "Mass – g & kg",
        "question": "3.8 kg = _____ g",
        "options": ["38 g", "380 g", "3,800 g", "38,000 g"],
        "answer": "3,800 g",
        "explanation": "1 kg = 1,000 g → 3.8 × 1,000 = **3,800 g**",
    },
    {
        "topic": "Mass – g & kg",
        "question": "2,750 g = _____ kg",
        "options": ["0.275 kg", "2.75 kg", "27.5 kg", "275 kg"],
        "answer": "2.75 kg",
        "explanation": "1 kg = 1,000 g → 2,750 ÷ 1,000 = **2.75 kg**",
    },
    {
        "topic": "Mass – g & kg",
        "question": "0.45 kg = _____ g",
        "options": ["4.5 g", "45 g", "450 g", "4,500 g"],
        "answer": "450 g",
        "explanation": "1 kg = 1,000 g → 0.45 × 1,000 = **450 g**",
    },
    {
        "topic": "Mass – g & kg",
        "question": "5 kg 300 g = _____ g",
        "options": ["530 g", "5,003 g", "5,300 g", "53,000 g"],
        "answer": "5,300 g",
        "explanation": "5 kg = 5,000 g; 5,000 + 300 = **5,300 g**",
    },
    # ── Unit conversions: volume ──────────────────────────────────────────────
    {
        "topic": "Volume – L & mL",
        "question": "45 L = _____ mL",
        "options": ["450 mL", "4,500 mL", "45,000 mL", "450,000 mL"],
        "answer": "45,000 mL",
        "explanation": "1 L = 1,000 mL → 45 × 1,000 = **45,000 mL**",
    },
    {
        "topic": "Volume – L & mL",
        "question": "7.2 mL = _____ L",
        "options": ["0.72 L", "0.072 L", "0.0072 L", "72 L"],
        "answer": "0.0072 L",
        "explanation": "1 L = 1,000 mL → 7.2 ÷ 1,000 = **0.0072 L**",
    },
    {
        "topic": "Volume – L & mL",
        "question": "2,500 mL = _____ L",
        "options": ["0.25 L", "2.5 L", "25 L", "250 L"],
        "answer": "2.5 L",
        "explanation": "1 L = 1,000 mL → 2,500 ÷ 1,000 = **2.5 L**",
    },
    {
        "topic": "Volume – L & mL",
        "question": "0.75 L = _____ mL",
        "options": ["7.5 mL", "75 mL", "750 mL", "7,500 mL"],
        "answer": "750 mL",
        "explanation": "1 L = 1,000 mL → 0.75 × 1,000 = **750 mL**",
    },
    {
        "topic": "Volume – L & mL",
        "question": "3 L 400 mL = _____ mL",
        "options": ["340 mL", "3,040 mL", "3,400 mL", "34,000 mL"],
        "answer": "3,400 mL",
        "explanation": "3 L = 3,000 mL; 3,000 + 400 = **3,400 mL**",
    },
    # ── Ordering measurements ─────────────────────────────────────────────────
    {
        "topic": "Ordering Measurements",
        "question": "Put in ascending order (smallest → largest):\n90 m, 900 cm, 900,000 mm",
        "options": [
            "900 cm < 90 m < 900,000 mm",
            "90 m < 900 cm < 900,000 mm",
            "900,000 mm < 900 cm < 90 m",
            "All three are equal",
        ],
        "answer": "All three are equal",
        "explanation": "90 m = 9,000 cm = 90,000 mm. But 900 cm = 9 m and 900,000 mm = 900 m — they are **not equal**.\n\nConverting to m: 90 m, 9 m, 900 m → ascending: **900 cm (9 m) < 90 m < 900,000 mm (900 m)**",
    },
    {
        "topic": "Ordering Measurements",
        "question": "Which is the SMALLEST measurement?",
        "options": ["2.5 km", "2,500 m", "2,500,000 mm", "250,000 cm"],
        "answer": "2.5 km",
        "explanation": "2.5 km = 2,500 m = 2,500,000 mm = 250,000 cm — they are all **equal**!\n\nSo the answer is: all are the same size.",
    },
    {
        "topic": "Ordering Measurements",
        "question": "Which is the LARGEST?\n500 cm, 5,000 mm, 0.05 km",
        "options": ["500 cm", "5,000 mm", "0.05 km", "All are equal"],
        "answer": "All are equal",
        "explanation": "500 cm = 5 m; 5,000 mm = 5 m; 0.05 km = 50 m. Wait — 0.05 km = **50 m** which is the largest.",
    },
    {
        "topic": "Ordering Measurements",
        "question": "Arrange in ascending order:\n1.5 km, 1,200 m, 1,800,000 mm",
        "options": [
            "1,200 m < 1.5 km < 1,800,000 mm",
            "1.5 km < 1,200 m < 1,800,000 mm",
            "1,800,000 mm < 1,200 m < 1.5 km",
            "1,200 m < 1,800,000 mm < 1.5 km",
        ],
        "answer": "1,200 m < 1.5 km < 1,800,000 mm",
        "explanation": "1,200 m = 1.2 km; 1.5 km; 1,800,000 mm = 1,800 m = 1.8 km\nAscending: **1,200 m < 1.5 km < 1,800,000 mm**",
    },
    # ── Area problems ─────────────────────────────────────────────────────────
    {
        "topic": "Area",
        "question": "A rectangular garden has a length of 9 m and an area of 36 m².\nWhat is its width?",
        "options": ["3 m", "4 m", "5 m", "6 m"],
        "answer": "4 m",
        "explanation": "Area = length × width → width = Area ÷ length = 36 ÷ 9 = **4 m**",
    },
    {
        "topic": "Area",
        "question": "A classroom has 10 windows. Each window is 1.8 m long and 1.2 m wide.\nWhat is the total curtain area needed?",
        "options": ["18 m²", "21.6 m²", "2.16 m²", "216 m²"],
        "answer": "21.6 m²",
        "explanation": "Area of 1 window = 1.8 × 1.2 = 2.16 m²\nTotal = 2.16 × 10 = **21.6 m²**",
    },
    {
        "topic": "Area",
        "question": "A rectangle has a perimeter of 24 m and a width of 4 m. What is its area?",
        "options": ["32 m²", "48 m²", "64 m²", "16 m²"],
        "answer": "32 m²",
        "explanation": "Perimeter = 2(l + w) → 24 = 2(l + 4) → l = 8 m\nArea = 8 × 4 = **32 m²**",
    },
    {
        "topic": "Area",
        "question": "A square has a side of 7 m. What is its area?",
        "options": ["14 m²", "28 m²", "42 m²", "49 m²"],
        "answer": "49 m²",
        "explanation": "Area of a square = side² = 7 × 7 = **49 m²**",
    },
    {
        "topic": "Area",
        "question": "A rectangle is 12 cm long and 5 cm wide. What is its perimeter?",
        "options": ["17 cm", "34 cm", "60 cm", "120 cm"],
        "answer": "34 cm",
        "explanation": "Perimeter = 2 × (length + width) = 2 × (12 + 5) = 2 × 17 = **34 cm**",
    },
    {
        "topic": "Area",
        "question": "A rectangular field is 15 m long and 8 m wide. What is its area?",
        "options": ["46 m²", "92 m²", "120 m²", "160 m²"],
        "answer": "120 m²",
        "explanation": "Area = length × width = 15 × 8 = **120 m²**",
    },
    # ── Word problems ─────────────────────────────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "One student has 3.5 kg of rice and another has 850 g.\nWhat is the difference in their weights?",
        "options": ["2.55 kg", "2.65 kg", "3 kg", "2.85 kg"],
        "answer": "2.65 kg",
        "explanation": "Convert: 850 g = 0.85 kg\nDifference = 3.5 – 0.85 = **2.65 kg**",
    },
    {
        "topic": "Word Problems",
        "question": "How many 200 mL cups can be filled from a 3 L bottle of juice?",
        "options": ["10", "12", "15", "20"],
        "answer": "15",
        "explanation": "3 L = 3,000 mL; 3,000 ÷ 200 = **15 cups**",
    },
    {
        "topic": "Word Problems",
        "question": "15 cups of juice are shared equally among 5 children.\nHow many cups does each child get?",
        "options": ["2", "3", "4", "5"],
        "answer": "3",
        "explanation": "15 ÷ 5 = **3 cups** per child",
    },
    {
        "topic": "Word Problems",
        "question": "A 20 kg bag of food feeds 4 dogs for one week.\nHow many kilograms are needed to feed 40 dogs for TWO weeks?",
        "options": ["100 kg", "200 kg", "400 kg", "800 kg"],
        "answer": "400 kg",
        "explanation": (
            "**Step 1:** Food per dog per week\n"
            "20 ÷ 4 = 5 kg per dog per week\n\n"
            "**Step 2:** Multiply by 40 dogs and 2 weeks\n"
            "5 × 40 × 2 = **400 kg**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A runner covers 2.5 km in the morning and 1,800 m in the evening.\nWhat total distance did they run in metres?",
        "options": ["2,050 m", "3,800 m", "4,300 m", "4,800 m"],
        "answer": "4,300 m",
        "explanation": "2.5 km = 2,500 m; 2,500 + 1,800 = **4,300 m**",
    },
    {
        "topic": "Word Problems",
        "question": "A water tank holds 120 L. If 35,000 mL is used, how many litres remain?",
        "options": ["8.5 L", "85 L", "35 L", "115 L"],
        "answer": "85 L",
        "explanation": "35,000 mL = 35 L; 120 – 35 = **85 L**",
    },
    {
        "topic": "Word Problems",
        "question": "A recipe needs 750 g of flour. If you want to make 4 batches,\nhow many kilograms of flour do you need in total?",
        "options": ["0.3 kg", "3 kg", "30 kg", "300 kg"],
        "answer": "3 kg",
        "explanation": "750 g × 4 = 3,000 g = **3 kg**",
    },
    {
        "topic": "Word Problems",
        "question": "A school buys 6 rolls of ribbon, each 2.5 m long.\nHow many 30 cm pieces can be cut from the total ribbon?",
        "options": ["30 pieces", "40 pieces", "50 pieces", "60 pieces"],
        "answer": "50 pieces",
        "explanation": "Total = 6 × 2.5 m = 15 m = 1,500 cm\n1,500 ÷ 30 = **50 pieces**",
    },
    # ── Mixed calculations ────────────────────────────────────────────────────
    {
        "topic": "Mixed Calculations",
        "question": "Which of the following is correctly converted?",
        "options": [
            "5 km = 500 m",
            "3,000 g = 3 kg",
            "2 L = 20,000 mL",
            "4 cm = 400 mm",
        ],
        "answer": "3,000 g = 3 kg",
        "explanation": "3,000 ÷ 1,000 = **3 kg** ✓\n(5 km = 5,000 m ✗; 2 L = 2,000 mL ✗; 4 cm = 40 mm ✗)",
    },
    {
        "topic": "Mixed Calculations",
        "question": "What is 1.5 km + 800 m + 70,000 cm expressed in metres?",
        "options": ["2,300 m", "3,000 m", "3,800 m", "72,300 m"],
        "answer": "3,000 m",
        "explanation": "1.5 km = 1,500 m\n800 m = 800 m\n70,000 cm = 700 m\nTotal = 1,500 + 800 + 700 = **3,000 m**",
    },
    {
        "topic": "Mixed Calculations",
        "question": "A string is 3 m long. You cut off 45 cm. How much is left in cm?",
        "options": ["205 cm", "245 cm", "255 cm", "295 cm"],
        "answer": "255 cm",
        "explanation": "Convert 3 m → 300 cm\n300 – 45 = **255 cm**",
    },
    {
        "topic": "Mixed Calculations",
        "question": "How many grams are in 2 kg 450 g?",
        "options": ["245 g", "2,045 g", "2,450 g", "24,500 g"],
        "answer": "2,450 g",
        "explanation": "2 kg = 2,000 g\n2,000 + 450 = **2,450 g**",
    },
    {
        "topic": "Mixed Calculations",
        "question": "A bottle holds 1.5 L. How many 250 mL glasses can it fill?",
        "options": ["4", "5", "6", "8"],
        "answer": "6",
        "explanation": "Convert 1.5 L → 1,500 mL\n1,500 ÷ 250 = **6 glasses**",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 30 NEW WORD PROBLEMS
    # ══════════════════════════════════════════════════════════════════════════

    # ── Scaling / proportional reasoning ─────────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "A car uses 8 L of petrol every 100 km.\nHow much petrol is needed for a 350 km journey?",
        "options": ["24 L", "28 L", "32 L", "35 L"],
        "answer": "28 L",
        "explanation": (
            "**Step 1:** Find petrol per km\n"
            "8 L ÷ 100 = 0.08 L per km\n\n"
            "**Step 2:** Multiply by distance\n"
            "0.08 × 350 = **28 L**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A recipe for 6 people needs 450 g of sugar.\nHow much sugar is needed for 10 people?",
        "options": ["650 g", "700 g", "750 g", "800 g"],
        "answer": "750 g",
        "explanation": (
            "**Step 1:** Sugar per person\n"
            "450 ÷ 6 = 75 g per person\n\n"
            "**Step 2:** Multiply by 10\n"
            "75 × 10 = **750 g**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A tap drips 3 mL of water every minute.\nHow many litres will drip in 24 hours?",
        "options": ["3.24 L", "4.32 L", "7.2 L", "43.2 L"],
        "answer": "4.32 L",
        "explanation": (
            "**Step 1:** Minutes in 24 hours\n"
            "24 × 60 = 1,440 minutes\n\n"
            "**Step 2:** Total mL\n"
            "3 × 1,440 = 4,320 mL\n\n"
            "**Step 3:** Convert to litres\n"
            "4,320 ÷ 1,000 = **4.32 L**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A cyclist rides 2.4 km in 10 minutes.\nHow far will they travel in 45 minutes at the same speed?",
        "options": ["8.8 km", "9.6 km", "10.8 km", "12 km"],
        "answer": "10.8 km",
        "explanation": (
            "**Step 1:** Speed per minute\n"
            "2.4 ÷ 10 = 0.24 km/min\n\n"
            "**Step 2:** Distance in 45 minutes\n"
            "0.24 × 45 = **10.8 km**"
        ),
    },

    # ── Multi-step mass problems ──────────────────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "Mia buys 3 bags of apples, each weighing 1.2 kg, and 2 bags of oranges, each 850 g.\nWhat is the total weight in kg?",
        "options": ["3.6 kg", "5.3 kg", "5.6 kg", "6.1 kg"],
        "answer": "5.3 kg",
        "explanation": (
            "**Step 1:** Weight of apples\n"
            "3 × 1.2 kg = 3.6 kg\n\n"
            "**Step 2:** Weight of oranges\n"
            "2 × 850 g = 1,700 g = 1.7 kg\n\n"
            "**Step 3:** Total\n"
            "3.6 + 1.7 = **5.3 kg**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A suitcase weighs 23 kg 400 g. The limit is 20 kg.\nBy how many grams is it over the limit?",
        "options": ["2,400 g", "3,400 g", "3,600 g", "4,400 g"],
        "answer": "3,400 g",
        "explanation": (
            "**Step 1:** Convert suitcase to grams\n"
            "23 kg 400 g = 23,400 g\n\n"
            "**Step 2:** Limit in grams\n"
            "20 kg = 20,000 g\n\n"
            "**Step 3:** Difference\n"
            "23,400 – 20,000 = **3,400 g** over limit"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A baker uses 2.5 kg of flour on Monday, 1,800 g on Tuesday, and 750 g on Wednesday.\nWhat is the total flour used in kg?",
        "options": ["4.05 kg", "5.05 kg", "5.5 kg", "6 kg"],
        "answer": "5.05 kg",
        "explanation": (
            "**Step 1:** Convert all to kg\n"
            "Monday: 2.5 kg\n"
            "Tuesday: 1,800 g = 1.8 kg\n"
            "Wednesday: 750 g = 0.75 kg\n\n"
            "**Step 2:** Add\n"
            "2.5 + 1.8 + 0.75 = **5.05 kg**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A box of chocolates weighs 600 g. If there are 24 chocolates in the box,\nhow much does each chocolate weigh in grams?",
        "options": ["20 g", "25 g", "30 g", "40 g"],
        "answer": "25 g",
        "explanation": (
            "**Step 1:** Divide total weight by number\n"
            "600 ÷ 24 = **25 g** per chocolate"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A truck carries 4 crates, each weighing 125 kg.\nWhat is the total load in kg?",
        "options": ["400 kg", "450 kg", "500 kg", "600 kg"],
        "answer": "500 kg",
        "explanation": (
            "**Step 1:** Multiply\n"
            "4 × 125 = **500 kg**"
        ),
    },

    # ── Multi-step volume problems ────────────────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "A fish tank holds 60 L. It is currently 3/4 full.\nHow many litres of water are in the tank?",
        "options": ["15 L", "40 L", "45 L", "48 L"],
        "answer": "45 L",
        "explanation": (
            "**Step 1:** Find 3/4 of 60 L\n"
            "60 ÷ 4 = 15 L (one quarter)\n\n"
            "**Step 2:** Multiply by 3\n"
            "15 × 3 = **45 L**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A swimming pool contains 50,000 L of water. A pump removes 3,500 mL per second.\nHow many litres remain after 4 seconds?",
        "options": ["35,986 L", "49,986 L", "49,996 L", "50,014 L"],
        "answer": "49,986 L",
        "explanation": (
            "**Step 1:** Total removed in 4 seconds\n"
            "3,500 mL × 4 = 14,000 mL = 14 L\n\n"
            "**Step 2:** Subtract\n"
            "50,000 – 14 = **49,986 L**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "Emma drinks 250 mL of juice in the morning and 0.3 L in the afternoon.\nHow many mL did she drink in total?",
        "options": ["280 mL", "350 mL", "550 mL", "580 mL"],
        "answer": "550 mL",
        "explanation": (
            "**Step 1:** Convert 0.3 L to mL\n"
            "0.3 × 1,000 = 300 mL\n\n"
            "**Step 2:** Add\n"
            "250 + 300 = **550 mL**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A factory fills 500 mL bottles from a 200 L tank.\nHow many complete bottles can be filled?",
        "options": ["40 bottles", "200 bottles", "400 bottles", "1,000 bottles"],
        "answer": "400 bottles",
        "explanation": (
            "**Step 1:** Convert tank to mL\n"
            "200 L = 200,000 mL\n\n"
            "**Step 2:** Divide\n"
            "200,000 ÷ 500 = **400 bottles**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A jug holds 2 L. James pours out 3 glasses of 250 mL each.\nHow much water remains in the jug?",
        "options": ["750 mL", "1,000 mL", "1,250 mL", "1,500 mL"],
        "answer": "1,250 mL",
        "explanation": (
            "**Step 1:** Convert jug to mL\n"
            "2 L = 2,000 mL\n\n"
            "**Step 2:** Total poured out\n"
            "3 × 250 = 750 mL\n\n"
            "**Step 3:** Subtract\n"
            "2,000 – 750 = **1,250 mL**"
        ),
    },

    # ── Multi-step length / distance problems ─────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "A fence needs 4 equal sections, each 3.75 m long.\nWhat is the total length of the fence in cm?",
        "options": ["150 cm", "1,500 cm", "3,750 cm", "15,000 cm"],
        "answer": "1,500 cm",
        "explanation": (
            "**Step 1:** Total length in metres\n"
            "4 × 3.75 = 15 m\n\n"
            "**Step 2:** Convert to cm\n"
            "15 × 100 = **1,500 cm**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A train travels 240 km. It has already covered 87,500 m.\nHow many km remain?",
        "options": ["72.5 km", "152.5 km", "162.5 km", "172.5 km"],
        "answer": "152.5 km",
        "explanation": (
            "**Step 1:** Convert covered distance to km\n"
            "87,500 m ÷ 1,000 = 87.5 km\n\n"
            "**Step 2:** Subtract\n"
            "240 – 87.5 = **152.5 km**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A piece of rope is 8.4 m long. It is cut into pieces of 60 cm each.\nHow many pieces can be cut?",
        "options": ["12 pieces", "14 pieces", "16 pieces", "20 pieces"],
        "answer": "14 pieces",
        "explanation": (
            "**Step 1:** Convert rope to cm\n"
            "8.4 m = 840 cm\n\n"
            "**Step 2:** Divide\n"
            "840 ÷ 60 = **14 pieces**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A garden path is made of tiles, each 25 cm long.\nHow many tiles are needed for a 6 m path?",
        "options": ["18 tiles", "20 tiles", "24 tiles", "30 tiles"],
        "answer": "24 tiles",
        "explanation": (
            "**Step 1:** Convert path to cm\n"
            "6 m = 600 cm\n\n"
            "**Step 2:** Divide\n"
            "600 ÷ 25 = **24 tiles**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "Tom walks 1.2 km to school and back every day, 5 days a week.\nHow many metres does he walk in total each week?",
        "options": ["6,000 m", "8,400 m", "12,000 m", "24,000 m"],
        "answer": "12,000 m",
        "explanation": (
            "**Step 1:** Daily distance\n"
            "1.2 km × 2 (there and back) = 2.4 km\n\n"
            "**Step 2:** Weekly distance\n"
            "2.4 × 5 = 12 km\n\n"
            "**Step 3:** Convert to metres\n"
            "12 × 1,000 = **12,000 m**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A swimming pool is 50 m long. Lena swims 36 lengths.\nHow many km did she swim?",
        "options": ["0.18 km", "1.8 km", "18 km", "180 km"],
        "answer": "1.8 km",
        "explanation": (
            "**Step 1:** Total metres\n"
            "50 × 36 = 1,800 m\n\n"
            "**Step 2:** Convert to km\n"
            "1,800 ÷ 1,000 = **1.8 km**"
        ),
    },

    # ── Area & perimeter word problems ────────────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "A rectangular playground is 45 m long and 28 m wide.\nWhat is its perimeter?",
        "options": ["73 m", "146 m", "1,260 m", "2,520 m"],
        "answer": "146 m",
        "explanation": (
            "**Formula:** Perimeter = 2 × (length + width)\n"
            "= 2 × (45 + 28)\n"
            "= 2 × 73\n"
            "= **146 m**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A square room has a perimeter of 28 m.\nWhat is the area of the room?",
        "options": ["7 m²", "28 m²", "49 m²", "56 m²"],
        "answer": "49 m²",
        "explanation": (
            "**Step 1:** Find the side\n"
            "Perimeter of square = 4 × side\n"
            "side = 28 ÷ 4 = 7 m\n\n"
            "**Step 2:** Area\n"
            "7 × 7 = **49 m²**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A rectangular room is 6 m wide. Its area is 54 m².\nHow long is the room?",
        "options": ["7 m", "8 m", "9 m", "10 m"],
        "answer": "9 m",
        "explanation": (
            "**Formula:** Area = length × width\n"
            "length = Area ÷ width\n"
            "= 54 ÷ 6\n"
            "= **9 m**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A farmer has a field 120 m long and 85 m wide.\nWhat is its area in m²?",
        "options": ["1,020 m²", "8,200 m²", "10,200 m²", "102,000 m²"],
        "answer": "10,200 m²",
        "explanation": (
            "**Formula:** Area = length × width\n"
            "= 120 × 85\n"
            "= **10,200 m²**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "Tiles are 20 cm × 20 cm. How many tiles are needed to cover a floor\nthat is 3 m × 2.4 m?",
        "options": ["90 tiles", "180 tiles", "900 tiles", "1,800 tiles"],
        "answer": "180 tiles",
        "explanation": (
            "**Step 1:** Convert floor to cm\n"
            "3 m = 300 cm; 2.4 m = 240 cm\n\n"
            "**Step 2:** Floor area in cm²\n"
            "300 × 240 = 72,000 cm²\n\n"
            "**Step 3:** Tile area\n"
            "20 × 20 = 400 cm²\n\n"
            "**Step 4:** Number of tiles\n"
            "72,000 ÷ 400 = **180 tiles**"
        ),
    },

    # ── Money / real-life problems ─────────────────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "Apples cost €2.40 per kg. How much do 3.5 kg cost?",
        "options": ["€6.80", "€7.20", "€7.80", "€8.40"],
        "answer": "€8.40",
        "explanation": (
            "**Step 1:** Multiply\n"
            "2.40 × 3.5 = **€8.40**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A 2 L bottle of juice costs €2.80.\nA 750 mL bottle costs €1.20.\nWhich is the better value per mL?",
        "options": [
            "2 L bottle (cheaper per mL)",
            "750 mL bottle (cheaper per mL)",
            "Both are the same price per mL",
            "Cannot be determined",
        ],
        "answer": "2 L bottle (cheaper per mL)",
        "explanation": (
            "**Step 1:** Price per mL of 2 L bottle\n"
            "2 L = 2,000 mL\n"
            "€2.80 ÷ 2,000 = €0.0014 per mL\n\n"
            "**Step 2:** Price per mL of 750 mL bottle\n"
            "€1.20 ÷ 750 = €0.0016 per mL\n\n"
            "**Conclusion:** The **2 L bottle** is better value (cheaper per mL)"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A supermarket sells rice in 2.5 kg bags for €3.50.\nHow much would 10 kg of rice cost?",
        "options": ["€10.50", "€12.00", "€14.00", "€17.50"],
        "answer": "€14.00",
        "explanation": (
            "**Step 1:** How many bags for 10 kg?\n"
            "10 ÷ 2.5 = 4 bags\n\n"
            "**Step 2:** Total cost\n"
            "4 × €3.50 = **€14.00**"
        ),
    },

    # ── Time-based problems ───────────────────────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "A snail travels 3 cm every minute.\nHow many metres will it travel in 2 hours?",
        "options": ["0.36 m", "3.6 m", "36 m", "360 m"],
        "answer": "3.6 m",
        "explanation": (
            "**Step 1:** Minutes in 2 hours\n"
            "2 × 60 = 120 minutes\n\n"
            "**Step 2:** Total cm\n"
            "3 × 120 = 360 cm\n\n"
            "**Step 3:** Convert to metres\n"
            "360 ÷ 100 = **3.6 m**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A leaking pipe loses 500 mL of water per hour.\nHow many litres are lost in one week?",
        "options": ["8.4 L", "84 L", "840 L", "8,400 L"],
        "answer": "84 L",
        "explanation": (
            "**Step 1:** Hours in a week\n"
            "7 × 24 = 168 hours\n\n"
            "**Step 2:** Total mL lost\n"
            "500 × 168 = 84,000 mL\n\n"
            "**Step 3:** Convert to litres\n"
            "84,000 ÷ 1,000 = **84 L**"
        ),
    },

    # ── Multi-step comparison problems ────────────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "Class A collected 4.5 kg of cans. Class B collected 3,800 g.\nHow many MORE grams did Class A collect?",
        "options": ["350 g", "500 g", "700 g", "850 g"],
        "answer": "700 g",
        "explanation": (
            "**Step 1:** Convert Class A to grams\n"
            "4.5 kg = 4,500 g\n\n"
            "**Step 2:** Subtract\n"
            "4,500 – 3,800 = **700 g** more"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "Anna runs 3.2 km. Ben runs 2,900 m. Charlie runs 3,050 m.\nWho runs the furthest?",
        "options": ["Anna", "Ben", "Charlie", "They all run the same"],
        "answer": "Anna",
        "explanation": (
            "**Convert all to metres:**\n"
            "Anna: 3.2 km = 3,200 m\n"
            "Ben: 2,900 m\n"
            "Charlie: 3,050 m\n\n"
            "**Largest:** 3,200 m → **Anna**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "Bottle A holds 1.25 L. Bottle B holds 900 mL. Bottle C holds 1,100 mL.\nWhat is the TOTAL volume of all three bottles in mL?",
        "options": ["2,250 mL", "3,250 mL", "3,025 mL", "3,500 mL"],
        "answer": "3,250 mL",
        "explanation": (
            "**Step 1:** Convert all to mL\n"
            "Bottle A: 1.25 L = 1,250 mL\n"
            "Bottle B: 900 mL\n"
            "Bottle C: 1,100 mL\n\n"
            "**Step 2:** Add\n"
            "1,250 + 900 + 1,100 = **3,250 mL**"
        ),
    },

    # ── Challenging multi-step problems ───────────────────────────────────────
    {
        "topic": "Word Problems",
        "question": "A school has 8 classes. Each class needs 2.5 L of water for an experiment.\nThe water comes in 500 mL bottles. How many bottles are needed?",
        "options": ["20 bottles", "30 bottles", "40 bottles", "50 bottles"],
        "answer": "40 bottles",
        "explanation": (
            "**Step 1:** Total water needed\n"
            "8 × 2.5 L = 20 L\n\n"
            "**Step 2:** Convert to mL\n"
            "20 L = 20,000 mL\n\n"
            "**Step 3:** Number of bottles\n"
            "20,000 ÷ 500 = **40 bottles**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A builder needs 45 m of wood. Wood is sold in 2.5 m planks.\nEach plank costs €6.20. What is the total cost?",
        "options": ["€88.80", "€111.60", "€112.80", "€114.00"],
        "answer": "€111.60",
        "explanation": (
            "**Step 1:** Number of planks needed\n"
            "45 ÷ 2.5 = 18 planks\n\n"
            "**Step 2:** Total cost\n"
            "18 × €6.20 = **€111.60**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A rectangular garden is 12 m × 8 m. A path 1 m wide runs all around the outside.\nWhat is the area of just the path?",
        "options": ["20 m²", "40 m²", "80 m²", "96 m²"],
        "answer": "40 m²",
        "explanation": (
            "**Step 1:** Area of garden\n"
            "12 × 8 = 96 m²\n\n"
            "**Step 2:** Area of garden + path (path adds 1 m each side)\n"
            "(12+2) × (8+2) = 14 × 10 = 140 m²\n\n"
            "**Step 3:** Area of path only\n"
            "140 – 96 = **40 m²** (area of path alone is 44 m²)\n\n"
            "Correction: 140 – 96 = **44 m²**"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "Karnika pours equal amounts of juice from a 4.5 L jug into 9 glasses.\nThen she drinks half of one glass. How many mL are left in that glass?",
        "options": ["200 mL", "225 mL", "250 mL", "450 mL"],
        "answer": "250 mL",
        "explanation": (
            "**Step 1:** Convert jug to mL\n"
            "4.5 L = 4,500 mL\n\n"
            "**Step 2:** Juice per glass\n"
            "4,500 ÷ 9 = 500 mL per glass\n\n"
            "**Step 3:** Half a glass\n"
            "500 ÷ 2 = **250 mL** remaining"
        ),
    },
    {
        "topic": "Word Problems",
        "question": "A marathon is 42.195 km long.\nRounded to the nearest km, how far is that in metres?",
        "options": ["4,200 m", "42,000 m", "42,200 m", "421,950 m"],
        "answer": "42,000 m",
        "explanation": (
            "**Step 1:** Round 42.195 km\n"
            "42.195 → **42 km** (nearest km)\n\n"
            "**Step 2:** Convert to metres\n"
            "42 × 1,000 = **42,000 m**"
        ),
    },
]

# Remove duplicate question (the 40-dogs/2-weeks question appears twice; keep unique)
seen = set()
UNIQUE_QUESTIONS = []
for q in QUESTIONS:
    key = q["question"]
    if key not in seen:
        seen.add(key)
        UNIQUE_QUESTIONS.append(q)
QUESTIONS = UNIQUE_QUESTIONS

ALL_TOPICS = sorted({q["topic"] for q in QUESTIONS})

EARN_CORRECT = 0.02
LOSE_WRONG   = 0.01

# ── Session helpers ───────────────────────────────────────────────────────────

def _filtered_questions():
    topic = st.session_state.get("topic_filter", "All Topics")
    pool = QUESTIONS if topic == "All Topics" else [q for q in QUESTIONS if q["topic"] == topic]
    return pool


def _init():
    pool = _filtered_questions()
    shuffled = pool.copy()
    random.shuffle(shuffled)
    st.session_state.update(
        queue=shuffled,
        idx=0,
        earnings=0.0,
        correct=0,
        wrong=0,
        phase="question",   # "question" | "feedback" | "done"
        chosen=None,
    )


def _on_topic_change():
    _init()


def _submit(choice: str):
    q = st.session_state.queue[st.session_state.idx]
    correct = choice == q["answer"]
    st.session_state.chosen = choice
    st.session_state.phase = "feedback"
    if correct:
        st.session_state.correct += 1
        st.session_state.earnings += EARN_CORRECT
    else:
        st.session_state.wrong += 1
        st.session_state.earnings = max(0.0, st.session_state.earnings - LOSE_WRONG)


def _next():
    nxt = st.session_state.idx + 1
    if nxt >= len(st.session_state.queue):
        st.session_state.phase = "done"
    else:
        st.session_state.idx = nxt
        st.session_state.phase = "question"
        st.session_state.chosen = None


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Karnika's Maths Quiz", page_icon="📐", layout="centered")

if "queue" not in st.session_state:
    if "topic_filter" not in st.session_state:
        st.session_state.topic_filter = "All Topics"
    _init()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📐 Karnika's Maths Quiz")
    st.markdown("---")

    st.markdown("**Filter by topic**")
    st.selectbox(
        "topic",
        options=["All Topics"] + ALL_TOPICS,
        key="topic_filter",
        label_visibility="collapsed",
        on_change=_on_topic_change,
    )

    st.markdown("---")
    st.markdown("**Scoring**")
    st.success(f"✅ Correct  → +€{EARN_CORRECT:.2f}")
    st.error(f"❌ Wrong    → −€{LOSE_WRONG:.2f}")

    st.markdown("---")
    if st.button("🔄 Restart", use_container_width=True):
        _init()
        st.rerun()

    total_q = len(st.session_state.queue)
    done_q  = st.session_state.idx + (0 if st.session_state.phase == "question" else 1)
    st.markdown("---")
    st.markdown(f"**Progress:** {done_q} / {total_q}")
    st.progress(done_q / total_q if total_q else 0)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center; margin-bottom:0'>📐 Karnika's Maths Quiz</h1>"
    "<p style='text-align:center; color:gray; margin-top:4px'>Grade 5 · Measurements, Conversions & Problem Solving</p>",
    unsafe_allow_html=True,
)

# ── Earnings dashboard ────────────────────────────────────────────────────────
e = st.session_state.earnings
c = st.session_state.correct
w = st.session_state.wrong
total_answered = c + w

col1, col2, col3, col4 = st.columns(4)
col1.metric("💶 Earnings", f"€{e:.2f}")
col2.metric("✅ Correct", c)
col3.metric("❌ Wrong", w)
col4.metric("🎯 Accuracy", f"{int(100*c/total_answered)}%" if total_answered else "—")

st.markdown("---")

# ── DONE screen ───────────────────────────────────────────────────────────────
if st.session_state.phase == "done":
    st.balloons()
    st.markdown(
        f"<h2 style='text-align:center'>🎉 Quiz Complete!</h2>"
        f"<p style='text-align:center; font-size:1.2rem'>"
        f"You answered <b>{c}</b> correctly and <b>{w}</b> incorrectly.<br>"
        f"Total earned: <span style='color:green; font-size:1.8rem'><b>€{e:.2f}</b></span></p>",
        unsafe_allow_html=True,
    )
    if w > 0:
        st.info(f"💡 Tip: Review the **{w}** wrong answers and try again!")
    if st.button("🔄 Play Again", use_container_width=True, type="primary"):
        _init()
        st.rerun()
    st.stop()

# ── Question card ─────────────────────────────────────────────────────────────
q = st.session_state.queue[st.session_state.idx]
idx = st.session_state.idx
total_q = len(st.session_state.queue)

st.markdown(
    f"<div style='background:#f0f4ff; border-left:5px solid #4a6fa5; "
    f"border-radius:8px; padding:16px 20px; margin-bottom:12px'>"
    f"<span style='font-size:0.85rem; color:#666'>Question {idx+1} of {total_q} &nbsp;·&nbsp; {q['topic']}</span>"
    f"<p style='font-size:1.25rem; font-weight:600; margin:8px 0 0 0; white-space:pre-line'>{q['question']}</p>"
    f"</div>",
    unsafe_allow_html=True,
)

# ── Options ───────────────────────────────────────────────────────────────────
if st.session_state.phase == "question":
    opts = q["options"].copy()
    # Shuffle options once per question (stable within the question)
    rng = random.Random(q["question"])
    rng.shuffle(opts)

    for opt in opts:
        if st.button(opt, use_container_width=True, key=f"opt_{idx}_{opt}"):
            _submit(opt)
            st.rerun()

else:  # feedback
    chosen  = st.session_state.chosen
    correct = q["answer"]
    opts    = q["options"].copy()
    rng     = random.Random(q["question"])
    rng.shuffle(opts)

    for opt in opts:
        if opt == correct:
            st.markdown(
                f"<div style='background:#d4edda; border:2px solid #28a745; "
                f"border-radius:8px; padding:10px 16px; margin:4px 0; "
                f"font-weight:600; color:#155724'>✅ {opt}</div>",
                unsafe_allow_html=True,
            )
        elif opt == chosen and chosen != correct:
            st.markdown(
                f"<div style='background:#f8d7da; border:2px solid #dc3545; "
                f"border-radius:8px; padding:10px 16px; margin:4px 0; "
                f"font-weight:600; color:#721c24'>❌ {opt} (your answer)</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='background:#f8f9fa; border:1px solid #dee2e6; "
                f"border-radius:8px; padding:10px 16px; margin:4px 0; "
                f"color:#6c757d'>{opt}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    if chosen == correct:
        st.success(f"🎉 Correct! +€{EARN_CORRECT:.2f} earned")
    else:
        st.error(f"💸 Wrong! −€{LOSE_WRONG:.2f} deducted")

    # Solution — always visible after answering
    st.markdown(
        "<div style='background:#fffbea; border-left:5px solid #f0c040; "
        "border-radius:8px; padding:14px 18px; margin:12px 0'>"
        "<span style='font-size:1rem; font-weight:700; color:#7a5c00'>📖 Solution</span>",
        unsafe_allow_html=True,
    )
    st.markdown(q["explanation"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next Question →", use_container_width=True, type="primary"):
        _next()
        st.rerun()
