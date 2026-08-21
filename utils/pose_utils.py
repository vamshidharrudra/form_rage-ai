import math
import os

import mediapipe as mp


MODEL_PATH = os.path.join(
    "models",
    "pose_landmarker_full.task"
)


LANDMARKS = {
    "nose": 0,

    "left_eye_inner": 1,
    "left_eye": 2,
    "left_eye_outer": 3,

    "right_eye_inner": 4,
    "right_eye": 5,
    "right_eye_outer": 6,

    "left_ear": 7,
    "right_ear": 8,

    "mouth_left": 9,
    "mouth_right": 10,

    "left_shoulder": 11,
    "right_shoulder": 12,

    "left_elbow": 13,
    "right_elbow": 14,

    "left_wrist": 15,
    "right_wrist": 16,

    "left_pinky": 17,
    "right_pinky": 18,

    "left_index": 19,
    "right_index": 20,

    "left_thumb": 21,
    "right_thumb": 22,

    "left_hip": 23,
    "right_hip": 24,

    "left_knee": 25,
    "right_knee": 26,

    "left_ankle": 27,
    "right_ankle": 28,

    "left_heel": 29,
    "right_heel": 30,

    "left_foot_index": 31,
    "right_foot_index": 32,
}


def create_pose_detector(
    model_path=MODEL_PATH,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5
):

    if not os.path.exists(model_path):

        raise FileNotFoundError(
            f"Pose Landmarker model not found: {model_path}"
        )

    base_options = mp.tasks.BaseOptions(
        model_asset_path=model_path
    )

    options = mp.tasks.vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=(
            min_pose_detection_confidence
        ),
        min_pose_presence_confidence=(
            min_pose_presence_confidence
        ),
        min_tracking_confidence=(
            min_tracking_confidence
        )
    )

    detector = mp.tasks.vision.PoseLandmarker.create_from_options(
        options
    )

    return detector


def process_video_frame(
    detector,
    frame_rgb,
    timestamp_ms
):

    if detector is None:

        raise ValueError(
            "Pose detector is not initialized."
        )

    if frame_rgb is None:

        return None

    image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame_rgb
    )

    result = detector.detect_for_video(
        image,
        int(timestamp_ms)
    )

    if not result.pose_landmarks:

        return None

    if len(result.pose_landmarks) == 0:

        return None

    return result.pose_landmarks[0]


def close_pose_detector(
    detector
):

    if detector is None:

        return

    try:

        detector.close()

    except Exception:

        pass


def get_point(
    landmark
):

    return (
        float(landmark.x),
        float(landmark.y),
        float(landmark.z)
    )


def get_joint_angle(
    landmarks,
    point_a,
    point_b,
    point_c
):

    if landmarks is None:

        return 0.0

    try:

        a = landmarks[point_a]
        b = landmarks[point_b]
        c = landmarks[point_c]

    except Exception:

        return 0.0

    ax, ay, az = get_point(a)
    bx, by, bz = get_point(b)
    cx, cy, cz = get_point(c)

    vector_ba = (
        ax - bx,
        ay - by,
        az - bz
    )

    vector_bc = (
        cx - bx,
        cy - by,
        cz - bz
    )

    magnitude_ba = math.sqrt(
        vector_ba[0] ** 2
        + vector_ba[1] ** 2
        + vector_ba[2] ** 2
    )

    magnitude_bc = math.sqrt(
        vector_bc[0] ** 2
        + vector_bc[1] ** 2
        + vector_bc[2] ** 2
    )

    if (
        magnitude_ba <= 1e-9
        or magnitude_bc <= 1e-9
    ):

        return 0.0

    dot_product = (

        vector_ba[0] * vector_bc[0]
        +
        vector_ba[1] * vector_bc[1]
        +
        vector_ba[2] * vector_bc[2]

    )

    cosine_value = (
        dot_product
        /
        (
            magnitude_ba
            *
            magnitude_bc
        )
    )

    cosine_value = max(
        -1.0,
        min(
            1.0,
            cosine_value
        )
    )

    angle = math.degrees(
        math.acos(
            cosine_value
        )
    )

    if not math.isfinite(angle):

        return 0.0

    return angle


def get_average_angle(
    landmarks,
    first_joint,
    second_joint
):

    angle_one = get_joint_angle(
        landmarks,
        first_joint[0],
        first_joint[1],
        first_joint[2]
    )

    angle_two = get_joint_angle(
        landmarks,
        second_joint[0],
        second_joint[1],
        second_joint[2]
    )

    valid_angles = []

    if angle_one > 0:

        valid_angles.append(
            angle_one
        )

    if angle_two > 0:

        valid_angles.append(
            angle_two
        )

    if not valid_angles:

        return 0.0

    return sum(
        valid_angles
    ) / len(
        valid_angles
    )


def get_landmark_visibility(
    landmarks,
    index
):

    if landmarks is None:

        return 0.0

    try:

        landmark = landmarks[index]

    except Exception:

        return 0.0

    visibility = getattr(
        landmark,
        "visibility",
        1.0
    )

    try:

        visibility = float(
            visibility
        )

    except Exception:

        return 0.0

    return max(
        0.0,
        min(
            1.0,
            visibility
        )
    )


def get_average_visibility(
    landmarks,
    indices
):

    if landmarks is None:

        return 0.0

    values = []

    for index in indices:

        value = get_landmark_visibility(
            landmarks,
            index
        )

        if value > 0:

            values.append(
                value
            )

    if not values:

        return 0.0

    return sum(
        values
    ) / len(
        values
    )


def landmarks_to_dict(
    landmarks
):

    if landmarks is None:

        return {}

    result = {}

    for name, index in LANDMARKS.items():

        try:

            landmark = landmarks[index]

        except Exception:

            continue

        result[name] = {

            "x": float(
                landmark.x
            ),

            "y": float(
                landmark.y
            ),

            "z": float(
                landmark.z
            ),

            "visibility": float(
                getattr(
                    landmark,
                    "visibility",
                    1.0
                )
            )

        }

    return result