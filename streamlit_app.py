import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64

# 1. Authenticate using the Streamlit Secret
genai.configure(api_key=st.secrets["API_KEY"])

st.set_page_config(page_title="Brand Builder", page_icon="🎨")

st.title("🎨 Brand Builder")
st.markdown("Visualize your product across mediums using Google's Gemini Image Generation.")

# --- Product Definition ---
st.sidebar.header("Product Identity")
product_name = st.sidebar.text_input("Product Name", placeholder="e.g., Onyx Flask")
product_desc = st.sidebar.text_area(
    "Describe the Product (The Anchor)", 
    placeholder="e.g., A sleek, matte-black reusable water bottle with a gold hexagonal cap. No logos."
)

st.sidebar.warning("🚫 Policy: No people will be included in any images.")

if st.sidebar.button("Generate Brand Assets"):
    if not product_desc:
        st.error("Please describe your product first!")
    else:
        # Define the prompts
        mediums = {
            "Outdoor Billboard": f"A massive highway billboard showcasing {product_desc}. Wide angle, shot from below, dramatic blue sky background, cinematic lighting. High resolution, high contrast. No people.",
            "Vintage Newspaper": f"A black and white printed advertisement in a newspaper featuring {product_desc}. Grainy paper texture, halftone dots, elegant typography layout. Product is centered. No people.",
            "Social Media Post": f"A minimalist, trendy Instagram-style product shot of {product_desc}. Placed on a clean marble surface with soft natural sunlight and shadows. 4k, professional photography. No people."
        }

        # 2. Initialize Google's image generation model
        model = genai.GenerativeModel("gemini-2.5-flash-preview-image-generation")

        for medium, prompt in mediums.items():
            with st.container():
                st.subheader(medium)
                st.info(f"**Prompt sent to Gemini:** {prompt}")
                
                with st.spinner(f"Generating {medium} image..."):
                    try:
                        # 3. Request the image from Google
                        response = model.generate_content(
                            prompt,
                            generation_config=genai.GenerationConfig(
                                response_modalities=["image", "text"]
                            )
                        )
                        
                        # 4. Extract and decode the image data
                        img_data = base64.b64decode(response.candidates[0].content.parts[0].inline_data.data)
                        img = Image.open(BytesIO(img_data))
                        
                        # 5. Display the real image on the website
                        st.image(img, caption=f"Visualizing {product_name} as a {medium}")
                        
                    except Exception as e:
                        st.error(f"Error generating image: {e}")
                
                st.divider()
else:
    st.info("Define your product in the sidebar to see it across different mediums.")
