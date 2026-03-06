import argparse
import os
import sys
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Try to find the project root to load config or .env
current_dir = os.path.dirname(os.path.abspath(__file__))
# Assuming structure: .trae/skills/gemini-image-optimizer/optimize_image.py
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))

# Option 1: Try to import from src.config
try:
    sys.path.append(project_root)
    from src.config import GEMINI_API_KEY
except ImportError:
    # Option 2: Load .env directly if src.config import fails
    env_path = os.path.join(project_root, "sys_init", ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def optimize_image(input_path, output_path, prompt, model_name="gemini-1.5-pro"):
    print(f"Initializing Gemini with model: {model_name}")
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in environment or config.")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return

    try:
        model = genai.GenerativeModel(model_name)
        img = Image.open(input_path)
        
        print(f"Sending request for {input_path}...")
        # Note: This call structure assumes the model supports image-to-image or image-to-text.
        # For actual image generation/editing, the API might differ (e.g. Imagen on Vertex AI).
        # We follow the project's implied pattern here.
        response = model.generate_content([prompt, img])
        
        # Check if response contains image data (hypothetical, depends on model/SDK version)
        if hasattr(response, 'images') and response.images:
            output_img = response.images[0]
            output_img.save(output_path)
            print(f"Successfully saved optimized image to {output_path}")
        elif hasattr(response, 'text'):
            print("Model returned text response instead of image:")
            print(response.text)
            print("Note: The selected Gemini model might be a text-output model. For image generation, ensure you are using a model that supports it (e.g., Imagen).")
        else:
            print("Received response but could not extract image or text.")
            
    except Exception as e:
        print(f"Error during optimization: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize image using Gemini")
    parser.add_argument("--input", required=True, help="Path to input image")
    parser.add_argument("--output", required=True, help="Path to output image")
    parser.add_argument("--prompt", required=True, help="Prompt for optimization")
    parser.add_argument("--model", default="gemini-1.5-pro", help="Gemini model name")
    
    args = parser.parse_args()
    
    optimize_image(args.input, args.output, args.prompt, args.model)
