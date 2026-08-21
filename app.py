import streamlit as st

st.set_page_config(
    page_title="FORMRAGE AI",
    page_icon=None,
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()

st.title("FORMRAGE AI")

st.subheader(
    "AI-Powered Exercise Form Analysis"
)

st.write(
    "Analyze exercise technique, detect repetitions, "
    "understand form problems and track improvement "
    "across workouts."
)

st.markdown("---")

st.header("Platform Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Form Analysis",
        "AI Powered"
    )

with c2:
    st.metric(
        "Rep Detection",
        "Continuous"
    )

with c3:
    st.metric(
        "Exercises",
        "10"
    )

st.markdown("---")

st.header("How the System Works")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.subheader("Upload")
    st.write(
        "Upload an exercise image or workout video."
    )

with c2:
    st.subheader("Track")
    st.write(
        "The system continuously tracks body landmarks "
        "throughout the workout."
    )

with c3:
    st.subheader("Detect")
    st.write(
        "Complete repetitions are identified from "
        "the movement pattern."
    )

with c4:
    st.subheader("Analyze")
    st.write(
        "AI evaluates form and provides specific "
        "recommendations."
    )

st.markdown("---")

st.header("Supported Exercises")

exercises = [
    "Squat",
    "Push-up",
    "Lunge",
    "Bicep Curl",
    "Shoulder Press",
    "Lateral Raise",
    "Front Raise",
    "Sit-up / Crunch",
    "Jumping Jack",
    "Plank"
]

columns = st.columns(5)

for index, exercise in enumerate(exercises):

    with columns[index % 5]:

        st.info(
            exercise
        )

st.markdown("---")

st.header("Feedback Modes")

c1, c2, c3 = st.columns(3)

with c1:

    st.subheader("Coach")

    st.write(
        "Professional feedback focused on improving "
        "exercise technique."
    )

with c2:

    st.subheader("Roast")

    st.write(
        "Humorous technique feedback with adjustable "
        "intensity."
    )

with c3:

    st.subheader("Teach")

    st.write(
        "Educational feedback explaining what happened, "
        "why it matters and how to correct it."
    )

st.markdown("---")

st.header("Start Your Analysis")

st.write(
    "Open Analyze from the navigation panel to "
    "upload your workout."
)

st.markdown(
    '<div class="footer">FORMRAGE AI provides educational fitness feedback and is not a medical diagnosis.</div>',
    unsafe_allow_html=True
)