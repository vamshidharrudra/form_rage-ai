import os
import streamlit as st

st.set_page_config(
    page_title="Exercise Guide",
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()

EXERCISES = {
    "Squat": {
        "image": "squat.png",
        "starting": "Stand with your feet approximately shoulder width apart.",
        "movement": "Lower your hips while bending your knees and return to the standing position.",
        "checks": [
            "Posture",
            "Knee alignment",
            "Depth",
            "Stability",
            "Technique"
        ],
        "mistakes": [
            "Insufficient depth",
            "Knees moving inward",
            "Excessive forward lean",
            "Unstable foot position"
        ],
        "score": "A strong squat requires controlled depth, stable feet and consistent knee alignment."
    },

    "Push-up": {
        "image": "push_up.png",
        "starting": "Begin in a straight plank position with your hands below your shoulders.",
        "movement": "Lower your body while maintaining alignment and push back to the starting position.",
        "checks": [
            "Body alignment",
            "Elbow position",
            "Range of motion",
            "Stability",
            "Technique"
        ],
        "mistakes": [
            "Hips dropping",
            "Incomplete movement",
            "Poor elbow alignment",
            "Unstable body position"
        ],
        "score": "A strong push-up maintains a straight body and controlled movement throughout the repetition."
    },

    "Lunge": {
        "image": "lunge.png",
        "starting": "Stand upright with your feet positioned comfortably.",
        "movement": "Step forward, lower your body and return to the starting position.",
        "checks": [
            "Posture",
            "Knee alignment",
            "Depth",
            "Balance",
            "Stability"
        ],
        "mistakes": [
            "Knee misalignment",
            "Poor balance",
            "Insufficient depth",
            "Uncontrolled movement"
        ],
        "score": "A strong lunge requires stable alignment and controlled movement."
    },

    "Bicep Curl": {
        "image": "bicep_curl.png",
        "starting": "Stand upright with your arms positioned beside your body.",
        "movement": "Bend your elbows to raise your hands and return them under control.",
        "checks": [
            "Elbow position",
            "Range of motion",
            "Stability",
            "Posture",
            "Technique"
        ],
        "mistakes": [
            "Swinging the body",
            "Moving the elbows",
            "Incomplete range of motion",
            "Using excessive momentum"
        ],
        "score": "A strong curl keeps the upper body stable and uses controlled elbow movement."
    },

    "Shoulder Press": {
        "image": "shoulder_press.png",
        "starting": "Hold the weights near shoulder level with a stable upright posture.",
        "movement": "Press the arms upward and return them under control.",
        "checks": [
            "Posture",
            "Shoulder alignment",
            "Range of motion",
            "Stability",
            "Technique"
        ],
        "mistakes": [
            "Excessive back movement",
            "Uneven arm movement",
            "Incomplete range",
            "Poor stability"
        ],
        "score": "A strong shoulder press uses controlled movement with stable posture."
    },

    "Lateral Raise": {
        "image": "lateral_raise.png",
        "starting": "Stand upright with your arms beside your body.",
        "movement": "Raise your arms laterally and return them under control.",
        "checks": [
            "Posture",
            "Shoulder alignment",
            "Movement range",
            "Stability",
            "Technique"
        ],
        "mistakes": [
            "Shrugging",
            "Excessive momentum",
            "Uneven movement",
            "Poor posture"
        ],
        "score": "A strong lateral raise uses controlled arm movement without excessive momentum."
    },

    "Front Raise": {
        "image": "front_raise.png",
        "starting": "Stand upright with your arms beside your body.",
        "movement": "Raise your arms forward and return them under control.",
        "checks": [
            "Posture",
            "Shoulder alignment",
            "Range of motion",
            "Stability",
            "Technique"
        ],
        "mistakes": [
            "Excessive momentum",
            "Poor shoulder alignment",
            "Uneven movement",
            "Poor control"
        ],
        "score": "A strong front raise keeps the torso stable and controls the complete movement."
    },

    "Sit-up / Crunch": {
        "image": "situp_crunch.png",
        "starting": "Begin in a stable lying position.",
        "movement": "Raise your upper body through a controlled abdominal movement and return under control.",
        "checks": [
            "Posture",
            "Alignment",
            "Range of motion",
            "Stability",
            "Technique"
        ],
        "mistakes": [
            "Excessive momentum",
            "Incomplete movement",
            "Poor control",
            "Incorrect posture"
        ],
        "score": "A strong repetition uses controlled movement instead of momentum."
    },

    "Jumping Jack": {
        "image": "jumping_jack.png",
        "starting": "Stand upright with your feet together and arms beside your body.",
        "movement": "Jump while moving your arms and legs outward and return to the starting position.",
        "checks": [
            "Posture",
            "Coordination",
            "Stability",
            "Movement range",
            "Technique"
        ],
        "mistakes": [
            "Incomplete movement",
            "Poor coordination",
            "Unstable landing",
            "Inconsistent movement"
        ],
        "score": "A strong jumping jack maintains consistent coordination and controlled landings."
    },

    "Plank": {
        "image": "plank.png",
        "starting": "Maintain a straight body position supported by your arms and feet.",
        "movement": "Hold the position while maintaining stable alignment.",
        "checks": [
            "Posture",
            "Alignment",
            "Stability",
            "Body position",
            "Technique"
        ],
        "mistakes": [
            "Hips dropping",
            "Hips raised too high",
            "Poor alignment",
            "Loss of stability"
        ],
        "score": "A strong plank maintains a straight and stable body position."
    }
}

st.title("Exercise Guide")

st.write(
    "Learn the correct movement and understand what FORMRAGE AI evaluates."
)

st.markdown("---")

exercise_names = list(EXERCISES.keys())

for row_start in range(0, len(exercise_names), 3):

    columns = st.columns(3)

    row_exercises = exercise_names[
        row_start:row_start + 3
    ]

    for column, exercise in zip(
        columns,
        row_exercises
    ):

        data = EXERCISES[exercise]

        image_path = os.path.join(
            "assets",
            "exercises",
            data["image"]
        )

        with column:

            if os.path.exists(image_path):

                st.image(
                    image_path,
                    use_container_width=True
                )

            else:

                st.warning(
                    f"Image not found: {data['image']}"
                )

            st.subheader(exercise)

            st.write(data["score"])

            st.markdown("---")

st.header("Exercise Details")

selected_exercise = st.selectbox(
    "Select Exercise",
    exercise_names
)

data = EXERCISES[selected_exercise]

st.markdown("---")

image_path = os.path.join(
    "assets",
    "exercises",
    data["image"]
)

left, right = st.columns([1, 1])

with left:

    if os.path.exists(image_path):

        st.image(
            image_path,
            use_container_width=True
        )

    else:

        st.warning(
            f"Image not found: {data['image']}"
        )

with right:

    st.subheader("Starting Position")

    st.write(data["starting"])

    st.subheader("Correct Movement")

    st.write(data["movement"])

st.markdown("---")

st.subheader("What FORMRAGE AI Checks")

check_columns = st.columns(
    len(data["checks"])
)

for column, check in zip(
    check_columns,
    data["checks"]
):

    with column:

        st.write(check)

st.markdown("---")

st.subheader("Common Technique Problems")

for mistake in data["mistakes"]:

    st.write(mistake)

st.markdown("---")

st.subheader("How to Get a Strong Score")

st.write(data["score"])