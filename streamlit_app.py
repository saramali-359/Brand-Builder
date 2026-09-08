import streamlit as st

st.set_page_config(page_title="Brand Builder", page_icon="🎨")

st.title("🎨 Brand Builder")
st.markdown("Visualize your product across mediums using the **Nano-Banana** model.")

# --- Step 1: Product Definition ---
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
        # These are the three distinct scenarios
        mediums = {
            "Outdoor Billboard": f"A massive highway billboard showcasing {product_desc}. Wide angle, shot from below, dramatic blue sky background, cinematic lighting. High resolution, high contrast. No people.",
            
            "Vintage Newspaper": f"A black and white printed advertisement in a newspaper featuring {product_desc}. Grainy paper texture, halftone dots, elegant typography layout. Product is centered. No people.",
            
            "Social Media Post": f"A minimalist, trendy Instagram-style product shot of {product_desc}. Placed on a clean marble surface with soft natural sunlight and shadows. 4k, professional photography. No people."
        }

        # Displaying the "Nano-Banana" prompts
        for medium, prompt in mediums.items():
            with st.container():
                st.subheader(medium)
                
                # Logic for the Nano-Banana Model Call
                # In a real app, you would send 'prompt' to the Nano-Banana API here
                st.info(f"**Nano-Banana Prompt:** {prompt}")
                
                # Placeholder for the resulting image
                # Replaced spaces with + for the URL to work correctly
                formatted_name = product_name.replace(" ", "+")
                formatted_medium = medium.replace(" ", "+")
                st.image(f"https://via.placeholder.com/800x400?text={formatted_medium}+Shot+of+{formatted_name}", 
                         caption=f"Visualizing {product_name} as a {medium}")
                st.divider()

else:
    st.info("Define your product in the sidebar to see it across different mediums.")
