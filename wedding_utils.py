import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from typing import Literal, Tuple

_DEFAULT_STATE = {
    "image_file": "./adrien-regan-save-the-date.png",
    "image_format": "jpeg",
}


def init_session_state():
    """Initializes the session state with default values."""
    for k, v in _DEFAULT_STATE.items():
        if k not in st.session_state:
            st.session_state[k] = v


def run_main(func):
    """Runs a function, extracting WeddingExceptions
    and displaying them specially."""
    try:
        init_session_state()
        func()
    except WeddingException as wedding_exception:
        st.error(wedding_exception.msg)


class WeddingException(Exception):
    """An exception to display specially."""

    def __init__(self, msg: str):
        self.msg = msg

    @classmethod
    def assertion(cls, condition: bool, msg: str):
        if not condition:
            raise cls(msg)


def get_email_text() -> str:
    """Get email text to send."""
    raise WeddingException("testing get_email_text")


def get_email_html() -> str:
    """Get the email html."""
    raise WeddingException("testing get_email_html")


@st.experimental_memo  # type: ignore
def _get_image_base_64(
    image_file, image_format: Literal["jpeg", "png"]
) -> Tuple[str, int, int]:
    """Gets the image data along with the image width and height."""
    # Open the image and convert it ot image_format
    im = Image.open(image_file).convert("RGB")
    output = BytesIO()
    im.save(output, format=image_format)
    im_data = output.getvalue()

    # Encode hte image to base64
    image_data = base64.b64encode(im_data).decode()
    data_url = f"data:image/{image_format};base64,{image_data}"

    # All done
    return data_url, im.width, im.height


def get_img_data() -> Tuple[str, int, int]:
    """Returns data_url, width, height."""
    return _get_image_base_64(
        st.session_state.image_file, st.session_state.image_format
    )
