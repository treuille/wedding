import wedding_utils
import streamlit as st
import streamlit.components.v1 as components

# from wedding_utils import WeddingException


def main():
    st.title("Scratchpad")
    data_url, width, height = wedding_utils.get_img_data()
    st.write("Data URL len:", len(data_url))
    st.code(data_url[:100])
    st.experimental_show(width)
    st.experimental_show(height)

    html = wedding_utils.get_email_html()
    st.code(html, language="python")
    components.html(html, height=3000)
    # if st.button("Save HTML"):
    #     with open("email.html", "w") as output:
    #         output.write(html)
    #         st.success(f"Wrote {output.name}")


if __name__ == "__main__":
    wedding_utils.run_main(main)
