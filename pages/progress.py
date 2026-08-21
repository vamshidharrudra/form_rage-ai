import streamlit as st
import pandas as pd

from core.session_manager import load_sessions

st.set_page_config(
    page_title="Progress",
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()

st.title("Progress")

st.write(
    "Track your exercise performance across previous workouts."
)

sessions = load_sessions()

if sessions.empty:
    st.info(
        "No workout history is available yet."
    )

    st.write(
        "Complete a workout from the Analyze page "
        "to start tracking your progress."
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

sessions["timestamp"] = pd.to_datetime(
    sessions["timestamp"],
    errors="coerce"
)

sessions = sessions.dropna(
    subset=["timestamp"]
)

sessions = sessions.sort_values(
    "timestamp"
)

starting_score = int(
    sessions.iloc[0]["score"]
)

latest_score = int(
    sessions.iloc[-1]["score"]
)

best_score = int(
    sessions["score"].max()
)

average_score = int(
    sessions["score"].mean()
)

improvement = (
    latest_score
    - starting_score
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Starting Score",
        f"{starting_score}/100"
    )

with c2:
    st.metric(
        "Latest Score",
        f"{latest_score}/100"
    )

with c3:
    st.metric(
        "Average Score",
        f"{average_score}/100"
    )

with c4:
    st.metric(
        "Improvement",
        f"{improvement:+d}"
    )

st.markdown("---")

st.header(
    "Form Score Over Time"
)

score_chart = sessions[
    [
        "timestamp",
        "score"
    ]
].copy()

score_chart = score_chart.set_index(
    "timestamp"
)

st.line_chart(
    score_chart["score"]
)

st.markdown("---")

st.header(
    "Exercise Performance"
)

exercise_scores = (
    sessions
    .groupby("exercise")["score"]
    .mean()
    .round()
    .sort_values(
        ascending=False
    )
)

if not exercise_scores.empty:

    st.bar_chart(
        exercise_scores
    )

st.markdown("---")

st.header(
    "Repetition Performance"
)

rep_chart = sessions[
    [
        "timestamp",
        "reps"
    ]
].copy()

rep_chart = rep_chart.set_index(
    "timestamp"
)

st.line_chart(
    rep_chart["reps"]
)

st.markdown("---")

st.header(
    "Workout History"
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
    if column in sessions.columns
]

st.dataframe(
    sessions[
        display_columns
    ].sort_values(
        "timestamp",
        ascending=False
    ),
    hide_index=True,
    use_container_width=True
)