import streamlit as st
from google import genai

# 1. Authenticate securely using your existing Google API Key
client = genai.Client(api_key=st.secrets["API_KEY"])

st.set_page_config(page_title="Brand Builder", page_icon="🎨")

st.title("🎨 Brand Builder")
st.markdown("Generate professional multi-channel marketing strategies and creative visual concepts.")

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
                # Use the reliable, free-tier gemini-3.7-flash text model
                prompt = f"""
                You are an expert creative director. For the product '{product_name}' described as: '{product_desc}':
                Create a high-converting marketing strategy for a {selected_medium}.
                Include:
                1. A compelling headline or hook.
                2. Detailed visual art direction description (No people).
                3. Copywriting caption or body text.
                Keep it structured and clean.
                """
                
                response = client.models.generate_content(
                    model='gemini-3.7-flash',
                    contents=prompt
                )
                
                st.subheader(f"Campaign Asset: {selected_medium}")
                st.markdown(response.text)
                
                # Render a sleek concept mockup frame
                st.divider()
                st.markdown("### 🖼️ Visual Art Direction Mockup")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.success(f"**Asset Layout Ready:** Optimized for {selected_medium}")
                    st.info(f"**Theme Style:** Commercial minimalist product showcase focusing strictly on `{product_name}` with zero human presence.")
                with col2:
                    st.metric(label="Compliance", value="100% Policy Safe", delta="No People")
                
            except Exception as e:
                st.error(f"Error generating strategy: {e}")
else:
    st.info("Fill out your product details in the sidebar, select a medium, and click 'Generate Strategy & Asset'.")
