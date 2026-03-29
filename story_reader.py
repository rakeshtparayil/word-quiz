import streamlit as st
import difflib
import re
import io
import os
import tempfile

# ── Story bank ────────────────────────────────────────────────────────────────

STORIES = {
    "The Old Lighthouse": {
        "level": "Grade 4–5",
        "text": (
            "On a rocky cliff above the sea stood an old lighthouse. "
            "Its white walls were worn by years of salt and wind. "
            "Every night the keeper climbed the spiral staircase and lit the great lamp. "
            "Ships far out at sea could see the beam sweeping across the dark water. "
            "One stormy evening the lamp flickered and nearly went out. "
            "The keeper worked quickly, replacing the oil and trimming the wick. "
            "By midnight the light was burning steadily once more. "
            "The sailors on the distant ship breathed a sigh of relief. "
            "They steered safely around the hidden rocks and reached the harbour by dawn. "
            "The old lighthouse had saved them again."
        ),
    },
    "Journey to the Stars": {
        "level": "Grade 5",
        "text": (
            "Maya had always dreamed of becoming an astronaut. "
            "Every clear night she would lie on the grass and count the stars. "
            "She studied hard, learning about gravity, planets, and the speed of light. "
            "One morning a letter arrived inviting her to a special science camp. "
            "At the camp she built rockets, programmed robots, and grew vegetables in simulated soil. "
            "Her team won the challenge by designing a satellite that could collect solar energy. "
            "The judges were impressed by her creativity and determination. "
            "Maya returned home with a certificate and a brand new telescope. "
            "That night she pointed it at Jupiter and saw its four largest moons. "
            "She smiled and wrote in her notebook: one day I will visit you."
        ),
    },
    "The Wise Old River": {
        "level": "Grade 4–5",
        "text": (
            "Deep in the forest there was a river that had flowed for thousands of years. "
            "The animals came to drink from its cool, clear water every morning. "
            "One summer the rain stopped and the river began to shrink. "
            "The deer, the rabbit, and the fox all became worried. "
            "They asked the ancient tortoise what they should do. "
            "The tortoise said that the forest needed more trees to bring back the rain. "
            "So all the animals worked together, planting seedlings along the riverbank. "
            "They watered the young trees carefully every day without fail. "
            "Months passed, and slowly the clouds returned to the valley. "
            "The river rose again, and the forest was green and alive once more."
        ),
    },
    "Karnika's Brilliant Idea": {
        "level": "Grade 5",
        "text": (
            "Karnika noticed that her school used enormous amounts of paper every week. "
            "Worksheets, notices, and test papers were printed and then thrown away. "
            "She decided to present a solution to the school council. "
            "First she collected data, counting the sheets used in each classroom. "
            "Then she calculated how many trees were needed to produce that much paper. "
            "The number surprised everyone, including the headteacher. "
            "Karnika suggested switching to digital worksheets and a shared notice board. "
            "She also proposed a recycling station near every classroom. "
            "The council voted unanimously in favour of her plan. "
            "Within three months the school had reduced its paper use by sixty percent."
        ),
    },
}

# ── Text utilities ────────────────────────────────────────────────────────────

def tokenise(text):
    """Return list of (original_token, normalised_token) pairs, preserving punctuation tokens."""
    tokens = re.findall(r"[A-Za-z']+|[^A-Za-z'\s]", text)
    result = []
    for t in tokens:
        norm = re.sub(r"[^a-z]", "", t.lower())
        result.append((t, norm))
    return result


def compare(original_text: str, spoken_text: str):
    """
    Align spoken tokens to original tokens using difflib.
    Returns list of dicts: {original, status}
    status: 'correct' | 'wrong' | 'missed'
    """
    orig_tokens  = tokenise(original_text)
    spok_tokens  = tokenise(spoken_text)

    orig_words   = [t for t in orig_tokens  if t[1]]   # skip punctuation
    spok_words   = [t for t in spok_tokens  if t[1]]

    orig_norm = [t[1] for t in orig_words]
    spok_norm = [t[1] for t in spok_words]

    matcher = difflib.SequenceMatcher(None, orig_norm, spok_norm, autojunk=False)
    results = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for tok in orig_words[i1:i2]:
                results.append({"original": tok[0], "norm": tok[1], "status": "correct"})
        elif tag == "replace":
            for tok in orig_words[i1:i2]:
                # partial-match: if spoken word is ≥ 70 % similar, call it 'close'
                spok_chunk = " ".join(t[0] for t in spok_words[j1:j2])
                ratio = max(
                    (difflib.SequenceMatcher(None, tok[1], s).ratio()
                     for s in spok_norm[j1:j2]),
                    default=0,
                )
                status = "close" if ratio >= 0.7 else "wrong"
                results.append({"original": tok[0], "norm": tok[1],
                                 "status": status, "spoken": spok_chunk})
        elif tag == "delete":
            for tok in orig_words[i1:i2]:
                results.append({"original": tok[0], "norm": tok[1], "status": "missed"})
        # "insert" → extra words spoken, ignored for scoring

    return results


