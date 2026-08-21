import streamlit as st

from core.groq_engine import (
    generate_text
)

from core.session_manager import (
    load_sessions,
    load_rep_history
)

st.set_page_config(
    page_title="AI Coach",
    page_icon=None,
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()

st.title("AI Coach")

st.write(
    "Ask questions about your exercise performance "
    "and receive feedback based on your recorded workouts."
)

sessions = load_sessions()
reps = load_rep_history()

if sessions.empty:

    st.info(
        "No workout history is available yet."
    )

    st.write(
        "Complete an exercise analysis first."
    )

    st.stop()

question = st.text_area(
    "Ask your question",
    placeholder=(
        "For example: What is my biggest weakness?"
    ),
    height=120
)

if st.button(
    "Ask AI Coach",
    type="primary"
):

    if not question.strip():

        st.warning(
            "Enter a question first."
        )

        st.stop()

    session_data = sessions.tail(
        10
    ).to_dict(
        orient="records"
    )

    rep_data = []

    if not reps.empty:

        rep_data = reps.tail(
            30
        ).to_dict(
            orient="records"
        )

    prompt = f"""
You are FORMRAGE AI Coach.

The user asked:

{question}

Use only the workout information
provided below.

Recent workout history:

{session_data}

Recent repetition information:

{rep_data}

Give a concise and practical answer.

Focus on:

Form improvement.
Exercise technique.
Repetition consistency.
Weak areas.
Progress.
Specific recommendations.

Do not provide medical diagnosis.

If the available data does not support
a conclusion, clearly say that.

Answer directly to the user.
"""

    try:

        with st.spinner(
            "AI Coach is analyzing your workout history..."
        ):

            response = generate_text(
                prompt
            )

        st.markdown("---")

        st.header(
            "Coach Response"
        )

        st.write(
            response
        )

    except Exception as error:

        st.error(
            "AI Coach could not process the request."
        )

        st.exception(
            error
        )