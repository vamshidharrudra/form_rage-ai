import base64
import json
from io import BytesIO

import streamlit as st
from groq import Groq
from PIL import Image, ImageDraw


MODEL_NAME = "qwen/qwen3.6-27b"


@st.cache_resource
def get_groq_client():

    api_key = st.secrets.get(
        "GROQ_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "GROQ_API_KEY not found in Streamlit secrets."
        )

    return Groq(
        api_key=api_key
    )


def encode_image(
    image_bytes
):

    return base64.b64encode(
        image_bytes
    ).decode(
        "utf-8"
    )


def parse_response(
    response
):

    text = (
        response
        .choices[0]
        .message
        .content
    )

    if not text:

        raise ValueError(
            "Groq returned an empty response."
        )

    try:

        return json.loads(
            text
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "Groq returned invalid JSON."
        ) from error


def analyze_image(
    image_bytes,
    prompt
):

    client = get_groq_client()

    image_base64 = encode_image(
        image_bytes
    )

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",

                "content": [

                    {
                        "type": "text",
                        "text": prompt
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url":
                                "data:image/jpeg;base64,"
                                + image_base64
                        }
                    }
                ]
            }
        ],

        temperature=0.2,

        max_completion_tokens=300,

        reasoning_effort="none",

        response_format={
            "type": "json_object"
        }
    )

    return parse_response(
        response
    )


def create_rep_contact_sheet(
    frame_bytes
):

    if not frame_bytes:

        raise ValueError(
            "No repetition frames provided."
        )

    images = []

    for image_bytes in frame_bytes[:3]:

        image = Image.open(
            BytesIO(
                image_bytes
            )
        ).convert(
            "RGB"
        )

        image.thumbnail(
            (
                160,
                160
            )
        )

        images.append(
            image
        )

    while len(images) < 3:

        images.append(
            images[-1].copy()
        )

    sheet = Image.new(
        "RGB",
        (
            480,
            190
        ),
        "white"
    )

    draw = ImageDraw.Draw(
        sheet
    )

    labels = [
        "START",
        "PEAK",
        "END"
    ]

    for index, image in enumerate(
        images
    ):

        x = index * 160

        image_x = (
            x
            +
            (
                160
                -
                image.width
            )
            // 2
        )

        image_y = 25

        sheet.paste(
            image,
            (
                image_x,
                image_y
            )
        )

        draw.text(
            (
                x + 8,
                5
            ),
            labels[index],
            fill="black"
        )

    output = BytesIO()

    sheet.save(
        output,
        format="JPEG",
        quality=40,
        optimize=True
    )

    return output.getvalue()


def analyze_rep_frames(
    frame_bytes,
    prompt
):

    client = get_groq_client()

    contact_sheet = create_rep_contact_sheet(
        frame_bytes
    )

    image_base64 = encode_image(
        contact_sheet
    )

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",

                "content": [

                    {
                        "type": "text",
                        "text": prompt
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url":
                                "data:image/jpeg;base64,"
                                + image_base64
                        }
                    }
                ]
            }
        ],

        temperature=0.2,

        max_completion_tokens=256,

        reasoning_effort="none",

        response_format={
            "type": "json_object"
        }
    )

    return parse_response(
        response
    )


def generate_text(
    prompt
):

    client = get_groq_client()

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.5,

        max_completion_tokens=300,

        reasoning_effort="none"
    )

    result = (
        response
        .choices[0]
        .message
        .content
    )

    if not result:

        raise ValueError(
            "Groq returned an empty response."
        )

    return result