import os
import tempfile

import cv2

from utils.pose_utils import (
    create_pose_detector,
    process_video_frame,
    close_pose_detector,
    LANDMARKS,
    get_joint_angle,
    get_average_angle
)


def calculate_squat_signal(landmarks):

    return get_average_angle(
        landmarks,
        (
            LANDMARKS["left_hip"],
            LANDMARKS["left_knee"],
            LANDMARKS["left_ankle"]
        ),
        (
            LANDMARKS["right_hip"],
            LANDMARKS["right_knee"],
            LANDMARKS["right_ankle"]
        )
    )


def calculate_pushup_signal(landmarks):

    return get_average_angle(
        landmarks,
        (
            LANDMARKS["left_shoulder"],
            LANDMARKS["left_elbow"],
            LANDMARKS["left_wrist"]
        ),
        (
            LANDMARKS["right_shoulder"],
            LANDMARKS["right_elbow"],
            LANDMARKS["right_wrist"]
        )
    )


def calculate_lunge_signal(landmarks):

    left = get_joint_angle(
        landmarks,
        LANDMARKS["left_hip"],
        LANDMARKS["left_knee"],
        LANDMARKS["left_ankle"]
    )

    right = get_joint_angle(
        landmarks,
        LANDMARKS["right_hip"],
        LANDMARKS["right_knee"],
        LANDMARKS["right_ankle"]
    )

    values = [
        value
        for value in [left, right]
        if value > 0
    ]

    if not values:
        return 0.0

    return min(values)


def calculate_bicep_curl_signal(landmarks):

    return get_average_angle(
        landmarks,
        (
            LANDMARKS["left_shoulder"],
            LANDMARKS["left_elbow"],
            LANDMARKS["left_wrist"]
        ),
        (
            LANDMARKS["right_shoulder"],
            LANDMARKS["right_elbow"],
            LANDMARKS["right_wrist"]
        )
    )


def calculate_shoulder_press_signal(landmarks):

    return get_average_angle(
        landmarks,
        (
            LANDMARKS["left_shoulder"],
            LANDMARKS["left_elbow"],
            LANDMARKS["left_wrist"]
        ),
        (
            LANDMARKS["right_shoulder"],
            LANDMARKS["right_elbow"],
            LANDMARKS["right_wrist"]
        )
    )


def calculate_lateral_raise_signal(landmarks):

    left_shoulder = landmarks[
        LANDMARKS["left_shoulder"]
    ]

    left_wrist = landmarks[
        LANDMARKS["left_wrist"]
    ]

    right_shoulder = landmarks[
        LANDMARKS["right_shoulder"]
    ]

    right_wrist = landmarks[
        LANDMARKS["right_wrist"]
    ]

    left_height = (
        left_shoulder.y
        - left_wrist.y
    )

    right_height = (
        right_shoulder.y
        - right_wrist.y
    )

    return (
        left_height
        + right_height
    ) / 2


def calculate_front_raise_signal(landmarks):

    return calculate_lateral_raise_signal(
        landmarks
    )


def calculate_situp_signal(landmarks):

    left = get_joint_angle(
        landmarks,
        LANDMARKS["left_shoulder"],
        LANDMARKS["left_hip"],
        LANDMARKS["left_knee"]
    )

    right = get_joint_angle(
        landmarks,
        LANDMARKS["right_shoulder"],
        LANDMARKS["right_hip"],
        LANDMARKS["right_knee"]
    )

    values = [
        value
        for value in [left, right]
        if value > 0
    ]

    if not values:
        return 0.0

    return sum(values) / len(values)


def calculate_jumping_jack_signal(landmarks):

    left_shoulder = landmarks[
        LANDMARKS["left_shoulder"]
    ]

    right_shoulder = landmarks[
        LANDMARKS["right_shoulder"]
    ]

    left_wrist = landmarks[
        LANDMARKS["left_wrist"]
    ]

    right_wrist = landmarks[
        LANDMARKS["right_wrist"]
    ]

    left_ankle = landmarks[
        LANDMARKS["left_ankle"]
    ]

    right_ankle = landmarks[
        LANDMARKS["right_ankle"]
    ]

    arm_opening = (
        abs(
            left_wrist.x
            - right_wrist.x
        )
        /
        max(
            abs(
                left_shoulder.x
                - right_shoulder.x
            ),
            0.001
        )
    )

    leg_opening = abs(
        left_ankle.x
        - right_ankle.x
    )

    return (
        arm_opening
        + leg_opening
    )


