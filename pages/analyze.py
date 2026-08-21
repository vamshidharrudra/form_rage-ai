from io import BytesIO

import pandas as pd
import streamlit as st
from PIL import Image

from core.groq_engine import (
    analyze_image,
    analyze_rep_frames
)

from core.prompt_engine import (
    build_analysis_prompt,
    build_rep_prompt
)

from core.movement_engine import (
    track_video_movement
)

from core.scoring_engine import (
    calculate_score_details,
    score_label,
    aggregate_scores
)

from core.session_manager import (
    save_session,
    save_rep_results
)

from utils.rep_detector import (
    detect_repetitions
)

from utils.video_utils import (
    validate_video,
    extract_frames_by_indices,
    frame_to_jpeg
)


st.set_page_config(
    page_title="FORMRAGE AI",
    page_icon="FORM",
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()


EXERCISES = [
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


def validate_image(
    image_bytes,
    max_mb=20
):

    if not image_bytes:

        return (
            False,
            "No image uploaded."
        )

    size_mb = (
        len(image_bytes)
        /
        (1024 * 1024)
    )

    if size_mb > max_mb:

        return (
            False,
            f"Image exceeds {max_mb} MB."
        )

    try:

        Image.open(
            BytesIO(
                image_bytes
            )
        ).verify()

    except Exception:

        return (
            False,
            "The uploaded file is not a valid image."
        )

    return (
        True,
        "Image is valid."
    )


def render_form_breakdown(
    form
):

    if not isinstance(
        form,
        dict
    ):

        form = {}

    values = [
        (
            "Posture",
            "posture"
        ),
        (
            "Alignment",
            "alignment"
        ),
        (
            "Range of Motion",
            "depth"
        ),
        (
            "Stability",
            "stability"
        ),
        (
            "Technique",
            "technique"
        )
    ]

    columns = st.columns(
        5
    )

    for column, item in zip(
        columns,
        values
    ):

        with column:

            try:

                value = int(
                    float(
                        form.get(
                            item[1],
                            0
                        )
                    )
                )

            except Exception:

                value = 0

            st.metric(
                item[0],
                f"{value}/100"
            )


def display_score_explanation(
    result
):

    details = result.get(
        "_score_details",
        {}
    )

    if not details:

        return

    st.subheader(
        "Why This Score?"
    )

    columns = st.columns(
        3
    )

    with columns[0]:

        st.metric(
            "Overall",
            f"{details.get('score', 0)}/100"
        )

    with columns[1]:

        st.metric(
            "Strongest Area",
            details.get(
                "strongest_label",
                "N/A"
            ),
            f"{details.get('strongest_score', 0):.0f}/100"
        )

    with columns[2]:

        st.metric(
            "Needs Most Improvement",
            details.get(
                "weakest_label",
                "N/A"
            ),
            f"{details.get('weakest_score', 0):.0f}/100"
        )

    st.info(
        details.get(
            "explanation",
            ""
        )
    )

    values = details.get(
        "values",
        {}
    )

    contributions = details.get(
        "contributions",
        {}
    )

    weights = details.get(
        "weights",
        {}
    )

    table = pd.DataFrame(
        {
            "Area": [
                "Posture",
                "Alignment",
                "Range of Motion",
                "Stability",
                "Technique"
            ],
            "Score": [
                values.get(
                    "posture",
                    0
                ),
                values.get(
                    "alignment",
                    0
                ),
                values.get(
                    "depth",
                    0
                ),
                values.get(
                    "stability",
                    0
                ),
                values.get(
                    "technique",
                    0
                )
            ],
            "Weight": [
                weights.get(
                    "posture",
                    0
                ),
                weights.get(
                    "alignment",
                    0
                ),
                weights.get(
                    "depth",
                    0
                ),
                weights.get(
                    "stability",
                    0
                ),
                weights.get(
                    "technique",
                    0
                )
            ],
            "Contribution": [
                contributions.get(
                    "posture",
                    0
                ),
                contributions.get(
                    "alignment",
                    0
                ),
                contributions.get(
                    "depth",
                    0
                ),
                contributions.get(
                    "stability",
                    0
                ),
                contributions.get(
                    "technique",
                    0
                )
            ]
        }
    )

    table["Weight"] = (
        table["Weight"]
        *
        100
    ).round(
        0
    ).astype(
        int
    ).astype(
        str
    ) + "%"

    table["Score"] = (
        table["Score"]
        .round(
            0
        )
        .astype(
            int
        )
    )

    table["Contribution"] = (
        table["Contribution"]
        .round(
            1
        )
    )

    st.dataframe(
        table,
        hide_index=True,
        use_container_width=True
    )


def display_mode_feedback(
    result,
    mode
):

    feedback = result.get(
        "mode_feedback",
        {}
    )

    if not isinstance(
        feedback,
        dict
    ):

        feedback = {}

    if mode == "Roast":

        st.subheader(
            "Roast Feedback"
        )

    elif mode == "Teach":

        st.subheader(
            "Teaching Feedback"
        )

    else:

        st.subheader(
            "Coach Feedback"
        )

    if feedback.get(
        "headline"
    ):

        st.markdown(
            f"**{feedback['headline']}**"
        )

    if feedback.get(
        "explanation"
    ):

        st.write(
            feedback["explanation"]
        )

    if mode == "Teach":

        if feedback.get(
            "why_it_matters"
        ):

            st.info(
                "Why it matters: "
                + feedback[
                    "why_it_matters"
                ]
            )

        if feedback.get(
            "how_to_fix"
        ):

            st.success(
                "How to fix: "
                + feedback[
                    "how_to_fix"
                ]
            )

        if feedback.get(
            "key_cue"
        ):

            st.warning(
                "Key cue: "
                + feedback[
                    "key_cue"
                ]
            )


def display_common_feedback(
    result
):

    main_issue = result.get(
        "main_issue",
        ""
    )

    strengths = result.get(
        "strengths",
        []
    )

    mistakes = result.get(
        "mistakes",
        []
    )

    recommendations = result.get(
        "recommendations",
        []
    )

    if main_issue:

        st.warning(
            "Main issue: "
            + str(
                main_issue
            )
        )

    left, right = st.columns(
        2
    )

    with left:

        st.markdown(
            "### What You Did Well"
        )

        if strengths:

            for item in strengths:

                st.success(
                    str(item)
                )

        else:

            st.write(
                "No specific strengths returned."
            )

    with right:

        st.markdown(
            "### Needs Improvement"
        )

        if mistakes:

            for item in mistakes:

                st.error(
                    str(item)
                )

        else:

            st.success(
                "No major form issue detected."
            )

    st.markdown(
        "### How To Improve"
    )

    if recommendations:

        for item in recommendations:

            st.info(
                str(item)
            )

    else:

        st.write(
            "No recommendations returned."
        )


def analyze_single_image(
    image_bytes,
    exercise,
    mode,
    roast_intensity
):

    prompt = build_analysis_prompt(
        exercise,
        mode,
        roast_intensity
    )

    result = analyze_image(
        image_bytes,
        prompt
    )

    validation = result.get(
        "validation",
        {}
    )

    if not validation.get(
        "is_suitable",
        False
    ):

        return (
            result,
            None
        )

    form = result.get(
        "form_analysis",
        {}
    )

    details = calculate_score_details(
        form,
        exercise
    )

    result[
        "_score_details"
    ] = details

    result[
        "_score_label"
    ] = score_label(
        details["score"]
    )

    result[
        "score"
    ] = details[
        "score"
    ]

    return (
        result,
        details[
            "score"
        ]
    )


def run_video_analysis(
    video_bytes,
    file_name,
    exercise,
    mode,
    roast_intensity
):

    st.write(
        "### Phase 1 — Continuous pose tracking"
    )

    progress = st.progress(
        0
    )

    status = st.empty()

    def callback(
        value,
        message
    ):

        progress.progress(
            max(
                0.0,
                min(
                    1.0,
                    float(value)
                )
            )
        )

        status.write(
            message
        )

    tracking = track_video_movement(
        video_bytes,
        file_name,
        exercise,
        progress_callback=callback,
        target_fps=15.0
    )

    progress.empty()

    status.empty()

    if exercise == "Plank":

        return {
            "type": "plank",
            "tracking": tracking,
            "reps": [],
            "rep_results": []
        }

    st.write(
        "### Phase 2 — Detecting complete repetitions"
    )

    reps = detect_repetitions(
        tracking[
            "records"
        ],
        exercise
    )

    if not reps:

        return {
            "type": "reps",
            "tracking": tracking,
            "reps": [],
            "rep_results": []
        }

    st.success(
        f"Detected {len(reps)} complete repetitions."
    )

    frame_indices = []

    for rep in reps:

        frame_indices.extend(
            [
                rep.start_frame,
                rep.peak_frame,
                rep.end_frame
            ]
        )

    st.write(
        "### Phase 3 — Extracting exact rep frames"
    )

    selected_frames = extract_frames_by_indices(
        video_bytes,
        file_name,
        frame_indices
    )

    st.write(
        "### Phase 4 — AI analysis of each repetition"
    )

    rep_results = []

    total = len(
        reps
    )

    rep_progress = st.progress(
        0
    )

    for index, rep in enumerate(
        reps
    ):

        frame_bytes = []

        frame_indices_for_rep = [
            rep.start_frame,
            rep.peak_frame,
            rep.end_frame
        ]

        for frame_index in frame_indices_for_rep:

            frame = selected_frames.get(
                frame_index
            )

            if frame is not None:

                frame_bytes.append(
                    frame_to_jpeg(
                        frame,
                        quality=40
                    )
                )

        rep_number = getattr(
            rep,
            "rep_number",
            index + 1
        )

        if not frame_bytes:

            result = {
                "rep_number": rep_number,
                "score": 0,
                "validation": {
                    "is_suitable": False,
                    "reason":
                        "Exact frames could not be extracted."
                },
                "_rep_metadata":
                    rep.to_dict(),
                "form_analysis": {},
                "strengths": [],
                "mistakes": [],
                "recommendations": [],
                "main_issue": "",
                "mode_feedback": {}
            }

            rep_results.append(
                result
            )

            rep_progress.progress(
                (index + 1)
                /
                total
            )

            continue

        prompt = build_rep_prompt(
            exercise,
            mode,
            rep_number,
            roast_intensity
        )

        try:

            st.write(
                f"Analyzing repetition "
                f"{rep_number} of {total}"
            )

            result = analyze_rep_frames(
                frame_bytes,
                prompt
            )

            if not isinstance(
                result,
                dict
            ):

                raise ValueError(
                    "AI returned invalid JSON."
                )

            result[
                "rep_number"
            ] = rep_number

            result[
                "_rep_metadata"
            ] = rep.to_dict()

            form = result.get(
                "form_analysis",
                {}
            )

            details = calculate_score_details(
                form,
                exercise
            )

            result[
                "_score_details"
            ] = details

            result[
                "_score_label"
            ] = score_label(
                details[
                    "score"
                ]
            )

            result[
                "score"
            ] = details[
                "score"
            ]

            validation = result.get(
                "validation",
                {}
            )

            if not isinstance(
                validation,
                dict
            ):

                validation = {}

            result[
                "validation"
            ] = validation

            rep_results.append(
                result
            )

            st.success(
                f"Rep {rep_number}: "
                f"{details['score']}/100"
            )

        except Exception as error:

            result = {
                "rep_number": rep_number,
                "score": 0,
                "validation": {
                    "is_suitable": False,
                    "reason": str(error)
                },
                "_rep_metadata":
                    rep.to_dict(),
                "form_analysis": {},
                "strengths": [],
                "mistakes": [],
                "recommendations": [],
                "main_issue": "",
                "mode_feedback": {}
            }

            rep_results.append(
                result
            )

            st.error(
                f"Rep {rep_number} AI analysis failed: "
                f"{error}"
            )

        rep_progress.progress(
            (index + 1)
            /
            total
        )

    rep_progress.empty()

    return {
        "type": "reps",
        "tracking": tracking,
        "reps": reps,
        "rep_results": rep_results
    }


st.title(
    "FORMRAGE AI"
)

st.caption(
    "AI-powered exercise form analysis and repetition tracking."
)


st.sidebar.header(
    "Analysis Settings"
)


exercise = st.sidebar.selectbox(
    "Select Exercise",
    EXERCISES
)


mode = st.sidebar.selectbox(
    "Feedback Mode",
    [
        "Coach",
        "Roast",
        "Teach"
    ]
)


if mode == "Roast":

    roast_intensity = st.sidebar.slider(
        "Roast Intensity",
        1,
        10,
        5
    )

else:

    roast_intensity = 0


st.sidebar.caption(
    "Video analysis processes the complete movement "
    "and uses exact frames from detected repetitions."
)


st.header(
    "1. Choose Your Input"
)


input_type = st.radio(
    "Input",
    [
        "Image",
        "Video"
    ],
    horizontal=True
)


if input_type == "Image":

    uploaded = st.file_uploader(
        "Upload Workout Image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ]
    )

    if uploaded:

        image_bytes = uploaded.getvalue()

        image = Image.open(
            BytesIO(
                image_bytes
            )
        )

        st.image(
            image,
            use_container_width=True
        )

        if st.button(
            "ANALYZE WORKOUT",
            type="primary",
            use_container_width=True
        ):

            valid, message = validate_image(
                image_bytes
            )

            if not valid:

                st.error(
                    message
                )

                st.stop()

            try:

                with st.spinner(
                    "FORMRAGE AI is analyzing your form..."
                ):

                    result, score = analyze_single_image(
                        image_bytes,
                        exercise,
                        mode,
                        roast_intensity
                    )

                validation = result.get(
                    "validation",
                    {}
                )

                if not validation.get(
                    "is_suitable",
                    False
                ):

                    st.error(
                        "Image is not suitable for this exercise."
                    )

                    st.warning(
                        validation.get(
                            "reason",
                            "Please upload a clearer image."
                        )
                    )

                    st.stop()

                session_id = save_session(
                    exercise,
                    mode,
                    "Image",
                    score,
                    result,
                    reps=0
                )

                st.markdown(
                    "---"
                )

                st.header(
                    "2. Form Analysis"
                )

                columns = st.columns(
                    3
                )

                with columns[0]:

                    st.metric(
                        "FORM SCORE",
                        f"{score}/100"
                    )

                with columns[1]:

                    st.metric(
                        "ASSESSMENT",
                        score_label(
                            score
                        )
                    )

                with columns[2]:

                    confidence = result.get(
                        "exercise",
                        {}
                    ).get(
                        "confidence",
                        0
                    )

                    st.metric(
                        "CONFIDENCE",
                        f"{confidence}%"
                    )

                st.progress(
                    score
                    /
                    100
                )

                render_form_breakdown(
                    result.get(
                        "form_analysis",
                        {}
                    )
                )

                display_score_explanation(
                    result
                )

                display_mode_feedback(
                    result,
                    mode
                )

                display_common_feedback(
                    result
                )

                with st.expander(
                    "View Saved Analysis"
                ):

                    st.json(
                        result
                    )

                st.success(
                    f"Session saved: {session_id}"
                )

            except Exception as error:

                st.error(
                    "Image analysis failed."
                )

                st.exception(
                    error
                )


else:

    uploaded = st.file_uploader(
        "Upload Workout Video",
        type=[
            "mp4",
            "mov",
            "avi",
            "mkv",
            "webm"
        ]
    )

    if uploaded:

        video_bytes = uploaded.getvalue()

        file_name = uploaded.name

        valid, message, info = validate_video(
            video_bytes,
            file_name
        )

        if not valid:

            st.error(
                message
            )

            st.stop()

        st.video(
            video_bytes
        )

        columns = st.columns(
            4
        )

        with columns[0]:

            st.metric(
                "Exercise",
                exercise
            )

        with columns[1]:

            st.metric(
                "Duration",
                f"{info['duration']:.1f}s"
            )

        with columns[2]:

            st.metric(
                "FPS",
                f"{info['fps']:.1f}"
            )

        with columns[3]:

            st.metric(
                "Mode",
                mode
            )

        if mode == "Roast":

            st.caption(
                f"Roast intensity: {roast_intensity}/10"
            )

        st.info(
            "The complete video is tracked continuously. "
            "The AI analyzes the exact start, peak and end "
            "frames belonging to each detected repetition."
        )

        if st.button(
            "ANALYZE WORKOUT",
            type="primary",
            use_container_width=True
        ):

            try:

                result = run_video_analysis(
                    video_bytes,
                    file_name,
                    exercise,
                    mode,
                    roast_intensity
                )

                if result[
                    "type"
                ] == "plank":

                    st.header(
                        "2. Plank Analysis"
                    )

                    st.info(
                        "Plank is treated as a hold exercise."
                    )

                    st.metric(
                        "Tracked Frames",
                        len(
                            result[
                                "tracking"
                            ][
                                "records"
                            ]
                        )
                    )

                    st.stop()

                reps = result[
                    "reps"
                ]

                rep_results = result[
                    "rep_results"
                ]

                if not reps:

                    st.error(
                        "No complete repetitions were detected."
                    )

                    st.stop()

                valid_results = []

                for item in rep_results:

                    validation = item.get(
                        "validation",
                        {}
                    )

                    if validation.get(
                        "is_suitable",
                        True
                    ):

                        if item.get(
                            "score",
                            0
                        ) > 0:

                            valid_results.append(
                                item
                            )

                if not valid_results:

                    st.error(
                        "Repetitions were detected, "
                        "but none could be scored."
                    )

                    st.stop()

                scores = [
                    int(
                        item[
                            "score"
                        ]
                    )
                    for item in valid_results
                ]

                summary = aggregate_scores(
                    scores
                )

                all_strengths = []

                all_mistakes = []

                all_recommendations = []

                issues = []

                for item in valid_results:

                    all_strengths.extend(
                        item.get(
                            "strengths",
                            []
                        )
                    )

                    all_mistakes.extend(
                        item.get(
                            "mistakes",
                            []
                        )
                    )

                    all_recommendations.extend(
                        item.get(
                            "recommendations",
                            []
                        )
                    )

                    if item.get(
                        "main_issue",
                        ""
                    ):

                        issues.append(
                            item[
                                "main_issue"
                            ]
                        )

                def unique_limit(
                    values,
                    limit=6
                ):

                    output = []

                    for value in values:

                        if value and value not in output:

                            output.append(
                                value
                            )

                    return output[
                        :limit
                    ]

                workout_summary = {

                    "main_issue":
                        issues[-1]
                        if issues
                        else "",

                    "strengths":
                        unique_limit(
                            all_strengths
                        ),

                    "mistakes":
                        unique_limit(
                            all_mistakes
                        ),

                    "recommendations":
                        unique_limit(
                            all_recommendations
                        )
                }

                session_id = save_session(
                    exercise,
                    mode,
                    "Video",
                    summary[
                        "average"
                    ],
                    workout_summary,
                    reps=len(
                        valid_results
                    )
                )

                save_rep_results(
                    session_id,
                    exercise,
                    mode,
                    rep_results
                )

                st.markdown(
                    "---"
                )

                st.header(
                    "2. Workout Result"
                )

                columns = st.columns(
                    5
                )

                with columns[0]:

                    st.metric(
                        "FORM SCORE",
                        f"{summary['average']}/100"
                    )

                with columns[1]:

                    st.metric(
                        "COMPLETE REPS",
                        len(
                            reps
                        )
                    )

                with columns[2]:

                    st.metric(
                        "BEST REP",
                        summary[
                            "best"
                        ]
                    )

                with columns[3]:

                    st.metric(
                        "LOWEST REP",
                        summary[
                            "worst"
                        ]
                    )

                with columns[4]:

                    st.metric(
                        "FORM CHANGE",
                        f"{summary['change']:+}"
                    )

                st.progress(
                    summary[
                        "average"
                    ]
                    /
                    100
                )

                st.info(
                    summary[
                        "trend"
                    ]
                )

                st.subheader(
                    "Rep Performance"
                )

                chart_data = pd.DataFrame(
                    {
                        "Rep": [
                            item.get(
                                "rep_number",
                                index + 1
                            )
                            for index, item
                            in enumerate(
                                valid_results
                            )
                        ],
                        "Score": scores
                    }
                )

                st.line_chart(
                    chart_data.set_index(
                        "Rep"
                    )
                )

                st.subheader(
                    "Repetition Details"
                )

                for index, item in enumerate(
                    valid_results
                ):

                    metadata = item.get(
                        "_rep_metadata",
                        {}
                    )

                    rep_number = item.get(
                        "rep_number",
                        index + 1
                    )

                    score = int(
                        item.get(
                            "score",
                            0
                        )
                    )

                    with st.expander(
                        f"Rep {rep_number} | {score}/100 | "
                        f"{score_label(score)}"
                    ):

                        columns = st.columns(
                            4
                        )

                        with columns[0]:

                            st.metric(
                                "Score",
                                f"{score}/100"
                            )

                        with columns[1]:

                            st.metric(
                                "Start",
                                f"{float(metadata.get('start_time', 0)):.2f}s"
                            )

                        with columns[2]:

                            st.metric(
                                "Peak",
                                f"{float(metadata.get('peak_time', 0)):.2f}s"
                            )

                        with columns[3]:

                            st.metric(
                                "End",
                                f"{float(metadata.get('end_time', 0)):.2f}s"
                            )

                        st.write(
                            f"Rep duration: "
                            f"{float(metadata.get('duration', 0)):.2f}s"
                        )

                        st.write(
                            f"Movement amplitude: "
                            f"{float(metadata.get('amplitude', 0)):.3f}"
                        )

                        st.markdown(
                            "---"
                        )

                        render_form_breakdown(
                            item.get(
                                "form_analysis",
                                {}
                            )
                        )

                        display_score_explanation(
                            item
                        )

                        display_mode_feedback(
                            item,
                            mode
                        )

                        display_common_feedback(
                            item
                        )

                st.markdown(
                    "---"
                )

                st.header(
                    "3. Workout Summary"
                )

                display_common_feedback(
                    workout_summary
                )

                st.success(
                    f"Complete workout saved successfully. "
                    f"Session ID: {session_id}"
                )

                with st.expander(
                    "View Complete Rep Data"
                ):

                    st.json(
                        rep_results
                    )

            except Exception as error:

                st.error(
                    "Video analysis failed."
                )

                st.exception(
                    error
                )


st.markdown(
    "---"
)

st.caption(
    "FORMRAGE AI provides educational fitness feedback."
)