@st.cache_resource(show_spinner="Loading speech model (first time only)…")
def _load_whisper():
    """Load the Whisper tiny model – cached so it's only loaded once."""
    import whisper
    return whisper.load_model("tiny")


def transcribe(audio_bytes: bytes) -> str:
    """
    Transcribe audio using OpenAI Whisper (local, no API key, no FLAC binary).
    Works on Apple Silicon and Intel Macs.
    """
    model = _load_whisper()
    # Write bytes to a temp WAV file – Whisper reads files, not bytes
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    try:
        result = model.transcribe(tmp_path, language="en", fp16=False)
        return result["text"].strip()
    finally:
        os.unlink(tmp_path)


# ── Word badge HTML ───────────────────────────────────────────────────────────

COLOURS = {
    "correct": ("#d4edda", "#155724", "✓"),
    "close":   ("#fff3cd", "#856404", "~"),
    "wrong":   ("#f8d7da", "#721c24", "✗"),
    "missed":  ("#e2e3f3", "#383d8d", "—"),
    "override_ok":  ("#d4edda", "#155724", "✓"),
    "override_bad": ("#f8d7da", "#721c24", "✗"),
}

def word_badge(word, status):
    bg, fg, icon = COLOURS.get(status, ("#eee", "#333", ""))
    return (
        f"<span style='display:inline-block; margin:3px 2px; padding:3px 8px; "
        f"border-radius:6px; background:{bg}; color:{fg}; font-size:1.05rem; "
        f"font-weight:600; border:1px solid {fg}33'>"
        f"{word} <sup style='font-size:0.65rem'>{icon}</sup></span>"
    )


# ── Page setup ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Story Reader",
    page_icon="📖",
    layout="wide",
)

# ── Session state defaults ────────────────────────────────────────────────────

