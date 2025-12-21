import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Configuration
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_NAME = "stabilityai/stable-diffusion-xl-base-1.0"

# Style presets
STYLE_PRESETS = {
    "None": "",
    "Anime": ", anime style, vibrant colors, Studio Ghibli inspired, detailed illustration",
    "Realistic": ", photorealistic, highly detailed, 8K resolution, professional photography",
    "Digital Art": ", digital painting, artstation trending, concept art, highly detailed",
    "Watercolor": ", watercolor painting, soft colors, artistic, delicate brushstrokes",
    "Oil Painting": ", oil painting, classical art style, textured canvas, rich colors",
    "Cyberpunk": ", cyberpunk style, neon lights, futuristic, sci-fi, dark atmosphere",
    "Fantasy": ", fantasy art, magical, enchanted, epic scene, mystical atmosphere",
}

# Initialize InferenceClient
client = InferenceClient(token=HUGGINGFACE_TOKEN)

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

def generate_image(prompt):
    """
    Generate an image using HuggingFace InferenceClient

    Args:
        prompt (str): Text description of the image to generate

    Returns:
        PIL.Image: Generated image or None if failed
    """
    try:
        # Use InferenceClient's text_to_image method
        image = client.text_to_image(prompt, model=MODEL_NAME)
        return image
    except Exception as e:
        error_msg = str(e)

        # Handle specific error cases
        if "503" in error_msg or "loading" in error_msg.lower():
            st.error("⏳ Model is currently loading. Please wait a moment and try again.")
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            st.error("⚠️ Rate limit reached. Please wait a few minutes before trying again.")
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            st.error("🔒 Authentication failed. Please check your HuggingFace token has 'Write' permissions.")
        else:
            st.error(f"❌ An error occurred: {error_msg}")

        return None

def main():
    # Initialize session state for image history
    if 'image_history' not in st.session_state:
        st.session_state.image_history = []

    # Header
    st.title("🎨 AI Image Generator")
    st.markdown("Generate stunning images from text using AI powered by Stable Diffusion XL")

    # Check if API token is configured
    if not HUGGINGFACE_TOKEN:
        st.error("⚠️ HuggingFace API token not found!")
        st.info("""
        **Setup Instructions:**
        1. Go to https://huggingface.co/settings/tokens
        2. Create a new token with 'Write' permissions
        3. Add it to the `.env` file as: `HUGGINGFACE_TOKEN=your_token_here`
        """)
        st.stop()

    # Sidebar with information
    with st.sidebar:
        st.header("🎨 Style Preset")
        selected_style = st.selectbox(
            "Choose a style:",
            options=list(STYLE_PRESETS.keys()),
            index=0,
            help="Select a style to automatically enhance your prompt"
        )

        # Show what the style adds
        if selected_style != "None":
            st.info(f"**Style adds:** {STYLE_PRESETS[selected_style]}")

        st.markdown("---")

        st.header("ℹ️ About")
        st.write(f"**Model:** {MODEL_NAME}")
        st.write("Stable Diffusion XL is a high-quality image generation model by Stability AI.")

        st.markdown("---")

        st.header("💡 Tips for Better Results")
        st.write("- Be specific and descriptive")
        st.write("- Include style, mood, and details")
        st.write("- Mention lighting and colors")
        st.write("- Or use a style preset above!")

        st.markdown("---")

        st.header("📝 Example Prompts")
        st.code("A serene lake at sunset")
        st.code("A futuristic city at night")
        st.code("A cute cat wearing a wizard hat")
        st.code("Mountain landscape with aurora borealis")

        st.markdown("---")

        st.info("**Note:** Free tier has rate limits. If you encounter errors, wait a few minutes.")

    # Main content area
    st.markdown("---")

    # Input section
    prompt = st.text_area(
        "✍️ Enter your image description:",
        placeholder="Example: A magical forest with glowing mushrooms, fantasy art style, vibrant colors",
        height=120,
        help="Describe the image you want to generate. Be as detailed as possible!"
    )

    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("🚀 Generate Image", use_container_width=True, type="primary")

    # Generation logic
    if generate_button:
        if not prompt.strip():
            st.warning("⚠️ Please enter a description for your image.")
        else:
            # Combine prompt with style
            style_suffix = STYLE_PRESETS[selected_style]
            enhanced_prompt = prompt.strip() + style_suffix

            # Show the enhanced prompt if a style is applied
            if selected_style != "None":
                with st.expander("🔍 View Enhanced Prompt", expanded=False):
                    st.code(enhanced_prompt)

            with st.spinner("🎨 Creating your image... This may take 10-30 seconds..."):
                image = generate_image(enhanced_prompt)

                if image:
                    st.success("✅ Image generated successfully!")

                    # Save to history
                    image_data = {
                        'image': image,
                        'prompt': prompt.strip(),
                        'enhanced_prompt': enhanced_prompt,
                        'style': selected_style,
                        'timestamp': datetime.now()
                    }
                    st.session_state.image_history.insert(0, image_data)

                    # Limit to 10 images
                    if len(st.session_state.image_history) > 10:
                        st.session_state.image_history = st.session_state.image_history[:10]

                    # Display the generated image
                    caption = f"{prompt}" if selected_style == "None" else f"{prompt} ({selected_style} style)"
                    st.image(image, caption=caption, use_container_width=True)

                    # Download button
                    buf = BytesIO()
                    image.save(buf, format="PNG")
                    byte_im = buf.getvalue()

                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="⬇️ Download Image",
                            data=byte_im,
                            file_name=f"ai_generated_{prompt[:30].replace(' ', '_')}.png",
                            mime="image/png",
                            use_container_width=True
                        )

    # Image History Gallery
    if st.session_state.image_history:
        st.markdown("---")
        st.header(f"🖼️ Image History ({len(st.session_state.image_history)}/10)")

        # Clear history button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col3:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.image_history = []
                st.rerun()

        # Display images in a grid (3 columns)
        cols = st.columns(3)
        for idx, img_data in enumerate(st.session_state.image_history):
            with cols[idx % 3]:
                # Display image
                st.image(img_data['image'], use_container_width=True)

                # Show style badge
                style_text = f"**{img_data['style']}**" if img_data['style'] != "None" else "No style"
                st.caption(style_text)

                # Show prompt in expander
                with st.expander("View prompt", expanded=False):
                    st.write(img_data['prompt'])
                    if img_data['style'] != "None":
                        st.caption(f"Enhanced: {img_data['enhanced_prompt']}")

                # Download button for each image
                buf = BytesIO()
                img_data['image'].save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.download_button(
                    label="⬇️ Download",
                    data=byte_im,
                    file_name=f"ai_generated_{img_data['prompt'][:20].replace(' ', '_')}_{idx}.png",
                    mime="image/png",
                    use_container_width=True,
                    key=f"download_{idx}"
                )

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>Built with ❤️ using Streamlit & HuggingFace Stable Diffusion XL</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
