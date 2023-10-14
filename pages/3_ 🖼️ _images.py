import streamlit as st
import requests
import json
import dotenv
import os

st.set_page_config(layout="wide")

# Load environment variables
dotenv.load_dotenv()

# Cloudflare API details
API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")

# Cloudflare Images API endpoint
API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/images/v1"


# Streamlit app layout
def main():
    st.header("Upload to Cloudflare Images")

    # Image uploader
    uploaded_image = st.file_uploader("Upload an image")

    if uploaded_image is not None:
        metadata = st.text_input("Image Metadata (optional)", "")
        require_signed_urls = st.checkbox("Require Signed URLs")

        if st.button("Upload Image"):
            response = upload_image(uploaded_image, metadata, require_signed_urls)
            response_data = response.json()

            if response_data.get("success", False):
                st.success("Image uploaded successfully!")
                st.experimental_rerun()
            else:
                st.write(response.json())
                st.error(
                    "Failed to upload image. Please check the Cloudflare API response."
                )

    st.header("Cloudflare Images Gallery")
    # Pagination
    pag_col1, pag_col2 = st.columns(2)
    with pag_col1:
        page_number = st.number_input("Page number", value=1, min_value=1, step=1)
    with pag_col2:
        per_page = st.number_input(
            "Images per page", value=12, min_value=10, max_value=10000, step=10
        )

    # Fetch images using Cloudflare API
    response = fetch_images(page_number, per_page)
    images = response.get("result", {}).get("images", [])

    if not images:
        st.write("No images found.")
    else:
        st.write("Displaying {} images:".format(len(images)))

        # Create a grid layout with 3 columns
        col1, col2, col3 = st.columns(3)

        for idx, image in enumerate(images):
            image_title = image.get("filename", "")
            for idy, image_url in enumerate(image.get("variants", [])):
                img_col = col1 if idx % 3 == 0 else col2 if idx % 3 == 1 else col3
                with img_col:
                    # Make the image clickable
                    st.markdown(
                        f'<a href="{image_url}" target="_blank"><img src="{image_url}" alt="{image_title}" width="100%"></a>',
                        unsafe_allow_html=True,
                    )
                    st.caption(image_title + "-" + str(idy))
                    # Add a "Delete" button
                    if st.button("Delete", key=f"delete_{idx}_{idy}"):
                        delete_image(image.get("id"))
                        st.info(f"Image '{image_title}' deleted.")
                        st.experimental_rerun()


# Fetch images using Cloudflare API
def fetch_images(page_number, per_page):
    headers = {
        "Authorization": "Bearer {}".format(API_TOKEN),
        "Content-Type": "application/json",
    }

    params = {"page": page_number, "per_page": per_page}

    response = requests.get(API_BASE_URL, headers=headers, params=params)
    data = response.json()

    return data


# Upload image using Cloudflare API
def upload_image(image, metadata, require_signed_urls):
    headers = {"Authorization": "Bearer {}".format(API_TOKEN)}

    data = {
        "metadata": json.dumps(metadata),
        "requireSignedURLs": require_signed_urls,
        "id": image.name,
    }

    response = requests.post(
        API_BASE_URL, headers=headers, data=data, files={"file": (image.name, image)}
    )
    return response


# Delete image using Cloudflare API
def delete_image(image_id):
    headers = {
        "Authorization": "Bearer {}".format(API_TOKEN),
        "Content-Type": "application/json",
    }

    delete_url = f"{API_BASE_URL}/{image_id}"
    response = requests.delete(delete_url, headers=headers)
    return response


if __name__ == "__main__":
    main()
