import streamlit as st

import wedding_utils


def get_data_url():
    raise NotImplementedError("get_data_url")

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


def main():
    st.subheader("Image")
    data_url, img_width = get_data_url()
    create_email(data_url, img_width)


if __name__ == "__main__":
    st.write(wedding_utils)
    wedding_utils.run_main(main)
