import streamlit as st
from google import genai
import urllib.parse

# 1. Authenticate securely using your existing Google API Key for text strategy
client = genai.Client(api_key=st.secrets["API_KEY"])

st.set_page_config(page_title="Brand Builder", page_icon="🎨")

st.title("🎨 Brand Builder")
st.markdown("Generate professional multi-channel marketing strategies and real AI visual assets.")

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
        with st.spinner(f"Crafting your {selected_medium} campaign & rendering visual..."):
            try:
                # 1. Generate marketing strategy copy using Gemini text model
                prompt = f"""
                You are an expert creative director. For the product '{product_name}' described as: '{product_desc}':
                Create a high-converting marketing strategy for a {selected_medium}.
                Include a compelling headline and copywriting caption. Keep it structured and clean.
                """
                
                response = client.models.generate_content(
                    model='gemini-3.7-flash',
                    contents=prompt
                )
                
                st.subheader(f"Campaign Asset: {selected_medium}")
                st.markdown(response.text)
                
                # 2. Render a real AI-generated image preview using a free public image engine
                st.divider()
                st.markdown("### 🖼️ Real AI-Generated Visual Asset")
                
                # Create a clean art direction prompt for the image
                image_query = f"Commercial product photography of {product_desc}, professional lighting, studio background, designed for a {selected_medium}, highly detailed, 4k, no people"
                encoded_prompt = urllib.parse.quote(image_query)
                
                # Free public AI image URL generator (no billing or quota limits)
                ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
                
                st.image(
                    ai_image_url,
                    caption=f"AI Visual Concept for {product_name} ({selected_medium})"
                )
                
            except Exception as e:
                st.error(f"Error generating campaign: {e}")
else:
    st.info("Fill out your product details in the sidebar, select a medium, and click 'Generate Strategy & Asset'.")
