import wedding_utils
import streamlit as st

# from wedding_utils import WeddingException


def main():
    st.title("Scratchpad")
    data_url, width, height = wedding_utils.get_img_data()
    st.write("Data URL len:", len(data_url))
    st.code(data_url[:100])
    st.experimental_show(width)
    st.experimental_show(height)


if __name__ == "__main__":
    wedding_utils.run_main(main)
