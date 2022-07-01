import textwrap
import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from typing import Literal, Tuple

_INVITE_TEXT = textwrap.dedent(
    """
    Save the date. Oct 15, 2022. Regan and Adrien.
    The Land, Santa Cruz Mountains, California.
    We would be so excited to see you.
    """
)

_DEFAULT_STATE = {
    "image_file": "./adrien-regan-save-the-date.png",
    "image_format": "jpeg",
    "invite_text": _INVITE_TEXT,
    "image_width": 1400,
    "subject": "This is a test",
}


def init_session_state():
    """Initializes the session state with default values."""
    with st.expander("Before init_session_state"):
        st.json(st.session_state)
    for k, v in _DEFAULT_STATE.items():
        if k not in st.session_state:
            st.session_state[k] = v
    with st.expander("After init_session_state"):
        st.json(st.session_state)


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
    return st.session_state.invite_text


def _to_css_str(css_attrs):
    return ";".join(f"{k}:{v}" for k, v in css_attrs.items())


def get_email_html() -> str:
    """Get the email html."""
    data_url, img_width, _ = get_img_data()
    border_size = 20

    table_style = {
        "border": "0px black",
        "padding": "0px",
        "spacing": "0px",
        "margin": "0px",
        "width": "100%",
    }

    tr_style = {
        "border": "0px black",
        "padding": "0px",
        "spacing": "0px",
        "margin": "0px",
    }

    td_style = {
        "border": "0px black",
        "padding": f"{border_size}px",
        "spacing": "0px",
        "margin": "0px",
        "background-color": "black",
        "color": "#444444",
        "font-family": "Sans-Serif",
        "text-align": "center",
    }

    img_style = {
        "border": "0px black",
        "width": f"100%",
        "max-width": f"{img_width}px",
        "display": "block",
        "margin": "0 auto",
    }

    body_text = "\n".join(
        f"<div>{s}.</div>" for s in st.session_state.invite_text.split(".")
    )

    return textwrap.dedent(
        f"""
        <table style="{_to_css_str(table_style)}"
            <tr style="{_to_css_str(tr_style)}">
                <td style="{_to_css_str(td_style)}">
                    <img 
                        src="{data_url}" 

                        alt="{st.session_state.invite_text}"

                        style="{_to_css_str(img_style)}"
                    >
                    {st.session_state.invite_text}
                </td>
            </tr>
        </table>
        """
    )


@st.experimental_memo  # type: ignore
def _get_image_base_64(
    image_file, image_format: Literal["jpeg", "png"], desired_width: int
) -> Tuple[str, int, int]:
    """Gets the image data along with the image width and height."""
    # Open the image and convert it ot image_format
    im = Image.open(image_file).convert("RGB")

    # Resize the image if need be

    # Write the image data in the right format
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
    desired_width = st.session_state.image_width

    return _get_image_base_64(
        st.session_state.image_file, st.session_state.image_format, desired_width
    )
