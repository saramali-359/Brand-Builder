import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# 1. Authenticate securely using your existing Google API Key
client = genai.Client(api_key=st.secrets["API_KEY"])

st.set_page_config(page_title="Brand Builder", page_icon="🎨")

st.title("🎨 Brand Builder")
st.markdown("Generate professional multi-channel marketing strategies and visual assets using Google Gemini.")

# --- Product Definition ---
st.sidebar.header("Product Identity")
product_name = st.sidebar.text_input("Product Name", placeholder="e.g., Onyx Flask")
product_desc = st.sidebar.text_area(
    "Describe the Product (The Anchor)", 
    placeholder="e.g., A sleek, matte-black reusable water bottle with a gold hexagonal cap. No logos."
)

st.sidebar.warning("🚫 Policy: No people will be included in any assets.")

selected_medium = st.selectbox(
    "Select Marketing Medium:",
    ["Outdoor Billboard", "Vintage Newspaper", "Social Media Post"]
)

if st.button("Generate Strategy & Asset"):
    if not product_desc:
        st.error("Please describe your product first in the sidebar!")
    else:
        with st.spinner(f"Crafting your {selected_medium} campaign and generating visual..."):
            try:
                # 1. Generate the strategy text
                strategy_prompt = f"""
                You are an expert creative director. For the product '{product_name}' described as: '{product_desc}':
                Create a high-converting marketing strategy for a {selected_medium}.
                Include a compelling headline and copywriting caption. Keep it structured and clean.
                """
                
                strategy_response = client.models.generate_content(
                    model='gemini-3.7-flash',
                    contents=strategy_prompt
                )
                
                st.subheader(f"Campaign Asset: {selected_medium}")
                st.markdown(strategy_response.text)
                
                st.divider()
                st.markdown("### 🖼️ Real AI-Generated Visual Asset")
                
                # 2. Generate the actual image using Google's native image model
                image_prompt = f"A professional marketing asset for a {selected_medium} featuring {product_desc}. High quality, commercial photography style. No people."
                
                image_response = client.models.generate_content(
                    model='gemini-3.1-flash-image',
                    contents=image_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(
                            aspect_ratio="16:9" if selected_medium == "Outdoor Billboard" else "1:1",
                        ),
                    ),
                )
                
                # 3. Extract and display the image bytes cleanly
                image_rendered = False
                for part in image_response.parts:
                    if part.inline_data:
                        image_bytes = part.inline_data.data
                        img = Image.open(BytesIO(image_bytes))
                        st.image(img, caption=f"Generated {selected_medium} for {product_name}")
                        image_rendered = True
                        break
                
                if not image_rendered:
                    st.info("Strategy text generated successfully. Visual asset rendering was skipped by the model policy.")
                
            except Exception as e:
                st.error(f"Error generating assets: {e}")
else:
    st.info("Fill out your product details in the sidebar, select a medium, and click 'Generate Strategy & Asset'.")
