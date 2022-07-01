import wedding_utils
import streamlit as st
import streamlit.components.v1 as components


def main():
    st.title("Wedding App")

    data_url, width, height = wedding_utils.get_img_data()
    st.write("Data URL len:", len(data_url))
    with st.expander("Show image data"):
        st.code(data_url[:100])
        st.experimental_show(width)
        st.experimental_show(height)

    email_html = wedding_utils.get_email_html()
    with st.expander("Show email html"):
        st.code(email_html, language="python")

    email_text = wedding_utils.get_email_text()
    with st.expander("Show email text"):
        st.code(email_text)

    if st.checkbox("Show html"):
        components.html(email_html, height=1000)

    st.button("Reset state", on_click=wedding_utils.reset_state)


if __name__ == "__main__":
    wedding_utils.run_main(main)
