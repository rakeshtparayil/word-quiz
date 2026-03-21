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
        "options": ["100 kg", "160 kg", "200 kg", "400 kg"],
        "answer": "200 kg",
        "explanation": "40 dogs = 10× more dogs → 20 × 10 = 200 kg for 1 week\nFor 2 weeks: 200 × 2 = **400 kg**\n\n⚠️ Correct answer: **400 kg** — careful with the 2-week part!",
    },
    {
        "topic": "Word Problems",
        "question": "A 20 kg bag of food feeds 4 dogs for one week.\nHow many kilograms are needed to feed 40 dogs for TWO weeks?",
        "options": ["100 kg", "200 kg", "400 kg", "800 kg"],
        "answer": "400 kg",
        "explanation": "Per dog per week = 20 ÷ 4 = 5 kg\n40 dogs × 2 weeks × 5 kg = **400 kg**",
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
        "explanation": "3,000 ÷ 1,000 = **3 kg** ✓\n(5 km = 5,000 m; 2 L = 2,000 mL; 4 cm = 40 mm)",
    },
    {
        "topic": "Mixed Calculations",
        "question": "What is 1.5 km + 800 m + 70,000 cm expressed in metres?",
        "options": ["2,300 m", "3,000 m", "3,800 m", "72,300 m"],
        "answer": "3,000 m",
        "explanation": "1.5 km = 1,500 m; 800 m; 70,000 cm = 700 m\n1,500 + 800 + 700 = **3,000 m**",
    },
    {
        "topic": "Mixed Calculations",
        "question": "A string is 3 m long. You cut off 45 cm. How much is left in cm?",
        "options": ["205 cm", "245 cm", "255 cm", "295 cm"],
        "answer": "255 cm",
        "explanation": "3 m = 300 cm; 300 – 45 = **255 cm**",
    },
    {
        "topic": "Mixed Calculations",
        "question": "How many grams are in 2 kg 450 g?",
        "options": ["245 g", "2,045 g", "2,450 g", "24,500 g"],
        "answer": "2,450 g",
        "explanation": "2 kg = 2,000 g; 2,000 + 450 = **2,450 g**",
    },
    {
        "topic": "Mixed Calculations",
        "question": "A bottle holds 1.5 L. How many 250 mL glasses can it fill?",
        "options": ["4", "5", "6", "8"],
        "answer": "6",
        "explanation": "1.5 L = 1,500 mL; 1,500 ÷ 250 = **6 glasses**",
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

    with st.expander("💡 See explanation"):
        st.markdown(q["explanation"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next Question →", use_container_width=True, type="primary"):
        _next()
        st.rerun()
