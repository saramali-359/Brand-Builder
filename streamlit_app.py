import streamlit as st
from google import genai

# 1. Authenticate securely using your existing Google API Key
client = genai.Client(api_key=st.secrets["API_KEY"])

st.set_page_config(page_title="Brand Builder", page_icon="🎨")

st.title("🎨 Brand Builder")
st.markdown("Generate professional multi-channel marketing strategies and visual concepts using Google Gemini.")

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
        with st.spinner(f"Crafting your {selected_medium} campaign..."):
            try:
                # Use the free-tier text model (gemini-2.0-flash) to write high-end ad copy & design prompts
                prompt = f"""
                You are an expert creative director. For the product '{product_name}' described as: '{product_desc}':
                Create a high-converting marketing strategy for a {selected_medium}.
                Include:
                1. A compelling headline or hook.
                2. Detailed visual art direction / prompt for an image generator.
                3. Copywriting caption or body text.
                Keep it structured and clean. No people in the visual description.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                
                st.subheader(f"Campaign Asset: {selected_medium}")
                st.markdown(response.text)
                
                # Dynamic visual placeholder preview tailored to the product category
                st.divider()
                st.markdown("### 🖼️ Visual Concept Preview")
                formatted_name = product_name.replace(" ", "+")
                st.image(
                    f"https://via.placeholder.com/900x500/111111/FFFFFF?text={formatted_name}+-+{selected_medium.replace(' ', '+')}",
                    caption=f"Concept Mockup for {product_name}"
                )
                
            except Exception as e:
                st.error(f"Error generating strategy: {e}")
else:
    st.info("Fill out your product details in the sidebar, select a medium, and click 'Generate Strategy & Asset'.")
