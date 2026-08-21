import streamlit as st
import pandas as pd

from core.session_manager import load_sessions

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()

st.title("Dashboard")

st.write(
    "Overview of your FORMRAGE AI workout performance."
)

sessions = load_sessions()

if sessions.empty:

    st.info(
        "No workout data is available yet."
    )

    st.write(
        "Analyze a workout to populate your dashboard."
    )

    st.stop()

sessions["score"] = pd.to_numeric(
    sessions["score"],
    errors="coerce"
).fillna(0)

sessions["reps"] = pd.to_numeric(
    sessions["reps"],
    errors="coerce"
).fillna(0)

total_workouts = len(
    sessions
)

total_reps = int(
    sessions["reps"].sum()
)

average_score = int(
    sessions["score"].mean()
)

best_score = int(
    sessions["score"].max()
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Workouts",
        total_workouts
    )

with c2:
    st.metric(
        "Total Repetitions",
        total_reps
    )

with c3:
    st.metric(
        "Average Score",
        f"{average_score}/100"
    )

with c4:
    st.metric(
        "Best Score",
        f"{best_score}/100"
    )

st.markdown("---")

st.header(
    "Workout Score"
)

sessions["timestamp"] = pd.to_datetime(
    sessions["timestamp"],
    errors="coerce"
)

score_data = sessions[
    [
        "timestamp",
        "score"
    ]
].dropna()

score_data = score_data.sort_values(
    "timestamp"
)

score_data = score_data.set_index(
    "timestamp"
)

st.line_chart(
    score_data["score"]
)

st.markdown("---")

st.header(
    "Performance By Exercise"
)

exercise_scores = (
    sessions
    .groupby("exercise")["score"]
    .mean()
    .round()
)

st.bar_chart(
    exercise_scores
)

st.markdown("---")

st.header(
    "Recent Workouts"
)

recent = sessions.sort_values(
    "timestamp",
    ascending=False
)

display_columns = [
    "timestamp",
    "exercise",
    "mode",
    "input_type",
    "score",
    "reps"
]

display_columns = [
    column
    for column in display_columns
    if column in recent.columns
]

st.dataframe(
    recent[
        display_columns
    ].head(10),
    hide_index=True,
    use_container_width=True
)