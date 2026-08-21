import math
from dataclasses import dataclass


REP_DETECTION_CONFIG = {
    "Squat": {
        "min_amplitude": 20.0,
        "min_duration": 0.8,
        "max_duration": 8.0
    },
    "Push-up": {
        "min_amplitude": 20.0,
        "min_duration": 0.6,
        "max_duration": 6.0
    },
    "Lunge": {
        "min_amplitude": 20.0,
        "min_duration": 0.8,
        "max_duration": 8.0
    },
    "Bicep Curl": {
        "min_amplitude": 30.0,
        "min_duration": 0.5,
        "max_duration": 5.0
    },
    "Shoulder Press": {
        "min_amplitude": 25.0,
        "min_duration": 0.7,
        "max_duration": 6.0
    },
    "Lateral Raise": {
        "min_amplitude": 0.08,
        "min_duration": 0.5,
        "max_duration": 5.0
    },
    "Front Raise": {
        "min_amplitude": 0.08,
        "min_duration": 0.5,
        "max_duration": 5.0
    },
    "Sit-up / Crunch": {
        "min_amplitude": 20.0,
        "min_duration": 0.7,
        "max_duration": 7.0
    },
    "Jumping Jack": {
        "min_amplitude": 0.10,
        "min_duration": 0.4,
        "max_duration": 5.0
    },
    "Plank": {
        "min_amplitude": 0.0,
        "min_duration": 2.0,
        "max_duration": 180.0
    }
}


@dataclass
class Repetition:
    rep_number: int
    start_frame: int
    peak_frame: int
    end_frame: int
    start_time: float
    peak_time: float
    end_time: float
    duration: float
    amplitude: float
    confidence: float
    direction: str = ""
    complete: bool = True
    reason: str = ""

    def to_dict(self):
        return {
            "rep_number": self.rep_number,
            "start_frame": self.start_frame,
            "peak_frame": self.peak_frame,
            "end_frame": self.end_frame,
            "start_time": self.start_time,
            "peak_time": self.peak_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "amplitude": self.amplitude,
            "confidence": self.confidence,
            "direction": self.direction,
            "complete": self.complete,
            "reason": self.reason
        }


def clean_signal(signal):
    cleaned = []

    if signal is None:
        return cleaned

    for value in signal:
        try:
            value = float(value)
        except Exception:
            continue

        if not math.isfinite(value):
            continue

        cleaned.append(value)

    return cleaned


def smooth_signal(signal, window=5):
    if len(signal) < 3:
        return signal[:]

    window = max(3, int(window))

    if window % 2 == 0:
        window += 1

    result = []
    half = window // 2

    for index in range(len(signal)):
        start = max(0, index - half)
        end = min(
            len(signal),
            index + half + 1
        )

        values = signal[start:end]

        result.append(
            sum(values) / len(values)
        )

    return result


def calculate_amplitude(values):
    if not values:
        return 0.0

    return max(values) - min(values)


def _find_extreme_index(
    signal,
    start,
    end,
    direction
):
    if end <= start:
        return start

    section = signal[start:end + 1]

    if direction == "down":
        local_index = min(
            range(len(section)),
            key=lambda i: section[i]
        )
    else:
        local_index = max(
            range(len(section)),
            key=lambda i: section[i]
        )

    return start + local_index


def _calculate_confidence(
    amplitude,
    duration,
    minimum_amplitude,
    minimum_duration,
    maximum_duration
):
    if minimum_amplitude <= 0:
        amplitude_score = 1.0
    else:
        amplitude_score = min(
            1.0,
            amplitude / minimum_amplitude
        )

    if duration < minimum_duration:
        duration_score = (
            duration / minimum_duration
        )
    elif duration > maximum_duration:
        duration_score = (
            maximum_duration / duration
        )
    else:
        duration_score = 1.0

    confidence = (
        amplitude_score * 0.65
        +
        duration_score * 0.35
    )

    return round(
        max(
            0.0,
            min(
                1.0,
                confidence
            )
        ) * 100,
        1
    )


def _build_repetition(
    rep_number,
    start_index,
    peak_index,
    end_index,
    signal,
    smoothed,
    frame_indices,
    times,
    direction,
    config
):
    if end_index <= start_index:
        return None

    start_time = times[start_index]
    peak_time = times[peak_index]
    end_time = times[end_index]

    duration = end_time - start_time

    if duration < config["min_duration"]:
        return None

    if duration > config["max_duration"]:
        return None

    section = smoothed[
        start_index:end_index + 1
    ]

    amplitude = calculate_amplitude(
        section
    )

    if amplitude < config["min_amplitude"]:
        return None

    confidence = _calculate_confidence(
        amplitude,
        duration,
        config["min_amplitude"],
        config["min_duration"],
        config["max_duration"]
    )

    return Repetition(
        rep_number=rep_number,
        start_frame=frame_indices[start_index],
        peak_frame=frame_indices[peak_index],
        end_frame=frame_indices[end_index],
        start_time=start_time,
        peak_time=peak_time,
        end_time=end_time,
        duration=duration,
        amplitude=amplitude,
        confidence=confidence,
        direction=direction,
        complete=True,
        reason="Complete movement cycle detected."
    )


