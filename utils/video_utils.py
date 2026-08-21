import os
import tempfile

import cv2


MAX_VIDEO_SIZE_MB = 300

MIN_VIDEO_DURATION = 3

MAX_VIDEO_DURATION = 180

FRAME_WIDTH = 640

SUPPORTED_VIDEO_TYPES = [
    "mp4",
    "mov",
    "avi",
    "mkv",
    "webm"
]


def validate_video(
    video_bytes,
    file_name
):

    if not video_bytes:

        return (
            False,
            "No video was uploaded.",
            None
        )

    size_mb = (
        len(video_bytes)
        /
        (1024 * 1024)
    )

    if size_mb > MAX_VIDEO_SIZE_MB:

        return (
            False,
            f"Video is {size_mb:.1f} MB. "
            f"Maximum allowed size is "
            f"{MAX_VIDEO_SIZE_MB} MB.",
            None
        )

    extension = os.path.splitext(
        file_name
    )[1].lower()

    supported_extensions = [
        "." + item
        for item in SUPPORTED_VIDEO_TYPES
    ]

    if extension not in supported_extensions:

        return (
            False,
            "Unsupported video format. "
            "Please upload MP4, MOV, AVI, MKV or WEBM.",
            None
        )

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

            return (
                False,
                "The video could not be opened.",
                None
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

            cap.release()

            return (
                False,
                "Could not determine video FPS.",
                None
            )

        duration = (
            total_frames
            /
            fps
        )

        cap.release()

    finally:

        try:

            os.remove(
                video_path
            )

        except Exception:

            pass

    if total_frames <= 0:

        return (
            False,
            "The video contains no readable frames.",
            None
        )

    if duration < MIN_VIDEO_DURATION:

        return (
            False,
            f"Video is only {duration:.1f} seconds long. "
            f"Please upload at least "
            f"{MIN_VIDEO_DURATION} seconds.",
            None
        )

    if duration > MAX_VIDEO_DURATION:

        return (
            False,
            f"Video is {duration:.1f} seconds long. "
            f"Please upload a video between "
            f"{MIN_VIDEO_DURATION} and "
            f"{MAX_VIDEO_DURATION} seconds.",
            None
        )

    metadata = {
        "duration": duration,
        "fps": fps,
        "total_frames": total_frames,
        "extension": extension
    }

    return (
        True,
        "Video is valid.",
        metadata
    )


def resize_frame(
    frame
):

    height, width = frame.shape[:2]

    if width <= FRAME_WIDTH:

        return frame

    scale = (
        FRAME_WIDTH
        /
        width
    )

    new_width = FRAME_WIDTH

    new_height = int(
        height * scale
    )

    return cv2.resize(
        frame,
        (
            new_width,
            new_height
        ),
        interpolation=cv2.INTER_AREA
    )


def extract_frames_by_indices(
    video_bytes,
    file_name,
    frame_indices
):

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

        frames = {}

        unique_indices = sorted(
            set(
                int(index)
                for index in frame_indices
                if int(index) >= 0
            )
        )

        for frame_index in unique_indices:

            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                frame_index
            )

            success, frame = cap.read()

            if not success:

                continue

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            frame = resize_frame(
                frame
            )

            frames[
                frame_index
            ] = frame

        cap.release()

        return frames

    finally:

        try:

            os.remove(
                video_path
            )

        except Exception:

            pass


def extract_video_frames(
    video_bytes,
    file_name,
    max_frames=8
):

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

        duration = (
            total_frames
            /
            fps
        )

        if total_frames <= max_frames:

            frame_indices = list(
                range(
                    total_frames
                )
            )

        else:

            frame_indices = []

            for i in range(
                max_frames
            ):

                frame_index = int(
                    i
                    *
                    (
                        total_frames - 1
                    )
                    /
                    (
                        max_frames - 1
                    )
                )

                frame_indices.append(
                    frame_index
                )

        frames = []

        for frame_index in frame_indices:

            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                frame_index
            )

            success, frame = cap.read()

            if not success:

                continue

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            frame = resize_frame(
                frame
            )

            frames.append(
                frame
            )

        cap.release()

        return {
            "frames": frames,
            "duration": duration,
            "fps": fps,
            "total_frames": total_frames
        }

    finally:

        try:

            os.remove(
                video_path
            )

        except Exception:

            pass


def frame_to_jpeg(
    frame,
    quality=40
):

    success, encoded = cv2.imencode(
        ".jpg",
        cv2.cvtColor(
            frame,
            cv2.COLOR_RGB2BGR
        ),
        [
            int(
                cv2.IMWRITE_JPEG_QUALITY
            ),
            quality
        ]
    )

    if not success:

        raise ValueError(
            "Could not convert video frame to JPEG."
        )

    return encoded.tobytes()