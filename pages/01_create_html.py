import textwrap
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from io import BytesIO
import base64


def get_data_url():
    # Load the image
    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
    if image_file is None:
        image_file = "./adrien-regan-save-the-date.png"
        st.info("Using default file")

    # To View Uploaded Image
    im = Image.open(image_file).convert("RGB")

    # You first need to save the image again in JPEG format; using the im.tostring() method would otherwise return raw image data that no browser would recognize:
    image_format = st.selectbox("Image format", ["jpeg", "png"])
    output = BytesIO()
    im.save(output, format=image_format)
    im_data = output.getvalue()

    # This you can then encode to base64:
    image_data = base64.b64encode(im_data).decode()
    data_url = f"data:image/{image_format};base64,{image_data}"
    st.metric("Encoded size", f"{len(data_url):,} bytes")

    # Show some details of the conversion
    with st.expander("Show details"):
        st.write(
            {
                "filename": getattr(image_file, "name", image_file),
                "mode": im.mode,
                "width": im.width,
                "height": im.height,
                "encoded_size": len(data_url),
            }
        )

    # Show a preview of the image
    with st.expander("Show image preview"):
        preview_width = st.slider("Width", 200, im.width, 300)
        st.image(im, width=preview_width)
        st.write(type(im))

    return data_url, im.width


def to_css_str(css_attrs):
    return ";".join(f"{k}:{v}" for k, v in css_attrs.items())


def create_email(data_url, img_width):
    """Creates an email based on the image width."""
    st.write("### Create email")
    border_size = st.slider("Border size", 0, 200, 20)
    body_style = {
        "padding": "0px",
        "spacing": "0px",
        "margin": "0px",
        "background-color": "black",
    }

    table_style = {
        "border": "0px black",
        "padding": "0px",
        "spacing": "0px",
        "margin": "0px",
        "width": "100%",
    }

    tr_style = {
        "padding": "0px",
        "spacing": "0px",
        "margin": "0px",
    }

    td_style = {
        # "padding": "0px",
        "padding": f"{border_size}px",
        "spacing": "0px",
        "margin": "0px",
        "background-color": "black",
    }

    img_style = {
        "width": f"100%",
        "max-width": f"{img_width}px",
        "display": "block",
        "margin": "0 auto",
    }

    html = textwrap.dedent(
        f"""
        <html>
            <head></head>
            <body style="{to_css_str(body_style)}">
                <table style="{to_css_str(table_style)}"
                    <tr style="{to_css_str(tr_style)}">
                        <td style="{to_css_str(td_style)}">
                            <img 
                                src="{data_url}" 

                                alt="Save the date. Oct 15, 2022. Regan and
                                Adrien. The Land, Santa Cruz Mountains, California." 

                                style="{to_css_str(img_style)}"
                            >
                        </td>
                    </tr>
                </table>
            </body>
        </html>
    """
    )
    components.html(html, height=3000)
    if st.button("Save HTML"):
        with open("email.html", "w") as output:
            output.write(html)
            st.success(f"Wrote {output.name}")
    # st.write("data_url", type(data_url), len(data_url))
    # st.write("img_width", type(img_width), img_width)


def main():
    st.subheader("Image")
    data_url, img_width = get_data_url()
    create_email(data_url, img_width)


if __name__ == "__main__":
    main()
