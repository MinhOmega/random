"""Module for generating images using local Stable Diffusion pipeline."""

import logging
import torch
from PIL import Image
from diffusers import DiffusionPipeline
from .base_image_generator import BaseImageGenerator

logger = logging.getLogger(__name__)


class LocalImageGenerator(BaseImageGenerator):
    """Image generator that uses local Stable Diffusion pipeline.

    This class implements image generation using a local installation
    of the Stable Diffusion model, optimized for product photography.
    """

    _pipeline = None

    def _get_pipeline(self):
        """Initialize and return the Stable Diffusion pipeline.

        Returns:
            DiffusionPipeline: Configured pipeline instance.
        """
        if self._pipeline is None:
            # Initialize pipeline with better defaults for product images
            torch_dtype = (
                torch.float16 if torch.cuda.is_available() else torch.float32
            )

            self._pipeline = DiffusionPipeline.from_pretrained(
                "stable-diffusion-v1-5/stable-diffusion-v1-5",
                torch_dtype=torch_dtype,
                safety_checker=None,  # Disable safety checker for speed
            )

            if torch.cuda.is_available():
                self._pipeline = self._pipeline.to("cuda")
                # For memory efficiency
                self._pipeline.enable_attention_slicing()

        return self._pipeline

    def generate_image(self, prompt: str, negative_prompt: str) -> Image.Image:
        """Generate image using local pipeline.

        Args:
            prompt: The text prompt describing the desired image.
            negative_prompt: Text describing what to avoid in the image.

        Returns:
            PIL.Image: The generated image.
        """
        pipeline = self._get_pipeline()
        device = "cuda" if torch.cuda.is_available() else "cpu"

        with torch.autocast(device):
            image = pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=25,
                guidance_scale=7.0,
            ).images[0]
        return image