def calculate_plank_signal(landmarks):

    left_shoulder = landmarks[
        LANDMARKS["left_shoulder"]
    ]

    left_hip = landmarks[
        LANDMARKS["left_hip"]
    ]

    left_ankle = landmarks[
        LANDMARKS["left_ankle"]
    ]

    angle = get_joint_angle(
        landmarks,
        LANDMARKS["left_shoulder"],
        LANDMARKS["left_hip"],
        LANDMARKS["left_ankle"]
    )

    return angle


EXERCISE_SIGNAL_FUNCTIONS = {

    "Squat":
        calculate_squat_signal,

    "Push-up":
        calculate_pushup_signal,

    "Lunge":
        calculate_lunge_signal,

    "Bicep Curl":
        calculate_bicep_curl_signal,

    "Shoulder Press":
        calculate_shoulder_press_signal,

    "Lateral Raise":
        calculate_lateral_raise_signal,

    "Front Raise":
        calculate_front_raise_signal,

    "Sit-up / Crunch":
        calculate_situp_signal,

    "Jumping Jack":
        calculate_jumping_jack_signal,

    "Plank":
        calculate_plank_signal
}


def calculate_movement_signal(
    exercise,
    landmarks
):

    function = EXERCISE_SIGNAL_FUNCTIONS.get(
        exercise
    )

    if function is None:

        raise ValueError(
            f"No movement signal configured for {exercise}"
        )

    return function(
        landmarks
    )


def track_video_movement(
    video_bytes,
    file_name,
    exercise,
    progress_callback=None,
    target_fps=15.0
):

    if not video_bytes:

        raise ValueError(
            "No video data was provided."
        )

    extension = os.path.splitext(
        file_name
    )[1].lower()

    if not extension:

        extension = ".mp4"

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    )

    video_path = temp_file.name

    try:

        temp_file.write(
            video_bytes
        )

        temp_file.close()

        cap = cv2.VideoCapture(
            video_path
        )

        if not cap.isOpened():

            raise ValueError(
                "Could not open the uploaded video."
            )

        total_frames = int(
            cap.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        fps = float(
            cap.get(
                cv2.CAP_PROP_FPS
            )
        )

        if fps <= 0:

            fps = 30.0

        if total_frames <= 0:

            cap.release()

            raise ValueError(
                "The video contains no readable frames."
            )

        duration = (
            total_frames / fps
        )

        if target_fps <= 0:

            target_fps = 15.0

        frame_step = max(
            1,
            int(
                round(
                    fps / target_fps
                )
            )
        )

        detector = create_pose_detector()

        records = []

        frame_index = 0

        processed_frames = 0

        try:

            while True:

                success, frame = cap.read()

                if not success:

                    break

                current_frame = frame_index

                frame_index += 1

                if (
                    current_frame
                    % frame_step
                    != 0
                ):

                    continue

                frame_rgb = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                timestamp_ms = int(
                    current_frame
                    * 1000
                    / fps
                )

                landmarks = process_video_frame(
                    detector,
                    frame_rgb,
                    timestamp_ms
                )

                processed_frames += 1

                if progress_callback:

                    progress_callback(
                        current_frame
                        /
                        max(
                            1,
                            total_frames - 1
                        ),
                        (
                            f"Processing frame "
                            f"{current_frame + 1} "
                            f"of "
                            f"{total_frames}"
                        )
                    )

                if landmarks is None:

                    continue

                try:

                    signal = calculate_movement_signal(
                        exercise,
                        landmarks
                    )

                except Exception:

                    continue

                if signal is None:

                    continue

                try:

                    signal = float(
                        signal
                    )

                except Exception:

                    continue

                records.append(
                    {
                        "frame_index":
                            current_frame,

                        "time":
                            current_frame / fps,

                        "timestamp_ms":
                            timestamp_ms,

                        "signal":
                            signal
                    }
                )

        finally:

            close_pose_detector(
                detector
            )

            cap.release()

        return {

            "records":
                records,

            "duration":
                duration,

            "fps":
                fps,

            "total_frames":
                total_frames,

            "processed_frames":
                processed_frames,

            "exercise":
                exercise,

            "target_fps":
                target_fps
        }

    finally:

        try:

            os.remove(
                video_path
            )

        except Exception:

            pass