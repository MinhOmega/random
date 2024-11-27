"""Module for generating images using Replicate API."""

import logging
from PIL import Image
from io import BytesIO
import requests
import replicate
from .base_image_generator import BaseImageGenerator
from .config import IMAGE_CONFIG

logger = logging.getLogger(__name__)


class ReplicateImageGenerator(BaseImageGenerator):
    """Image generator that uses Replicate API.

    This class implements image generation using the Replicate API
    service for Stable Diffusion.
    """

    def generate_image(self, prompt: str, negative_prompt: str) -> Image.Image:
        """Generate image using Replicate API.

        Args:
            prompt: The text prompt describing the desired image.
            negative_prompt: Text describing what to avoid in the image.

        Returns:
            PIL.Image: The generated image.

        Raises:
            Exception: If image generation fails.
        """
        try:
            output = replicate.run(
                IMAGE_CONFIG["replicate_model"],
                input={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "num_inference_steps": 25,
                    "guidance_scale": 7.0,
                },
            )

            # Download the generated image
            response = requests.get(output[0])
            response.raise_for_status()
            return Image.open(BytesIO(response.content))

        except Exception as e:
            logger.error(f"Replicate generation error: {e}")
            raise
