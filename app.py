import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.markdown("""
    <style>
        .big-font { font-size:20px !important; }
        .stButton button { background-color: #FF4B4B; color: white; font-size: 16px; padding: 10px; border-radius: 10px; }
        .stColorPicker, .stSlider { margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.subheader("🎨 YouTube Thumbnail Generator")

# Upload main image
uploaded_image = st.file_uploader("📤 Upload Side Image", type=["jpg", "png", "jpeg"])

# Background settings
background_option = st.radio("🖼 Choose Background Color or Image", ("Color", "Image"))
text_bg_color = st.color_picker("🎨 Pick a background color", "#FFFFFF") if background_option == "Color" else None
text_bg_image = st.file_uploader("📤 Upload background image", type=["jpg", "png", "jpeg"]) if background_option == "Image" else None

# Text items storage
if "text_items" not in st.session_state:
    st.session_state.text_items = []

# Add new text input with inheritance
if st.button("➕ Add Text"):
    last_text = st.session_state.text_items[-1] if st.session_state.text_items else {"text": "", "x": 50, "y": 100, "size": 40, "color": "#000000"}
    st.session_state.text_items.append({"text": "", "x": 50, "y": 100, "size": last_text["size"], "color": last_text["color"]})

# Modify existing text items
for idx, text_item in enumerate(st.session_state.text_items):
    with st.expander(f"📝 Text {idx + 1}"):
        text_item["text"] = st.text_area(f"Enter text {idx+1}", text_item["text"], key=f"text_{idx}")
        text_item["x"] = st.slider(f"↔ X Position {idx+1}", 0, 800, text_item["x"], key=f"x_{idx}")
        text_item["y"] = st.slider(f"↕ Y Position {idx+1}", 0, 600, text_item["y"], key=f"y_{idx}")
        text_item["size"] = st.slider(f"🔠 Font Size {idx+1}", 20, 100, text_item["size"], key=f"size_{idx}")
        text_item["color"] = st.color_picker(f"🎨 Text Color {idx+1}", text_item["color"], key=f"color_{idx}")

# Font setup
urdu_font_path = "/home/habib92/wow/thumbnail-generator/Noto_Nastaliq_Urdu/static/NotoNastaliqUrdu-Regular.ttf"

if uploaded_image:
    image = Image.open(uploaded_image).resize((426, 720))
    background = Image.open(text_bg_image).resize((854, 720)) if text_bg_image else Image.new("RGB", (854, 720), color=text_bg_color)
    thumbnail = Image.new("RGB", (1280, 720))
    thumbnail.paste(background, (0, 0))
    thumbnail.paste(image, (854, 0))
    
    draw = ImageDraw.Draw(thumbnail)
    for text_item in st.session_state.text_items:
        font = ImageFont.truetype(urdu_font_path, text_item["size"])
        draw.text((text_item["x"], text_item["y"]), text_item["text"], font=font, fill=text_item["color"])
    
    st.image(thumbnail, caption="🖼 Generated Thumbnail")
    buf = io.BytesIO()
    thumbnail.save(buf, format="PNG")
    st.download_button("⬇ Download Thumbnail", data=buf.getvalue(), file_name="thumbnail.png", mime="image/png")
