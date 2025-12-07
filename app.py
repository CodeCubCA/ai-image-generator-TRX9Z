import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image
from io import BytesIO
from datetime import datetime
import random

# Load environment variables
load_dotenv()

# Configuration
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Random creative prompts
RANDOM_PROMPTS = [
    "A cyberpunk city at sunset, neon lights reflecting on wet streets, futuristic skyscrapers",
    "A magical forest with glowing mushrooms, ethereal light, fantasy atmosphere",
    "A cute robot reading a book in a cozy library, warm lighting, detailed illustration",
    "An astronaut riding a horse on Mars, red desert landscape, cinematic",
    "A steampunk airship flying over mountains, Victorian era design, dramatic clouds",
    "A cat wearing a wizard hat casting spells, digital art, magical particles",
    "A futuristic sports car in a neon tunnel, motion blur, cyberpunk aesthetic",
    "A cozy treehouse in autumn, warm lighting, orange and red leaves, peaceful",
    "A dragon sleeping on a pile of ancient books in a library, fantasy art",
    "An underwater city with bioluminescent plants, deep ocean, mysterious atmosphere",
    "A vintage record store on a rainy night, neon sign, nostalgic vibe",
    "A phoenix rising from flames, vibrant colors, epic fantasy scene",
    "A Japanese garden in spring, cherry blossoms, koi pond, serene",
    "A retro diner on Route 66 at golden hour, 1950s style, Americana",
    "A mystical crystal cave with glowing gems, fantasy landscape, ethereal lighting",
    "A floating island in the clouds with waterfalls, fantasy landscape, majestic",
    "A cozy coffee shop in Paris with outdoor seating, romantic evening atmosphere",
    "A medieval knight riding a motorcycle, fantasy meets modern, epic scene",
    "A lighthouse on a cliff during a storm, dramatic waves, moody atmosphere",
    "A bustling alien marketplace with exotic creatures, sci-fi, colorful stalls",
    "A snowy owl flying through a winter forest, magical realism, soft snowfall",
    "A neon-lit ramen shop in Tokyo at night, street photography style, atmospheric",
    "A giant mechanical clock tower in a Victorian city, steampunk, detailed gears",
    "A serene beach at sunrise with palm trees, tropical paradise, peaceful",
    "A mystical witch's cottage in the woods, smoke from chimney, enchanting",
    "A futuristic subway station with holographic ads, cyberpunk, busy commuters",
    "A hot air balloon festival at dawn, colorful balloons, dreamy landscape",
    "A pirate ship sailing through space nebula, fantasy sci-fi, cosmic ocean",
    "A cozy reading nook by a window on a rainy day, warm blankets, books everywhere",
    "A majestic white wolf howling at the full moon, fantasy art, mystical forest",
    "An art deco theater marquee at night, 1920s style, glamorous and elegant",
    "A mystical portal in an ancient temple, glowing runes, adventure scene",
    "A cyberpunk samurai in the rain, neon katana, futuristic Tokyo street",
    "A fairy tale castle on a mountain peak, surrounded by clouds, magical",
    "A vintage bookstore with endless shelves, warm lighting, hidden alcoves",
    "A bioluminescent jellyfish swarm in deep ocean, ethereal glow, underwater beauty",
    "A cozy cabin in snow-covered mountains, smoke from chimney, winter wonderland",
    "A futuristic greenhouse dome on Mars, terraforming, lush plants inside",
    "A mystical deer with glowing antlers in an enchanted forest, magical realism",
    "A 1980s arcade filled with neon lights and retro games, nostalgic atmosphere"
]

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# Title and description
st.title("🎨 AI Image Generator")
st.markdown("Generate stunning images from text descriptions using AI")

# Check if API token is configured
if not HUGGINGFACE_TOKEN:
    st.error("⚠️ HuggingFace API token not found!")
    st.info("""
    **Setup Instructions:**
    1. Go to https://huggingface.co/settings/tokens
    2. Create a new token with 'Write' permissions
    3. Create a `.env` file in the project directory
    4. Add your token: `HUGGINGFACE_TOKEN=your_token_here`
    5. Restart the application
    """)
    st.stop()

