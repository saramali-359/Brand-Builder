import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# 1. Authenticate using the Streamlit Secret
client = genai.Client(api_key=st.secrets["API_KEY"])

st.set_page_config(page_title="Brand Builder", page_icon="🎨")

st.title("🎨 Brand Builder")
st.markdown("Visualize your product across mediums using Google Gemini.")

# --- Product Definition ---
st.sidebar.header("Product Identity")
product_name = st.sidebar.text_input("Product Name", placeholder="e.g., Onyx Flask")
product_desc = st.sidebar.text_area(
    "Describe the Product (The Anchor)", 
    placeholder="e.g., A sleek, matte-black reusable water bottle with a gold hexagonal cap. No logos."
)

st.sidebar.warning("🚫 Policy: No people will be included in any images.")

# Choose a single medium to generate at a time to stay safely within free quotas
selected_medium = st.selectbox(
    "Select Marketing Medium to Generate:",
    ["Outdoor Billboard", "Vintage Newspaper", "Social Media Post"]
)

if st.button("Generate Asset"):
    if not product_desc:
        st.error("Please describe your product first in the sidebar!")
    else:
        # Define the targeted prompts
        mediums_dict = {
            "Outdoor Billboard": f"A massive highway billboard showcasing {product_desc}. Wide angle, shot from below, dramatic blue sky background, cinematic lighting. High resolution, high contrast. No people.",
            "Vintage Newspaper": f"A black and white printed advertisement in a newspaper featuring {product_desc}. Grainy paper texture, halftone dots, elegant typography layout. Product is centered. No people.",
            "Social Media Post": f"A minimalist, trendy Instagram-style product shot of {product_desc}. Placed on a clean marble surface with soft natural sunlight and shadows. 4k, professional photography. No people."
        }

        prompt = mediums_dict[selected_medium]

        st.subheader(selected_medium)
        st.info(f"**Prompt sent to Gemini:** {prompt}")
        
        with st.spinner(f"Generating your {selected_medium} asset..."):
            try:
                # Use the stable free-tier image generation model ID
                response = client.models.generate_content(
                    model='gemini-2.5-flash-image',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"]
                    )
                )
                
                # Extract the image bytes from the response parts
                image_found = False
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        image_bytes = part.inline_data.data
                        img = Image.open(BytesIO(image_bytes))
                        st.image(img, caption=f"Visualizing {product_name} as a {selected_medium}")
                        image_found = True
                        break
                
                if not image_found:
                    st.warning("The model returned text instead of an image.")
                    if response.text:
                        st.write(response.text)
                
            except Exception as e:
                st.error(f"Error generating image: {e}")
else:
    st.info("Select a medium and click 'Generate Asset' to create your marketing visual.")
