import streamlit as st
from wedding_utils import WeddingException
import wedding_utils


def main():
    st.expander("Show help").help(st.selectbox)
    wedding_utils.selectbox(
        "Image format",
        options=["png", "jpeg"],
        key="image_format",
    )


if __name__ == "__main__":
    wedding_utils.run_main(main)