# Initialize the HuggingFace Inference Client
@st.cache_resource
def get_inference_client():
    return InferenceClient(token=HUGGINGFACE_TOKEN)

client = get_inference_client()

# Initialize session state for prompt
if 'prompt_text' not in st.session_state:
    st.session_state.prompt_text = ""

# Main interface
st.markdown("---")

# Text input for prompt
prompt = st.text_area(
    "Enter your image description:",
    value=st.session_state.prompt_text,
    placeholder="Example: A serene mountain landscape at sunset with a lake reflection",
    height=100,
    help="Describe the image you want to generate in detail",
    key="prompt_input"
)

# Update session state with current input
st.session_state.prompt_text = prompt

# Negative prompt input
negative_prompt = st.text_input(
    "Negative Prompt (Optional):",
    placeholder="What you DON'T want in the image...",
    help="Tell the AI what to avoid. Examples: 'blurry, low quality, distorted' or 'dark, gloomy, scary' or 'text, watermark, signature'"
)

# Create two columns for buttons
col1, col2 = st.columns([2, 1])

# Random prompt button
with col2:
    if st.button("🎲 Random Prompt", use_container_width=True):
        st.session_state.prompt_text = random.choice(RANDOM_PROMPTS)
        st.rerun()

# Generate button
with col1:
    generate_clicked = st.button("🚀 Generate Image", type="primary", use_container_width=True)

if generate_clicked:
    if not prompt.strip():
        st.warning("Please enter a description for the image.")
    else:
        try:
            # Show loading indicator
            with st.spinner("🎨 Generating your image... This may take a few seconds..."):
                # Generate image using InferenceClient
                # Include negative prompt if provided
                generation_params = {
                    "prompt": prompt,
                    "model": MODEL_NAME
                }

                if negative_prompt.strip():
                    generation_params["negative_prompt"] = negative_prompt

                image = client.text_to_image(**generation_params)

                # Display the generated image
                st.success("✅ Image generated successfully!")
                st.image(image, caption=f"Generated: {prompt}", use_container_width=True)

                # Add download button
                # Convert PIL Image to bytes
                buf = BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()

                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"ai_generated_{timestamp}.png"

                # Create download button
                st.download_button(
                    label="⬇️ Download Image",
                    data=byte_im,
                    file_name=filename,
                    mime="image/png",
                    use_container_width=True
                )

        except Exception as e:
            error_message = str(e)

            # Handle specific error cases
            if "401" in error_message or "authentication" in error_message.lower():
                st.error("❌ Authentication failed. Please check your HuggingFace API token.")
                st.info("Make sure your token has 'Write' permissions or at minimum 'Make calls to the serverless Inference API'")
            elif "429" in error_message or "rate limit" in error_message.lower():
                st.error("❌ Rate limit exceeded. Please wait a moment and try again.")
                st.info("The free tier has rate limits. Consider upgrading your HuggingFace account for higher limits.")
            elif "503" in error_message or "loading" in error_message.lower():
                st.error("❌ Model is currently loading. Please try again in a few seconds.")
            else:
                st.error(f"❌ An error occurred: {error_message}")
                st.info("Try again or consider using a different model.")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown(f"""
    **Current Model:**
    `{MODEL_NAME}`

    **Features:**
    - Fast image generation
    - High-quality results
    - Simple text-to-image conversion

    **Tips for better results:**
    - Be specific and descriptive
    - Include details about style, lighting, and mood
    - Mention colors, composition, and atmosphere
    - Example: "A photorealistic sunset over ocean waves, golden hour lighting, vibrant orange and purple sky"
    """)

    st.markdown("---")
    st.markdown("**Powered by:**")
    st.markdown("- 🤗 HuggingFace Inference API")
    st.markdown("- 🎈 Streamlit")
