import streamlit as st
import pandas as pd

from core.session_manager import (
    load_sessions,
    load_rep_history
)

st.set_page_config(
    page_title="Reports",
    page_icon=None,
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()

st.title("Workout Reports")

st.write(
    "Review and export your previous workout analyses."
)

sessions = load_sessions()
reps = load_rep_history()

if sessions.empty:

    st.info(
        "No workout reports are available yet."
    )

    st.stop()

sessions["score"] = pd.to_numeric(
    sessions["score"],
    errors="coerce"
).fillna(0)

sessions = sessions.sort_values(
    "timestamp",
    ascending=False
)

session_ids = sessions[
    "session_id"
].tolist()

selected_session = st.selectbox(
    "Select Workout",
    session_ids
)

session = sessions[
    sessions["session_id"]
    ==
    selected_session
].iloc[0]

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Exercise",
        session["exercise"]
    )

with c2:
    st.metric(
        "Score",
        f"{int(session['score'])}/100"
    )

with c3:
    st.metric(
        "Repetitions",
        int(session.get("reps", 0))
    )

with c4:
    st.metric(
        "Mode",
        session.get(
            "mode",
            "Coach"
        )
    )

st.markdown("---")

st.header(
    "Workout Summary"
)

main_issue = session.get(
    "main_issue",
    ""
)

if main_issue:

    st.subheader(
        "Main Issue"
    )

    st.warning(
        main_issue
    )

strengths = str(
    session.get(
        "strengths",
        ""
    )
)

mistakes = str(
    session.get(
        "mistakes",
        ""
    )
)

recommendations = str(
    session.get(
        "recommendations",
        ""
    )
)

c1, c2 = st.columns(2)

with c1:

    st.subheader(
        "Strengths"
    )

    for item in strengths.split(" | "):

        if item.strip():

            st.success(
                item
            )

with c2:

    st.subheader(
        "Mistakes"
    )

    for item in mistakes.split(" | "):

        if item.strip():

            st.error(
                item
            )

st.subheader(
    "Recommendations"
)

for item in recommendations.split(" | "):

    if item.strip():

        st.info(
            item
        )

if not reps.empty:

    session_reps = reps[
        reps["session_id"]
        ==
        selected_session
    ].copy()

    if not session_reps.empty:

        session_reps["score"] = pd.to_numeric(
            session_reps["score"],
            errors="coerce"
        ).fillna(0)

        st.markdown("---")

        st.header(
            "Rep Performance"
        )

        chart = session_reps[
            [
                "rep_number",
                "score"
            ]
        ].set_index(
            "rep_number"
        )

        st.line_chart(
            chart["score"]
        )

        st.subheader(
            "Rep Data"
        )

        display_columns = [
            "rep_number",
            "score",
            "posture",
            "alignment",
            "depth",
            "stability",
            "technique",
            "weakest_area",
            "strongest_area"
        ]

        display_columns = [
            column
            for column in display_columns
            if column in session_reps.columns
        ]

        st.dataframe(
            session_reps[
                display_columns
            ],
            hide_index=True,
            use_container_width=True
        )

st.markdown("---")

report_text = f"""
FORMRAGE AI WORKOUT REPORT

Exercise: {session["exercise"]}

Date: {session.get("timestamp", "")}

Mode: {session.get("mode", "")}

Score: {int(session["score"])}/100

Repetitions: {int(session.get("reps", 0))}

Main Issue:
{main_issue}

Strengths:
{strengths}

Mistakes:
{mistakes}

Recommendations:
{recommendations}
"""

st.download_button(
    "Download Report",
    report_text,
    file_name="formrage_workout_report.txt",
    mime="text/plain"
)