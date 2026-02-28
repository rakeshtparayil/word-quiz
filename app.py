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

def init_state():
    if "queue" not in st.session_state:
        queue = WORDS.copy()
        random.shuffle(queue)
        st.session_state.queue = queue
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.total = 0
        st.session_state.submitted = False
        st.session_state.feedback = ""

def next_word():
    st.session_state.index += 1
    if st.session_state.index >= len(st.session_state.queue):
        random.shuffle(st.session_state.queue)
        st.session_state.index = 0
    st.session_state.submitted = False
    st.session_state.feedback = ""

init_state()

st.title("Word Type & Verb Quiz")
st.caption("Turning adjectives and nouns into verbs using -ify, -ise, -ate, -en")

st.markdown("---")

current = st.session_state.queue[st.session_state.index]
word = current["word"]

st.markdown(f"### Word:  **{word.upper()}**")
st.write("")

col1, col2 = st.columns(2)

with col1:
    word_type = st.radio(
        "Is this word a...",
        ["adjective", "noun"],
        key=f"type_{st.session_state.index}",
        disabled=st.session_state.submitted,
    )

with col2:
    verb_input = st.text_input(
        "Write the verb form:",
        key=f"verb_{st.session_state.index}",
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

            st.session_state.total += 1
            points = 0
            lines = []

            if type_correct:
                points += 1
                lines.append(f"✅ Word type: **{correct_type}** — correct!")
            else:
                lines.append(f"❌ Word type: you said **{word_type}**, correct answer is **{correct_type}**")

            if verb_correct:
                points += 1
                lines.append(f"✅ Verb form: **{correct_verb}** — correct!")
            else:
                lines.append(f"❌ Verb form: you wrote **{user_verb}**, correct answer is **{correct_verb}**")

            st.session_state.score += points
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
total_possible = st.session_state.total * 2 if st.session_state.total > 0 else 1
st.metric("Score", f"{st.session_state.score} / {st.session_state.total * 2}")

if st.button("🔄 Restart Quiz"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
