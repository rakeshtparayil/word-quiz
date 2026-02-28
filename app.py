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
MAX_EUROS = TOTAL_WORDS * 0.10

def init_state():
    if "queue" not in st.session_state:
        queue = WORDS.copy()
        random.shuffle(queue)
        st.session_state.queue = queue
        st.session_state.index = 0
        st.session_state.euros = 0.0
        st.session_state.correct_count = 0
        st.session_state.wrong_count = 0
        st.session_state.wrong_words = []
        st.session_state.submitted = False
        st.session_state.feedback = ""
        st.session_state.finished = False
    # total_euros and cycles_done persist across cycles
    if "total_euros" not in st.session_state:
        st.session_state.total_euros = 0.0
    if "cycles_done" not in st.session_state:
        st.session_state.cycles_done = 0

def restart():
    # preserve cumulative totals
    total_euros = st.session_state.get("total_euros", 0.0)
    cycles_done = st.session_state.get("cycles_done", 0)
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.total_euros = total_euros
    st.session_state.cycles_done = cycles_done

def next_word():
    next_index = st.session_state.index + 1
    if next_index >= TOTAL_WORDS:
        st.session_state.finished = True
        st.session_state.total_euros += st.session_state.euros
        st.session_state.cycles_done += 1
    else:
        st.session_state.index = next_index
        st.session_state.submitted = False
        st.session_state.feedback = ""

init_state()

st.title("Word Type & Verb Quiz")
st.caption("Turning adjectives and nouns into verbs using -ify, -ise, -ate, -en")
st.markdown("---")

# ── Finished screen ───────────────────────────────────────────────────────────
if st.session_state.finished:
    euros = st.session_state.euros
    correct = st.session_state.correct_count
    wrong = st.session_state.wrong_count
    wrong_words = st.session_state.wrong_words

    st.balloons()
    st.markdown("## Cycle Complete! 🎉")
    st.markdown("---")

    # Score summary
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("✅ Correct", correct)
    with c2:
        st.metric("❌ Wrong", wrong)
    with c3:
        st.metric("💶 This Cycle", f"€{euros:.2f}", help=f"Max per cycle: €{MAX_EUROS:.2f}")
    with c4:
        st.metric("🏦 All Cycles Total", f"€{st.session_state.total_euros:.2f}",
                  help=f"Across {st.session_state.cycles_done} cycle(s)")

    pct = max(0.0, (euros / MAX_EUROS)) * 100
    st.progress(max(0.0, min(1.0, euros / MAX_EUROS)))
    st.markdown(f"**Score: {pct:.1f}%**")

    if correct == TOTAL_WORDS:
        st.success("Perfect score! Outstanding work!")
    elif pct >= 75:
        st.success("Great job! Keep it up!")
    elif pct >= 50:
        st.warning("Good effort! Review the missed words and try again.")
    else:
        st.error("Keep practising — you'll get there!")

    # Wrong words table
    if wrong_words:
        st.markdown("---")
        st.markdown("### ❌ Words You Got Wrong")
        st.markdown("Review these before your next cycle:")

        header = "| Word | Your Type | Correct Type | Your Verb | Correct Verb |"
        divider = "|---|---|---|---|---|"
        rows = [header, divider]
        for w in wrong_words:
            type_mark = "✅" if w["type_correct"] else "❌"
            verb_mark = "✅" if w["verb_correct"] else "❌"
            rows.append(
                f"| **{w['word']}** "
                f"| {type_mark} {w['your_type']} "
                f"| {w['correct_type']} "
                f"| {verb_mark} {w['your_verb']} "
                f"| {w['correct_verb']} |"
            )
        st.markdown("\n".join(rows))
    else:
        st.success("You got every single word right — no mistakes!")

    st.write("")
    if st.button("🔄 Start New Cycle", type="primary"):
        restart()
        st.rerun()

# ── Quiz screen ───────────────────────────────────────────────────────────────
else:
    idx = st.session_state.index
    current = st.session_state.queue[idx]
    word = current["word"]

    st.progress(idx / TOTAL_WORDS)
    st.caption(f"Word {idx + 1} of {TOTAL_WORDS}   |   ✅ {st.session_state.correct_count}   ❌ {st.session_state.wrong_count}")

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
                    st.session_state.correct_count += 1
                else:
                    lines.append("**Not fully correct. -€0.05** ❌")
                    st.session_state.wrong_count += 1
                    st.session_state.wrong_words.append({
                        "word": word,
                        "your_type": word_type,
                        "correct_type": correct_type,
                        "type_correct": type_correct,
                        "your_verb": user_verb,
                        "correct_verb": correct_verb,
                        "verb_correct": verb_correct,
                    })

                st.session_state.euros += earned
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
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("✅ Correct", st.session_state.correct_count)
    with c2:
        st.metric("❌ Wrong", st.session_state.wrong_count)
    with c3:
        st.metric("💶 This Cycle", f"€{st.session_state.euros:.2f}",
                  help="Both correct: +€0.10 | Any wrong: -€0.05")
    with c4:
        st.metric("🏦 All Cycles Total", f"€{st.session_state.total_euros:.2f}",
                  help=f"Across {st.session_state.cycles_done} completed cycle(s)")

    if st.button("🔄 Restart Quiz"):
        restart()
        st.rerun()
