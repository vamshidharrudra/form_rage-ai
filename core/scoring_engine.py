import math


EXERCISE_WEIGHTS = {
    "Squat": {
        "posture": 0.20,
        "alignment": 0.25,
        "depth": 0.25,
        "stability": 0.15,
        "technique": 0.15
    },

    "Push-up": {
        "posture": 0.20,
        "alignment": 0.25,
        "depth": 0.20,
        "stability": 0.15,
        "technique": 0.20
    },

    "Lunge": {
        "posture": 0.20,
        "alignment": 0.25,
        "depth": 0.20,
        "stability": 0.20,
        "technique": 0.15
    },

    "Bicep Curl": {
        "posture": 0.10,
        "alignment": 0.20,
        "depth": 0.25,
        "stability": 0.20,
        "technique": 0.25
    },

    "Shoulder Press": {
        "posture": 0.15,
        "alignment": 0.25,
        "depth": 0.20,
        "stability": 0.20,
        "technique": 0.20
    },

    "Lateral Raise": {
        "posture": 0.15,
        "alignment": 0.25,
        "depth": 0.20,
        "stability": 0.20,
        "technique": 0.20
    },

    "Front Raise": {
        "posture": 0.15,
        "alignment": 0.25,
        "depth": 0.20,
        "stability": 0.20,
        "technique": 0.20
    },

    "Sit-up / Crunch": {
        "posture": 0.20,
        "alignment": 0.15,
        "depth": 0.25,
        "stability": 0.15,
        "technique": 0.25
    },

    "Jumping Jack": {
        "posture": 0.10,
        "alignment": 0.20,
        "depth": 0.20,
        "stability": 0.20,
        "technique": 0.20
    },

    "Plank": {
        "posture": 0.25,
        "alignment": 0.30,
        "depth": 0.05,
        "stability": 0.25,
        "technique": 0.15
    }
}


LABELS = {
    "posture": "Posture",
    "alignment": "Alignment",
    "depth": "Range of Motion",
    "stability": "Stability",
    "technique": "Technique"
}


def clamp(
    value
):

    try:

        value = float(
            value
        )

    except Exception:

        value = 0

    if not math.isfinite(
        value
    ):

        value = 0

    return max(
        0,
        min(
            100,
            value
        )
    )


def get_weights(
    exercise
):

    return EXERCISE_WEIGHTS.get(
        exercise,
        {
            "posture": 0.20,
            "alignment": 0.25,
            "depth": 0.20,
            "stability": 0.15,
            "technique": 0.20
        }
    )


def calculate_score_details(
    form_analysis,
    exercise
):

    if not isinstance(
        form_analysis,
        dict
    ):

        form_analysis = {}

    weights = get_weights(
        exercise
    )

    values = {}

    for key in LABELS:

        values[key] = clamp(
            form_analysis.get(
                key,
                0
            )
        )

    contributions = {}

    for key in LABELS:

        contributions[key] = round(
            values[key]
            *
            weights[key],
            2
        )

    score = round(
        sum(
            contributions.values()
        )
    )

    weakest_key = min(
        values,
        key=values.get
    )

    strongest_key = max(
        values,
        key=values.get
    )

    weakest_value = values[
        weakest_key
    ]

    strongest_value = values[
        strongest_key
    ]

    if weakest_value < 50:

        severity = "high"

    elif weakest_value < 70:

        severity = "medium"

    else:

        severity = "low"

    explanation = (
        f"{LABELS[weakest_key]} "
        f"is the weakest area at "
        f"{weakest_value:.0f}/100."
    )

    if strongest_value >= 80:

        strength_explanation = (
            f"{LABELS[strongest_key]} "
            f"is your strongest area at "
            f"{strongest_value:.0f}/100."
        )

    else:

        strength_explanation = (
            "No form category is currently "
            "above 80/100."
        )

    return {
        "score": score,
        "values": values,
        "weights": weights,
        "contributions": contributions,
        "weakest_area": weakest_key,
        "weakest_label": LABELS[weakest_key],
        "weakest_score": weakest_value,
        "strongest_area": strongest_key,
        "strongest_label": LABELS[strongest_key],
        "strongest_score": strongest_value,
        "severity": severity,
        "explanation": explanation,
        "strength_explanation": strength_explanation
    }


def calculate_score(
    form_analysis,
    exercise=None
):

    return calculate_score_details(
        form_analysis,
        exercise
    )[
        "score"
    ]


def score_label(
    score
):

    score = clamp(
        score
    )

    if score >= 90:

        return "Excellent"

    if score >= 75:

        return "Good"

    if score >= 60:

        return "Needs Improvement"

    return "Poor"


def aggregate_scores(
    scores
):

    clean_scores = []

    for score in scores:

        try:

            value = float(
                score
            )

        except Exception:

            continue

        if math.isfinite(
            value
        ):

            clean_scores.append(
                clamp(
                    value
                )
            )

    if not clean_scores:

        return {
            "valid": False,
            "average": 0,
            "best": 0,
            "worst": 0,
            "first": 0,
            "last": 0,
            "change": 0,
            "trend": "No valid scores."
        }

    average = round(
        sum(
            clean_scores
        )
        /
        len(
            clean_scores
        )
    )

    best = round(
        max(
            clean_scores
        )
    )

    worst = round(
        min(
            clean_scores
        )
    )

    first = round(
        clean_scores[0]
    )

    last = round(
        clean_scores[-1]
    )

    change = (
        last
        -
        first
    )

    if change >= 10:

        trend = (
            "Form improved during the workout."
        )

    elif change <= -10:

        trend = (
            "Form declined during the workout."
        )

    else:

        trend = (
            "Form remained relatively consistent."
        )

    return {
        "valid": True,
        "average": average,
        "best": best,
        "worst": worst,
        "first": first,
        "last": last,
        "change": change,
        "trend": trend
    }