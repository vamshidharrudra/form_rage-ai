import json
import os
from datetime import datetime

import pandas as pd


SESSION_FILE = "data/session_history.csv"

REP_FILE = "data/rep_history.csv"

JSON_DIR = "data/analysis_runs"


def ensure_directories():

    os.makedirs(
        "data",
        exist_ok=True
    )

    os.makedirs(
        JSON_DIR,
        exist_ok=True
    )


def append_csv(
    file_path,
    row
):

    ensure_directories()

    new_data = pd.DataFrame(
        [row]
    )

    if not os.path.exists(
        file_path
    ):

        new_data.to_csv(
            file_path,
            index=False
        )

        return

    try:

        old_data = pd.read_csv(
            file_path
        )

    except Exception:

        old_data = pd.DataFrame()

    if old_data.empty:

        final_data = new_data

    else:

        final_data = pd.concat(
            [
                old_data,
                new_data
            ],
            ignore_index=True
        )

    final_data.to_csv(
        file_path,
        index=False
    )


def save_session(
    exercise,
    mode,
    input_type,
    score,
    result,
    reps=0
):

    ensure_directories()

    timestamp = datetime.now()

    session_id = timestamp.strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    session = {

        "session_id":
            session_id,

        "timestamp":
            timestamp.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "exercise":
            exercise,

        "mode":
            mode,

        "input_type":
            input_type,

        "score":
            int(
                score
            ),

        "reps":
            int(
                reps
            ),

        "main_issue":
            result.get(
                "main_issue",
                ""
            ),

        "strengths":
            " | ".join(
                result.get(
                    "strengths",
                    []
                )
            ),

        "mistakes":
            " | ".join(
                result.get(
                    "mistakes",
                    []
                )
            ),

        "recommendations":
            " | ".join(
                result.get(
                    "recommendations",
                    []
                )
            )
    }

    append_csv(
        SESSION_FILE,
        session
    )

    return session_id


def save_rep_results(
    session_id,
    exercise,
    mode,
    rep_results
):

    ensure_directories()

    saved_rows = []

    for result in rep_results:

        metadata = result.get(
            "_rep_metadata",
            {}
        )

        form = result.get(
            "form_analysis",
            {}
        )

        score_details = result.get(
            "_score_details",
            {}
        )

        feedback = result.get(
            "mode_feedback",
            {}
        )

        validation = result.get(
            "validation",
            {}
        )

        rep_number = result.get(
            "rep_number",
            metadata.get(
                "rep_number",
                0
            )
        )

        row = {

            "session_id":
                session_id,

            "timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "exercise":
                exercise,

            "mode":
                mode,

            "rep_number":
                rep_number,

            "score":
                int(
                    result.get(
                        "score",
                        0
                    )
                ),

            "score_label":
                result.get(
                    "_score_label",
                    ""
                ),

            "posture":
                form.get(
                    "posture",
                    0
                ),

            "alignment":
                form.get(
                    "alignment",
                    0
                ),

            "depth":
                form.get(
                    "depth",
                    0
                ),

            "stability":
                form.get(
                    "stability",
                    0
                ),

            "technique":
                form.get(
                    "technique",
                    0
                ),

            "weakest_area":
                score_details.get(
                    "weakest_label",
                    ""
                ),

            "weakest_score":
                score_details.get(
                    "weakest_score",
                    0
                ),

            "strongest_area":
                score_details.get(
                    "strongest_label",
                    ""
                ),

            "strongest_score":
                score_details.get(
                    "strongest_score",
                    0
                ),

            "score_explanation":
                score_details.get(
                    "explanation",
                    ""
                ),

            "start_time":
                metadata.get(
                    "start_time",
                    0
                ),

            "peak_time":
                metadata.get(
                    "peak_time",
                    0
                ),

            "end_time":
                metadata.get(
                    "end_time",
                    0
                ),

            "duration":
                metadata.get(
                    "duration",
                    0
                ),

            "amplitude":
                metadata.get(
                    "amplitude",
                    0
                ),

            "rep_confidence":
                metadata.get(
                    "confidence",
                    0
                ),

            "validation":
                validation.get(
                    "is_suitable",
                    False
                ),

            "validation_reason":
                validation.get(
                    "reason",
                    ""
                ),

            "main_issue":
                result.get(
                    "main_issue",
                    ""
                ),

            "strengths":
                " | ".join(
                    result.get(
                        "strengths",
                        []
                    )
                ),

            "mistakes":
                " | ".join(
                    result.get(
                        "mistakes",
                        []
                    )
                ),

            "recommendations":
                " | ".join(
                    result.get(
                        "recommendations",
                        []
                    )
                ),

            "feedback_headline":
                feedback.get(
                    "headline",
                    ""
                ),

            "feedback_explanation":
                feedback.get(
                    "explanation",
                    ""
                ),

            "why_it_matters":
                feedback.get(
                    "why_it_matters",
                    ""
                ),

            "how_to_fix":
                feedback.get(
                    "how_to_fix",
                    ""
                ),

            "key_cue":
                feedback.get(
                    "key_cue",
                    ""
                )
        }

        append_csv(
            REP_FILE,
            row
        )

        saved_rows.append(
            row
        )

    json_path = os.path.join(
        JSON_DIR,
        f"{session_id}.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "session_id":
                    session_id,

                "exercise":
                    exercise,

                "mode":
                    mode,

                "rep_results":
                    rep_results
            },
            file,
            indent=2,
            ensure_ascii=False,
            default=str
        )

    return saved_rows


def load_sessions():

    ensure_directories()

    if not os.path.exists(
        SESSION_FILE
    ):

        return pd.DataFrame()

    try:

        return pd.read_csv(
            SESSION_FILE
        )

    except Exception:

        return pd.DataFrame()


def load_rep_history():

    ensure_directories()

    if not os.path.exists(
        REP_FILE
    ):

        return pd.DataFrame()

    try:

        return pd.read_csv(
            REP_FILE
        )

    except Exception:

        return pd.DataFrame()