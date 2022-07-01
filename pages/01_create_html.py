import streamlit as st
from wedding_utils import WeddingException
import wedding_utils


def main():
    st.expander("Show help").help(st.selectbox)
    st.write(st.session_state)
    st.selectbox("Image format", options=["png", "jpeg"], key="image_format")
    st.write(st.session_state)
    # "invite_text": _INVITE_TEXT,
    # "image_width": 1400,


if __name__ == "__main__":
    wedding_utils.run_main(main)
