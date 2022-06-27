import wedding_utils
from wedding_utils import WeddingException
import streamlit as st


def main():
    st.title("Scratchpad")
    data_url = wedding_utils.get_data_url()
    st.write("Data URL len:", len(data_url))
    st.code(data_url[:100])


if __name__ == "__main__":
    wedding_utils.run_main(main)
