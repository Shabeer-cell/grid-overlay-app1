import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Grid Overlay Tool", layout="centered")
st.title("🧰 Grid Overlay for Visual Inspection")

# File upload
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

# Parameters for grid
spacing = st.slider("📏 Grid Spacing (pixels)", 10, 100, 50)
thickness = st.slider("✏️ Line Thickness", 1, 10, 2)

# Color selection
color_name = st.selectbox("🎨 Select Grid Color", ["Blue", "Red", "Green", "Black", "White"])
color_map = {
    "Blue": (255, 0, 0),
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Black": (0, 0, 0),
    "White": (255, 255, 255)
}
grid_color = color_map[color_name]

if uploaded_file is not None:
    # Convert image to OpenCV format
    image = Image.open(uploaded_file)
    img_np = np.array(image)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Draw grid
    height, width, _ = img_bgr.shape
    grid_img = img_bgr.copy()
    for x in range(0, width, spacing):
        cv2.line(grid_img, (x, 0), (x, height), grid_color, thickness)
    for y in range(0, height, spacing):
        cv2.line(grid_img, (0, y), (width, y), grid_color, thickness)

    # Convert to RGB and display
    output_img = cv2.cvtColor(grid_img, cv2.COLOR_BGR2RGB)
    st.image(output_img, caption="✅ Grid Applied", use_column_width=True)

    # Save for download
    result = Image.fromarray(output_img)
    result.save("grid_output.jpg")
    with open("grid_output.jpg", "rb") as f:
        st.download_button("⬇️ Download Image", f, file_name="grid_output.jpg", mime="image/jpeg")
