import streamlit as st
import random

# ── German number logic ─────────────────────────────────────────────────────

_ONES = [
    "", "ein", "zwei", "drei", "vier", "fünf",
    "sechs", "sieben", "acht", "neun",
]
_TEENS = [
    "zehn", "elf", "zwölf", "dreizehn", "vierzehn",
    "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn",
]
_TENS = [
    "", "zehn", "zwanzig", "dreißig", "vierzig",
    "fünfzig", "sechzig", "siebzig", "achtzig", "neunzig",
]


def _below_hundred(n: int) -> str:
    if n == 0:
        return ""
    if n < 10:
        return _ONES[n]
    if n < 20:
        return _TEENS[n - 10]
    ten, one = divmod(n, 10)
    return (_ONES[one] + "und" + _TENS[ten]) if one else _TENS[ten]


def _below_thousand(n: int) -> str:
    if n < 100:
        return _below_hundred(n)
    h, rest = divmod(n, 100)
    return _ONES[h] + "hundert" + _below_hundred(rest)


def number_to_german(n: int) -> str:
    """Return the canonical German word(s) for n (0 – 10 000)."""
    if n == 0:
        return "null"
    if n == 1:
        return "eins"
    if n < 100:
        return _below_hundred(n)
    if n < 1000:
        result = _below_thousand(n)
    else:
        t, rest = divmod(n, 1000)
        t_word = "zehn" if t == 10 else _ONES[t]
        result = t_word + "tausend" + _below_thousand(rest)
    # Numbers whose last two digits are 01 (e.g. 101, 201, 1001) end in "eins"
    if n % 100 == 1:
        result = result[:-3] + "eins"
    return result


def valid_answers(n: int) -> set[str]:
    """All accepted spellings for n (lower-cased)."""
    primary = number_to_german(n).lower()
    accepted = {primary}
    accepted.add(primary.replace("einhundert", "hundert"))
    if n == 1000:
        accepted.add("tausend")
    return accepted


# ── Range config ─────────────────────────────────────────────────────────────

RANGES = {
    "1 – 100":        (1,     100),
    "101 – 1,000":    (101,   1_000),
    "1,001 – 10,000": (1_001, 10_000),
    "All (1 – 10,000)": (1,  10_000),
}


# ── Session-state helpers ────────────────────────────────────────────────────

def _pick_number() -> int:
    lo, hi = RANGES[st.session_state.range_label]
    return random.randint(lo, hi)


def _init():
    if "range_label" not in st.session_state:
        st.session_state.range_label = "1 – 100"
    st.session_state.update(
        number=_pick_number(),
        wrong=0,
        total=0,
        phase="question",
        last_ok=None,
        canon="",
    )


def _next():
    st.session_state.number = _pick_number()
    st.session_state.phase = "question"


def _check(user_text: str):
    n = st.session_state.number
    ok = user_text.strip().lower() in valid_answers(n)
    st.session_state.total += 1
    if not ok:
        st.session_state.wrong += 1
    st.session_state.last_ok = ok
    st.session_state.canon = number_to_german(n)
    st.session_state.phase = "feedback"


def _on_range_change():
    """Called when the sidebar range selector changes."""
    st.session_state.number = _pick_number()
    st.session_state.wrong = 0
    st.session_state.total = 0
    st.session_state.phase = "question"
    st.session_state.last_ok = None
    st.session_state.canon = ""


# ── App ──────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Deutsch Zahlen Trainer",
    page_icon="🇩🇪",
    layout="centered",
)

if "number" not in st.session_state:
    _init()

# ── Sidebar – range filter ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("**Number range**")

    selected = st.radio(
        "range",
        options=list(RANGES.keys()),
        index=list(RANGES.keys()).index(st.session_state.range_label),
        label_visibility="collapsed",
        on_change=_on_range_change,
        key="range_label",
    )

    lo, hi = RANGES[st.session_state.range_label]
    st.caption(f"Numbers drawn from **{lo:,}** to **{hi:,}**")

    st.markdown("---")
    if st.button("🔄 Restart / Reset score", use_container_width=True):
        _on_range_change()
        st.rerun()

    st.markdown("---")
    with st.expander("📖 Quick Reference"):
        st.markdown(
            """
| # | Deutsch |
|---|---------|
| 1 | eins |
| 2 | zwei |
| 11 | elf |
| 12 | zwölf |
| 20 | zwanzig |
| 21 | einundzwanzig |
| 30 | dreißig |
| 100 | einhundert |
| 1 000 | eintausend |
| 10 000 | zehntausend |

**Compound rule:**  
ones + **und** + tens  
→ `drei` + `und` + `zwanzig` = `dreiundzwanzig` (23)
"""
        )

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center; margin-bottom:0'>🇩🇪 Deutsch Zahlen</h1>"
    f"<p style='text-align:center; color:gray; margin-top:4px'>"
    f"Range: <b>{st.session_state.range_label}</b> — type the German name</p>",
    unsafe_allow_html=True,
)

# ── Score bar ────────────────────────────────────────────────────────────────
total = st.session_state.total
wrong = st.session_state.wrong
correct = total - wrong
acc = f"{int(100 * correct / total)}%" if total else "—"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Shown", total)
c2.metric("✅ Correct", correct)
c3.metric("❌ Wrong", wrong)
c4.metric("Accuracy", acc)

st.markdown("---")

# ── Number display ────────────────────────────────────────────────────────────
number = st.session_state.number

st.markdown(
    f"<div style='"
    f"text-align:center; font-size:6rem; font-weight:800; "
    f"letter-spacing:2px; padding:24px 0; line-height:1'>"
    f"{number:,}</div>",
    unsafe_allow_html=True,
)

# ── Input / Feedback ──────────────────────────────────────────────────────────
if st.session_state.phase == "question":
    with st.form("answer_form", clear_on_submit=True):
        user_input = st.text_input(
            "German word:",
            placeholder="e.g. dreitausendvierhundertfünf",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button(
            "Check ✔", use_container_width=True, type="primary"
        )

    if submitted:
        if user_input.strip():
            _check(user_input)
            st.rerun()
        else:
            st.warning("Please type an answer before checking.")

else:  # feedback
    if st.session_state.last_ok:
        st.success("✓  Richtig! (Correct!)", icon="🎉")
    else:
        st.error(
            f"✗  Falsch! The correct answer is:  **{st.session_state.canon}**",
            icon="❌",
        )

    if st.button("Next number →", use_container_width=True, type="primary"):
        _next()
        st.rerun()
