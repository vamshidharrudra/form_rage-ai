from io import BytesIO

from PIL import Image


MAX_IMAGE_SIZE_MB = 20


SUPPORTED_IMAGE_TYPES = [
    "jpg",
    "jpeg",
    "png",
    "webp"
]


def validate_image(image_bytes):
    """
    Validate an uploaded image.

    Returns:
        tuple:
            (is_valid, message)
    """

    if not image_bytes:
        return False, "No image was uploaded."

    size_mb = (
        len(image_bytes)
        / (1024 * 1024)
    )

    if size_mb > MAX_IMAGE_SIZE_MB:
        return False, (
            f"Image is {size_mb:.1f} MB. "
            f"Maximum allowed size is "
            f"{MAX_IMAGE_SIZE_MB} MB."
        )

    try:

        image = Image.open(
            BytesIO(image_bytes)
        )

        image.verify()

    except Exception:

        return False, (
            "The uploaded file is not "
            "a valid image."
        )

    return True, "Image is valid."


def load_image(image_bytes):
    """
    Convert bytes into a PIL image.
    """

    return Image.open(
        BytesIO(image_bytes)
    )


def resize_image(
    image_bytes,
    max_width=1600
):
    """
    Resize large images while preserving
    aspect ratio.

    Returns JPEG bytes.
    """

    image = Image.open(
        BytesIO(image_bytes)
    ).convert("RGB")

    width, height = image.size

    if width > max_width:

        ratio = (
            max_width / width
        )

        new_height = int(
            height * ratio
        )

        image = image.resize(
            (
                max_width,
                new_height
            )
        )

    output = BytesIO()

    image.save(
        output,
        format="JPEG",
        quality=90
    )

    return output.getvalue()