def detect_repetitions(
    records,
    exercise,
    fps=None
):
    if not records:
        return []

    config = REP_DETECTION_CONFIG.get(
        exercise
    )

    if config is None:
        raise ValueError(
            f"Unsupported exercise: {exercise}"
        )

    signal = []
    frame_indices = []
    times = []

    for record in records:
        if not isinstance(record, dict):
            continue

        try:
            value = float(
                record["signal"]
            )

            frame = int(
                record["frame_index"]
            )

            time_value = float(
                record["time"]
            )

        except Exception:
            continue

        if not math.isfinite(value):
            continue

        signal.append(value)
        frame_indices.append(frame)
        times.append(time_value)

    if len(signal) < 5:
        return []

    if exercise == "Plank":
        return detect_plank(
            signal,
            frame_indices,
            times,
            config
        )

    cleaned = clean_signal(
        signal
    )

    if len(cleaned) < 5:
        return []

    smoothed = smooth_signal(
        cleaned
    )

    repetitions = []

    minimum_amplitude = config[
        "min_amplitude"
    ]

    minimum_duration = config[
        "min_duration"
    ]

    maximum_duration = config[
        "max_duration"
    ]

    state = "waiting"
    start_index = None
    direction = None
    rep_number = 1

    for index in range(
        1,
        len(smoothed)
    ):
        difference = (
            smoothed[index]
            -
            smoothed[index - 1]
        )

        if state == "waiting":

            if abs(difference) < 0.5:
                continue

            start_index = index - 1

            if difference < 0:
                direction = "down"
            else:
                direction = "up"

            state = "moving"

            continue

        if state == "moving":

            if direction == "down":

                if (
                    smoothed[index]
                    >
                    smoothed[index - 1]
                ):

                    peak_index = (
                        _find_extreme_index(
                            smoothed,
                            start_index,
                            index,
                            "down"
                        )
                    )

                    repetition = (
                        _build_repetition(
                            rep_number,
                            start_index,
                            peak_index,
                            index,
                            cleaned,
                            smoothed,
                            frame_indices,
                            times,
                            direction,
                            config
                        )
                    )

                    if repetition is not None:
                        repetitions.append(
                            repetition
                        )

                        rep_number += 1

                    start_index = index
                    direction = "up"

            else:

                if (
                    smoothed[index]
                    <
                    smoothed[index - 1]
                ):

                    peak_index = (
                        _find_extreme_index(
                            smoothed,
                            start_index,
                            index,
                            "up"
                        )
                    )

                    repetition = (
                        _build_repetition(
                            rep_number,
                            start_index,
                            peak_index,
                            index,
                            cleaned,
                            smoothed,
                            frame_indices,
                            times,
                            direction,
                            config
                        )
                    )

                    if repetition is not None:
                        repetitions.append(
                            repetition
                        )

                        rep_number += 1

                    start_index = index
                    direction = "down"

    return repetitions


def detect_plank(
    signal,
    frame_indices,
    times,
    config
):
    if len(signal) < 2:
        return []

    duration = (
        times[-1]
        -
        times[0]
    )

    if duration < config["min_duration"]:
        return []

    amplitude = calculate_amplitude(
        signal
    )

    confidence = 100.0

    if amplitude > 20:
        confidence = 60.0

    middle = len(frame_indices) // 2

    repetition = Repetition(
        rep_number=1,
        start_frame=frame_indices[0],
        peak_frame=frame_indices[middle],
        end_frame=frame_indices[-1],
        start_time=times[0],
        peak_time=times[middle],
        end_time=times[-1],
        duration=duration,
        amplitude=amplitude,
        confidence=confidence,
        direction="hold",
        complete=True,
        reason="Plank hold detected."
    )

    return [repetition]


def get_rep_key_frames(
    repetition
):
    return {
        "start": repetition.start_frame,
        "peak": repetition.peak_frame,
        "end": repetition.end_frame
    }


def get_rep_summary(
    repetitions
):
    if not repetitions:
        return {
            "total_reps": 0,
            "average_confidence": 0,
            "average_duration": 0,
            "average_amplitude": 0
        }

    confidences = [
        rep.confidence
        for rep in repetitions
    ]

    durations = [
        rep.duration
        for rep in repetitions
    ]

    amplitudes = [
        rep.amplitude
        for rep in repetitions
    ]

    return {
        "total_reps": len(
            repetitions
        ),
        "average_confidence": round(
            sum(confidences)
            /
            len(confidences),
            1
        ),
        "average_duration": round(
            sum(durations)
            /
            len(durations),
            2
        ),
        "average_amplitude": round(
            sum(amplitudes)
            /
            len(amplitudes),
            2
        )
    }