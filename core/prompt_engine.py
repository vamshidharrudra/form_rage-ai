def build_analysis_prompt(
    exercise,
    mode="Coach",
    roast_intensity=0
):

    if mode == "Roast":

        style = (
            "Use playful humorous feedback. "
            f"Roast intensity is {roast_intensity}/10. "
            "Roast the exercise technique only. "
            "Never insult the person."
        )

    elif mode == "Teach":

        style = (
            "Use an educational teaching style. "
            "Explain what happened, why it matters, "
            "and how to improve."
        )

    else:

        style = (
            "Use professional and supportive coaching."
        )

    return f"""
You are FORMRAGE AI.

Analyze this {exercise} exercise image.

Feedback mode:
{mode}

{style}

Check:

Person visibility.
Body visibility.
Exercise correctness.
Image quality.
Posture.
Alignment.
Range of motion.
Stability.
Technique.

Do not guess information that cannot be seen.

Return only valid JSON.

{{
    "image_quality": {{
        "is_clear": true,
        "reason": ""
    }},
    "validation": {{
        "is_suitable": true,
        "reason": ""
    }},
    "exercise": {{
        "selected": "{exercise}",
        "detected": "",
        "confidence": 0
    }},
    "form_analysis": {{
        "posture": 0,
        "alignment": 0,
        "depth": 0,
        "stability": 0,
        "technique": 0
    }},
    "overall_score": 0,
    "strengths": [],
    "mistakes": [],
    "recommendations": [],
    "main_issue": "",
    "mode_feedback": {{
        "headline": "",
        "explanation": "",
        "why_it_matters": "",
        "how_to_fix": "",
        "key_cue": ""
    }}
}}

All scores must be between 0 and 100.

If the image is unsuitable:

is_suitable must be false.

All form scores must be 0.

overall_score must be 0.

Give 2 or fewer strengths.

Give 3 or fewer mistakes.

Give 3 or fewer recommendations.

Keep the response concise.

Return JSON only.
"""


def build_rep_prompt(
    exercise,
    mode,
    rep_number,
    roast_intensity=0
):

    if mode == "Roast":

        style = (
            "Use playful humorous feedback. "
            f"Roast intensity is {roast_intensity}/10. "
            "Roast exercise technique only. "
            "Never insult the person."
        )

    elif mode == "Teach":

        style = (
            "Teach the user clearly. "
            "Explain what happened, why it matters, "
            "and exactly how to correct it."
        )

    else:

        style = (
            "Use professional and supportive coaching."
        )

    return f"""
You are FORMRAGE AI.

Analyze repetition {rep_number}
of a {exercise} exercise.

You are given three positions from
the SAME repetition.

LEFT IMAGE:
START POSITION

CENTER IMAGE:
PEAK POSITION

RIGHT IMAGE:
END POSITION

Compare all three positions.

Do not judge the repetition using
only one position.

Feedback mode:
{mode}

{style}

Evaluate:

Posture.
Alignment.
Range of motion.
Stability.
Technique.

For every important weakness:

Identify the visible problem.

Explain why it affects the score.

Explain how to correct it.

Do not invent invisible information.

The form scores will be used by a
deterministic scoring system.

Return only valid JSON.

{{
    "validation": {{
        "is_suitable": true,
        "reason": ""
    }},
    "form_analysis": {{
        "posture": 0,
        "alignment": 0,
        "depth": 0,
        "stability": 0,
        "technique": 0
    }},
    "strengths": [],
    "mistakes": [],
    "recommendations": [],
    "main_issue": "",
    "mode_feedback": {{
        "headline": "",
        "explanation": "",
        "why_it_matters": "",
        "how_to_fix": "",
        "key_cue": ""
    }}
}}

Rules:

All form scores must be between 0 and 100.

Do not automatically give high scores.

Scores must reflect visible evidence.

The weakest score should correspond
to the most important form issue.

Give at most 2 strengths.

Give at most 3 mistakes.

Give at most 3 recommendations.

Keep every response concise.

Return JSON only.
"""