for key, val in {
    "results":     None,    # list of word dicts after analysis
    "transcript":  "",
    "overrides":   {},      # idx -> True(correct) / False(wrong)
    "analysed":    False,
    "story_key":   list(STORIES.keys())[0],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📖 Story Reader")
    st.markdown("---")

    story_key = st.selectbox(
        "Choose a story",
        list(STORIES.keys()),
        index=list(STORIES.keys()).index(st.session_state.story_key),
    )
    if story_key != st.session_state.story_key:
        st.session_state.story_key      = story_key
        st.session_state.results        = None
        st.session_state.transcript     = ""
        st.session_state.overrides      = {}
        st.session_state.analysed       = False

    story = STORIES[story_key]
    st.caption(f"Level: {story['level']}")
    st.markdown("---")

    st.markdown("**Legend**")
    for label, (bg, fg, icon) in COLOURS.items():
        if label.startswith("override"):
            continue
        st.markdown(
            f"<span style='background:{bg};color:{fg};padding:2px 8px;"
            f"border-radius:5px;font-weight:600'>{icon} {label.title()}</span>",
            unsafe_allow_html=True,
        )
    st.markdown("---")
    st.markdown(
        "**How it works**\n\n"
        "1. Read the story card\n"
        "2. Press **Record** and read aloud\n"
        "3. Press **Analyse** to check\n"
        "4. Toggle any word to correct it"
    )
    if st.session_state.analysed:
        st.markdown("---")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.results    = None
            st.session_state.transcript = ""
            st.session_state.overrides  = {}
            st.session_state.analysed   = False
            st.rerun()


# ── Header ────────────────────────────────────────────────────────────────────

st.markdown(
    "<h1 style='text-align:center;margin-bottom:0'>📖 Story Reader</h1>"
    "<p style='text-align:center;color:gray;margin-top:4px'>"
    "Record your reading – see every word marked right or wrong</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

story_text = story["text"]

# ── Two-column layout ─────────────────────────────────────────────────────────

col_story, col_record = st.columns([3, 2], gap="large")

# ── LEFT: story card ──────────────────────────────────────────────────────────
with col_story:
    st.markdown(f"### {story_key}")
    sentences = re.split(r'(?<=[.!?])\s+', story_text)

    if not st.session_state.analysed:
        # Plain story display (before recording)
        st.markdown(
            "<div style='background:#f7f9ff;border-left:5px solid #4a6fa5;"
            "border-radius:8px;padding:20px 24px;font-size:1.15rem;line-height:2'>"
            + story_text +
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        # Colour-coded word display (after analysis)
        results   = st.session_state.results
        overrides = st.session_state.overrides

        html = (
            "<div style='background:#f7f9ff;border-left:5px solid #4a6fa5;"
            "border-radius:8px;padding:20px 24px;line-height:2.6;font-size:1.05rem'>"
        )
        for i, r in enumerate(results):
            status = r["status"]
            if i in overrides:
                status = "override_ok" if overrides[i] else "override_bad"
            html += word_badge(r["original"], status)
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

        # ── Transcript box ────────────────────────────────────────────────────
        st.markdown("**What was heard:**")
        st.info(st.session_state.transcript or "_(nothing recognised)_")


# ── RIGHT: record + score ─────────────────────────────────────────────────────
with col_record:

    if not st.session_state.analysed:
        st.markdown("### 🎙️ Record your reading")
        st.markdown(
            "<div style='background:#fffbea;border:1px solid #f0c040;"
            "border-radius:8px;padding:12px 16px;font-size:0.95rem'>"
            "💡 <b>Tip:</b> Press the microphone, read the whole story, then press stop.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("")

        audio = st.audio_input("Press the microphone to start recording")

        if audio:
            st.success("Recording captured! Press **Analyse** to check your reading.")
            if st.button("🔍 Analyse Reading", type="primary", use_container_width=True):
                with st.spinner("Transcribing your voice…"):
                    try:
                        transcript = transcribe(audio.read())
                        results    = compare(story_text, transcript)
                        st.session_state.transcript = transcript
                        st.session_state.results    = results
                        st.session_state.overrides  = {}
                        st.session_state.analysed   = True
                        st.rerun()
                    except sr.UnknownValueError:
                        st.error("Could not understand the audio. Please try again in a quieter place.")
                    except sr.RequestError as e:
                        st.error(f"Speech service error: {e}. Check your internet connection.")

    else:
        # ── Score dashboard ───────────────────────────────────────────────────
        results   = st.session_state.results
        overrides = st.session_state.overrides

        n_total   = len(results)
        n_correct = sum(
            1 for i, r in enumerate(results)
            if (i in overrides and overrides[i]) or
               (i not in overrides and r["status"] in ("correct", "close"))
        )
        n_wrong   = n_total - n_correct
        accuracy  = int(100 * n_correct / n_total) if n_total else 0

        st.markdown("### 📊 Result")
        m1, m2, m3 = st.columns(3)
        m1.metric("✅ Correct",  n_correct)
        m2.metric("❌ Wrong",    n_wrong)
        m3.metric("🎯 Accuracy", f"{accuracy}%")

        # Progress bar
        bar_col = "#28a745" if accuracy >= 80 else "#ffc107" if accuracy >= 60 else "#dc3545"
        st.markdown(
            f"<div style='background:#eee;border-radius:8px;height:18px;margin:8px 0'>"
            f"<div style='background:{bar_col};width:{accuracy}%;height:18px;"
            f"border-radius:8px;transition:width 0.5s'></div></div>",
            unsafe_allow_html=True,
        )
        if accuracy == 100:
            st.balloons()
            st.success("🌟 Perfect reading! Amazing job!")
        elif accuracy >= 80:
            st.success("🎉 Great reading! Keep it up!")
        elif accuracy >= 60:
            st.warning("👍 Good effort! Practice the highlighted words.")
        else:
            st.error("💪 Keep practising – you're getting there!")

        st.markdown("---")

        # ── Wrong / missed word list ──────────────────────────────────────────
        problem_words = [
            (i, r) for i, r in enumerate(results)
            if r["status"] in ("wrong", "missed", "close")
            and i not in overrides
        ]
        if problem_words:
            st.markdown("**Words to practise:**")
            for i, r in problem_words:
                icon = "❌" if r["status"] == "wrong" else ("—" if r["status"] == "missed" else "~")
                st.markdown(
                    f"<span style='font-size:1rem'>{icon} <b>{r['original']}</b> "
                    f"<span style='color:gray;font-size:0.85rem'>"
                    f"({'not said' if r['status']=='missed' else 'said differently'})"
                    f"</span></span>",
                    unsafe_allow_html=True,
                )
        else:
            st.success("No problem words! 🌟")

        st.markdown("---")

        # ── Parent correction panel ───────────────────────────────────────────
        st.markdown("### ✏️ Parent Corrections")
        st.caption("Toggle any word the automatic check got wrong.")

        for i, r in enumerate(results):
            current_status = r["status"]
            if i in overrides:
                current_status = "override_ok" if overrides[i] else "override_bad"

            is_ok = current_status in ("correct", "close", "override_ok")
            btn_label = f"{'✅' if is_ok else '❌'}  {r['original']}"
            btn_help  = "Click to mark as WRONG" if is_ok else "Click to mark as CORRECT"

            if st.button(btn_label, key=f"tog_{i}", help=btn_help, use_container_width=True):
                # Toggle the override
                st.session_state.overrides[i] = not is_ok
                st.rerun()
