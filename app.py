import streamlit as st
import random

WORDS = [
    {"word": "agony",         "type": "noun",      "verb": "agonise"},
    {"word": "author",        "type": "noun",      "verb": "authorise"},
    {"word": "broad",         "type": "adjective", "verb": "broaden"},
    {"word": "capital",       "type": "noun",      "verb": "capitalise"},
    {"word": "central",       "type": "adjective", "verb": "centralise"},
    {"word": "clear",         "type": "adjective", "verb": "clarify"},
    {"word": "deep",          "type": "adjective", "verb": "deepen"},
    {"word": "empathy",       "type": "noun",      "verb": "empathise"},
    {"word": "flat",          "type": "adjective", "verb": "flatten"},
    {"word": "humid",         "type": "adjective", "verb": "humidify"},
    {"word": "identity",      "type": "noun",      "verb": "identify"},
    {"word": "indication",    "type": "noun",      "verb": "indicate"},
    {"word": "intensity",     "type": "noun",      "verb": "intensify"},
    {"word": "just",          "type": "adjective", "verb": "justify"},
    {"word": "magnification", "type": "noun",      "verb": "magnify"},
    {"word": "memory",        "type": "noun",      "verb": "memorise"},
    {"word": "navigation",    "type": "noun",      "verb": "navigate"},
    {"word": "participant",   "type": "noun",      "verb": "participate"},
    {"word": "peaceful",      "type": "adjective", "verb": "pacify"},
    {"word": "priority",      "type": "noun",      "verb": "prioritise"},
    {"word": "private",       "type": "adjective", "verb": "privatise"},
    {"word": "pure",          "type": "adjective", "verb": "purify"},
    {"word": "ripe",          "type": "adjective", "verb": "ripen"},
    {"word": "significant",   "type": "adjective", "verb": "signify"},
    {"word": "thick",         "type": "adjective", "verb": "thicken"},
    {"word": "unity",         "type": "noun",      "verb": "unify"},
]

TOTAL_WORDS = len(WORDS)
MAX_EUROS = TOTAL_WORDS * 0.10  # €0.10 per word if both answers correct

def init_state():
    if "queue" not in st.session_state:
        queue = WORDS.copy()
        random.shuffle(queue)
        st.session_state.queue = queue
        st.session_state.index = 0
        st.session_state.cents = 0.0  # euros
        st.session_state.submitted = False
        st.session_state.feedback = ""
        st.session_state.finished = False

def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def next_word():
    next_index = st.session_state.index + 1
    if next_index >= TOTAL_WORDS:
        st.session_state.finished = True
    else:
        st.session_state.index = next_index
        st.session_state.submitted = False
        st.session_state.feedback = ""

init_state()

st.title("Word Type & Verb Quiz")
st.caption("Turning adjectives and nouns into verbs using -ify, -ise, -ate, -en")
st.markdown("---")

# ── Finished screen ──────────────────────────────────────────────────────────
if st.session_state.finished:
    cents = st.session_state.cents
    st.balloons()
    st.markdown("## Cycle Complete! 🎉")
    st.markdown(f"You went through all **{TOTAL_WORDS} words**.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Earned", f"€{cents:.2f}")
    with col2:
        st.metric("Max Possible", f"€{MAX_EUROS:.2f}")

    pct = (cents / MAX_EUROS) * 100
    st.progress(max(0.0, min(1.0, cents / MAX_EUROS)))
    st.markdown(f"**Score: {pct:.1f}%**")

    if cents == MAX_CENTS:
        st.success("Perfect score! Outstanding work!")
    elif pct >= 75:
        st.success("Great job! Keep it up!")
    elif pct >= 50:
        st.warning("Good effort! Review the missed words and try again.")
    else:
        st.error("Keep practising — you'll get there!")

    st.write("")
    if st.button("🔄 Start New Cycle", type="primary"):
        restart()
        st.rerun()

# ── Quiz screen ───────────────────────────────────────────────────────────────
else:
    idx = st.session_state.index
    current = st.session_state.queue[idx]
    word = current["word"]

    # Progress bar
    progress = idx / TOTAL_WORDS
    st.progress(progress)
    st.caption(f"Word {idx + 1} of {TOTAL_WORDS}")

    st.markdown(f"### Word:  **{word.upper()}**")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        word_type = st.radio(
            "Is this word a...",
            ["adjective", "noun"],
            key=f"type_{idx}",
            disabled=st.session_state.submitted,
        )

    with col2:
        verb_input = st.text_input(
            "Write the verb form:",
            key=f"verb_{idx}",
            disabled=st.session_state.submitted,
            placeholder="e.g. clarify",
        )

    st.write("")

    if not st.session_state.submitted:
        if st.button("Submit", type="primary"):
            if not verb_input.strip():
                st.warning("Please write the verb form before submitting.")
            else:
                correct_type = current["type"]
                correct_verb = current["verb"]
                user_verb = verb_input.strip().lower()

                type_correct = word_type == correct_type
                verb_correct = user_verb == correct_verb
                both_correct = type_correct and verb_correct

                earned = 0.10 if both_correct else -0.05
                lines = []

                if type_correct:
                    lines.append(f"✅ Word type: **{correct_type}** — correct!")
                else:
                    lines.append(f"❌ Word type: you said **{word_type}**, correct is **{correct_type}**")

                if verb_correct:
                    lines.append(f"✅ Verb form: **{correct_verb}** — correct!")
                else:
                    lines.append(f"❌ Verb form: you wrote **{user_verb}**, correct is **{correct_verb}**")

                if both_correct:
                    lines.append("**Both correct! +€0.10** 🎉")
                else:
                    lines.append("**Not fully correct. -€0.05** ❌")

                st.session_state.cents += earned
                st.session_state.feedback = "\n\n".join(lines)
                st.session_state.submitted = True
                st.rerun()

    if st.session_state.submitted:
        st.markdown(st.session_state.feedback)
        st.write("")
        if st.button("Next Word ➡️"):
            next_word()
            st.rerun()

    st.markdown("---")
    st.metric("Earnings so far", f"€{st.session_state.cents:.2f}",
              help=f"Max possible: €{MAX_EUROS:.2f}  |  Both correct: +€0.10, Any wrong: -€0.05")

    if st.button("🔄 Restart Quiz"):
        restart()
        st.rerun()
