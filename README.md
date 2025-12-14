---
title: AI Image Generator
emoji: 🎨
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: 1.40.0
app_file: app.py
pinned: false
---

# AI Image Generator

A web-based AI image generator powered by HuggingFace's FLUX.1-schnell model and built with Streamlit.

## Features

- Generate stunning images from text descriptions
- Fast image generation using FLUX.1-schnell model
- **Style Presets** - 7 artistic styles: Anime, Realistic, Digital Art, Watercolor, Oil Painting, Cyberpunk, and Fantasy
- **Image History Gallery** - View and manage up to 10 previously generated images
- Clean and intuitive user interface
- Download generated images
- Comprehensive error handling
- Built-in usage tips and example prompts

## Prerequisites

- Python 3.8 or higher
- HuggingFace account with API token (with Write permissions)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/CodeCubCA/ai-image-generator-Alex-CodeCub.git
cd ai-image-generator
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your HuggingFace API token:
   - Go to https://huggingface.co/settings/tokens
   - Create a new token with **Write** permissions
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your token:
     ```
     HUGGINGFACE_TOKEN=your_token_here
     ```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to:
   - Local: http://localhost:8501
   - Network: http://192.168.1.92:8501

3. Enter a description of the image you want to generate

4. Click "Generate Image" and wait for the AI to create your image

5. Download your generated image using the download button

## Example Prompts

- "A serene lake at sunset, oil painting style, warm colors"
- "A futuristic city at night, cyberpunk style, neon lights"
- "A cute cat wearing a wizard hat, digital art, detailed"
- "Mountain landscape with aurora borealis, photorealistic"

## Style Presets

Choose from 7 built-in style presets to enhance your prompts:

| Style | Description |
|-------|-------------|
| None | Use your original prompt as-is |
| Anime | Studio Ghibli inspired, vibrant colors |
| Realistic | Photorealistic, 8K resolution |
| Digital Art | Artstation trending, concept art |
| Watercolor | Soft colors, delicate brushstrokes |
| Oil Painting | Classical art, textured canvas |
| Cyberpunk | Neon lights, futuristic sci-fi |
| Fantasy | Magical, enchanted, epic scenes |

## Tips for Better Results

- Be specific and descriptive in your prompts
- Use style presets for consistent artistic results
- Include mood and atmosphere details
- Mention lighting and colors

## Project Structure

```
ai-image-generator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Dependencies

- `streamlit` - Web framework for the UI
- `huggingface_hub` - Official HuggingFace API client
- `python-dotenv` - Environment variable management
- `Pillow` - Image processing library

## Technical Details

### Model
- **FLUX.1-schnell** by Black Forest Labs
- Fast, high-quality image generation
- Publicly accessible via HuggingFace Inference API

### API
- Uses HuggingFace's `InferenceClient` from `huggingface_hub`
- Serverless inference for zero infrastructure management
- Automatic endpoint routing and error handling

## Limitations

- Free tier has rate limits
- Image generation may take 10-30 seconds
- Model needs to load on first request (cold start)

## Troubleshooting

### Authentication Error (401)
- Ensure your HuggingFace token has **Write** permissions
- Check that the token is correctly set in the `.env` file

### Rate Limit Error (429)
- Wait a few minutes before trying again
- Consider upgrading to HuggingFace PRO for higher limits

### Model Loading Error (503)
- Wait a moment and try again
- The model may be loading (cold start)

## License

This project is created for educational purposes.

## Acknowledgments

- HuggingFace for providing the Inference API
- Black Forest Labs for the FLUX.1-schnell model
- Streamlit for the web framework

## Author

Created as part of CodeCub's AI/ML course assignment.
