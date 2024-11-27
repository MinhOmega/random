"""Module for generating images using Hugging Face's Diffusers library."""

import logging
import torch
from PIL import Image
from diffusers import StableDiffusion3Pipeline
from .base_image_generator import BaseImageGenerator

logger = logging.getLogger(__name__)


class HuggingFaceImageGenerator(BaseImageGenerator):
    """Image generator that uses Hugging Face's Diffusers library.

    This class implements image generation using Stable Diffusion 3
    running locally through the Hugging Face Diffusers library.
    """

    _pipeline = None

    def _get_pipeline(self):
        """Initialize and return the Stable Diffusion pipeline.

        Returns:
            StableDiffusion3Pipeline: Configured pipeline instance.
        """
        if self._pipeline is None:
            # Initialize pipeline with better defaults for product images
            device = "cuda" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if device == "cuda" else torch.float32

            self._pipeline = StableDiffusion3Pipeline.from_pretrained(
                "stabilityai/stable-diffusion-3-medium-diffusers",
                torch_dtype=torch_dtype,
                safety_checker=None,  # Disable safety checker for speed
            )

            if device == "cuda":
                self._pipeline = self._pipeline.to(device)
                # For memory efficiency
                self._pipeline.enable_attention_slicing()

        return self._pipeline

    def generate_image(self, prompt: str, negative_prompt: str) -> Image.Image:
        """Generate image using local Stable Diffusion 3.

        Args:
            prompt: The text prompt describing the desired image.
            negative_prompt: Text describing what to avoid in the image.

        Returns:
            PIL.Image: The generated image.

        Raises:
            Exception: If image generation fails.
        """
        try:
            pipeline = self._get_pipeline()
            device = "cuda" if torch.cuda.is_available() else "cpu"

            with torch.autocast(device):
                image = pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=28,
                    height=1024,
                    width=1024,
                    guidance_scale=7.0,
                ).images[0]

            return image

        except Exception as e:
            logger.error(f"Stable Diffusion generation error: {e}")
            raise
