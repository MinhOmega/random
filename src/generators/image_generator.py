import os
import base64
import logging
from PIL import Image
from io import BytesIO
import requests
import torch
from diffusers import DiffusionPipeline

logger = logging.getLogger(__name__)


class ImageGenerator:
    _pipeline = None  # Class variable to store the model pipeline

    @classmethod
    def _get_pipeline(cls):
        if cls._pipeline is None:
            # Initialize pipeline with better defaults for product images
            cls._pipeline = DiffusionPipeline.from_pretrained(
                "stable-diffusion-v1-5/stable-diffusion-v1-5",
                torch_dtype=(
                    torch.float16 if torch.cuda.is_available() else torch.float32
                ),
                safety_checker=None,  # Disable safety checker for speed
            )

            if torch.cuda.is_available():
                cls._pipeline = cls._pipeline.to("cuda")
                cls._pipeline.enable_attention_slicing()  # For memory efficiency

        return cls._pipeline

    @staticmethod
    def generate_product_image(product_name: str, description: str) -> dict:
        try:
            # Create product directory
            product_dir = os.path.join(
                "products", product_name.replace(" ", "_").lower()
            )
            os.makedirs(product_dir, exist_ok=True)

            try:
                # Enhanced prompt for e-commerce products
                prompt = (
                    f"professional product photography of {product_name}, "
                    f"{description}, centered composition, pure white background, "
                    "studio lighting, high resolution, commercial photography, "
                    "product centered, minimalist, clean, sharp focus, "
                    "high-end commercial product photography"
                )

                # Negative prompt for better results
                negative_prompt = (
                    "text, watermark, logo, blur, duplicate, multiple items, "
                    "distortion, noise, grain, dark, shadows"
                )

                # Generate image with optimized parameters
                pipeline = ImageGenerator._get_pipeline()
                with torch.autocast("cuda" if torch.cuda.is_available() else "cpu"):
                    image = pipeline(
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        num_inference_steps=25,  # Reduced for speed
                        guidance_scale=7.0,
                    ).images[0]

                # Save image
                filename = f"{product_name.replace(' ', '_').lower()}_main.jpg"
                image_path = os.path.join(product_dir, filename)
                image.save(image_path, "JPEG", quality=95)

                logger.info(f"Generated image saved to {image_path}")

                # Convert to base64
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                return {
                    "base64": f"data:image/jpeg;base64,{img_str}",
                    "file_path": image_path,
                }

            except Exception as gen_error:
                logger.error(f"Image generation error: {gen_error}")
                raise

        except Exception as e:
            logger.warning(f"Using placeholder due to error: {str(e)}")
            # Create placeholder
            name = product_name.replace(" ", "+")
            placeholder_url = (
                f"https://placehold.co/1024x1024/FFFFFF/333333/png?" f"text={name}"
            )

            try:
                # Download placeholder
                response = requests.get(placeholder_url)
                response.raise_for_status()

                filename = f"{product_name.replace(' ', '_').lower()}_main.jpg"
                image_path = os.path.join(product_dir, filename)

                img = Image.open(BytesIO(response.content))
                img.save(image_path, "JPEG", quality=95)

                logger.info(f"Saved placeholder to {image_path}")

                return {"base64": None, "file_path": image_path}

            except Exception as placeholder_error:
                logger.error(f"Placeholder error: {placeholder_error}")
                return {"base64": None, "file_path": placeholder_url}
