import streamlit as st
import pandas as pd

from core.session_manager import (
    load_rep_history
)

st.set_page_config(
    page_title="Rep Analysis",
    page_icon=None,
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()

st.title("Rep Analysis")

st.write(
    "Review the performance of individual repetitions."
)

reps = load_rep_history()

if reps.empty:

    st.info(
        "No repetition analysis is available yet."
    )

    st.write(
        "Analyze a workout from the Analyze page first."
    )

    st.stop()

reps["score"] = pd.to_numeric(
    reps["score"],
    errors="coerce"
).fillna(0)

sessions = reps[
    "session_id"
].dropna().unique().tolist()

selected_session = st.selectbox(
    "Select Workout",
    sessions
)

session_reps = reps[
    reps["session_id"]
    ==
    selected_session
].copy()

session_reps = session_reps.sort_values(
    "rep_number"
)

if session_reps.empty:

    st.warning(
        "No repetitions were found for this workout."
    )

    st.stop()

exercise = session_reps.iloc[0].get(
    "exercise",
    "Unknown"
)

average_score = round(
    session_reps["score"].mean()
)

best_score = round(
    session_reps["score"].max()
)

lowest_score = round(
    session_reps["score"].min()
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Exercise",
        exercise
    )

with c2:
    st.metric(
        "Complete Reps",
        len(session_reps)
    )

with c3:
    st.metric(
        "Average Score",
        f"{average_score}/100"
    )

with c4:
    st.metric(
        "Lowest Score",
        f"{lowest_score}/100"
    )

st.markdown("---")

st.header("Rep Performance")

chart = session_reps[
    [
        "rep_number",
        "score"
    ]
].copy()

chart = chart.set_index(
    "rep_number"
)

st.line_chart(
    chart["score"]
)

st.markdown("---")

st.header("Repetition Details")

rep_numbers = session_reps[
    "rep_number"
].tolist()

selected_rep = st.selectbox(
    "Select Repetition",
    rep_numbers
)

rep = session_reps[
    session_reps["rep_number"]
    ==
    selected_rep
].iloc[0]

st.subheader(
    f"Repetition {selected_rep}"
)

st.metric(
    "Score",
    f"{int(rep['score'])}/100"
)

c1, c2, c3, c4, c5 = st.columns(5)

for column, label in [
    (c1, "Posture"),
    (c2, "Alignment"),
    (c3, "Range of Motion"),
    (c4, "Stability"),
    (c5, "Technique")
]:

    key = {
        "Posture": "posture",
        "Alignment": "alignment",
        "Range of Motion": "depth",
        "Stability": "stability",
        "Technique": "technique"
    }[label]

    value = pd.to_numeric(
        rep.get(
            key,
            0
        ),
        errors="coerce"
    )

    if pd.isna(value):
        value = 0

    column.metric(
        label,
        f"{int(value)}/100"
    )

st.markdown("---")

weakest = rep.get(
    "weakest_area",
    ""
)

strongest = rep.get(
    "strongest_area",
    ""

)

explanation = rep.get(
    "score_explanation",
    ""
)

if weakest:

    st.subheader(
        "Main Area to Improve"
    )

    st.warning(
        weakest
    )

if strongest:

    st.subheader(
        "Strongest Area"
    )

    st.success(
        strongest
    )

if explanation:

    st.subheader(
        "Why This Rep Received This Score"
    )

    st.write(
        explanation
    )

mistakes = str(
    rep.get(
        "mistakes",
        ""
    )
)

recommendations = str(
    rep.get(
        "recommendations",
        ""
    )
)

strengths = str(
    rep.get(
        "strengths",
        ""
    )
)

if strengths:

    st.subheader(
        "What You Did Well"
    )

    for item in strengths.split(" | "):

        if item.strip():

            st.success(
                item
            )

if mistakes:

    st.subheader(
        "What Needs Improvement"
    )

    for item in mistakes.split(" | "):

        if item.strip():

            st.error(
                item
            )

if recommendations:

    st.subheader(
        "How to Improve"
    )

    for item in recommendations.split(" | "):

        if item.strip():

            st.info(
                item
            )

st.markdown("---")

st.subheader(
    "Rep Timing"
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Start",
        f"{float(rep.get('start_time', 0)):.2f}s"
    )

with c2:
    st.metric(
        "Peak",
        f"{float(rep.get('peak_time', 0)):.2f}s"
    )

with c3:
    st.metric(
        "End",
        f"{float(rep.get('end_time', 0)):.2f}s"
    )