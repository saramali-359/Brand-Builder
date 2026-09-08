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

if st.sidebar.button("Generate Brand Assets"):
    if not product_desc:
        st.error("Please describe your product first initials!")
    else:
        # Define the prompts
        mediums = {
            "Outdoor Billboard": f"A massive highway billboard showcasing {product_desc}. Wide angle, shot from below, dramatic blue sky background, cinematic lighting. High resolution, high contrast. No people.",
            "Vintage Newspaper": f"A black and white printed advertisement in a newspaper featuring {product_desc}. Grainy paper texture, halftone dots, elegant typography layout. Product is centered. No people.",
            "Social Media Post": f"A minimalist, trendy Instagram-style product shot of {product_desc}. Placed on a clean marble surface with soft natural sunlight and shadows. 4k, professional photography. No people."
        }

        for medium, prompt in mediums.items():
            with st.container():
                st.subheader(medium)
                st.info(f"**Prompt sent to Gemini:** {prompt}")
                
                with st.spinner(f"Generating {medium} image..."):
                    try:
                        # Use Gemini Flash to generate the image content directly
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
                                st.image(img, caption=f"Visualizing {product_name} as a {medium}")
                                image_found = True
                                break
                        
                        if not image_found:
                            st.warning("The model returned text instead of an image. Try tweaking the prompt slightly.")
                            if response.text:
                                st.write(response.text)
                        
                    except Exception as e:
                        st.error(f"Error generating image: {e}")
                
                st.divider()
else:
    st.info("Define your product in the sidebar to see it across different mediums.")
