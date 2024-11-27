"""Base module for image generation implementations.

This module provides the abstract base class for different image generation
backends. It defines the common interface and shared functionality for
generating product images.
"""

import abc
import os
import base64
import logging
import requests
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)


class BaseImageGenerator(abc.ABC):
    """Abstract base class for image generators.

    This class defines the interface for image generation and provides
    common functionality for handling product images, including error
    handling and file management.
    """

    @abc.abstractmethod
    def generate_image(self, prompt: str, negative_prompt: str) -> Image.Image:
        """Generate image using the specific implementation.

        Args:
            prompt: The text prompt describing the desired image.
            negative_prompt: Text describing what to avoid in the image.

        Returns:
            PIL.Image: The generated image.

        Raises:
            NotImplementedError: If the subclass doesn't implement this method.
        """
        pass

    def generate_product_image(
        self, product_name: str, description: str
    ) -> dict:
        """Generate and save a product image.

        Args:
            product_name: Name of the product.
            description: Description of the product.

        Returns:
            dict: Contains base64 encoded image and file path.
                Keys:
                - base64: Base64 encoded image string
                - file_path: Path where the image is saved

        Raises:
            Exception: If image generation or saving fails.
        """
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
                    f"{description}, centered composition, "
                    "pure white background, studio lighting, "
                    "high resolution, commercial photography, "
                    "product centered, minimalist, clean, sharp focus, "
                    "high-end commercial product photography"
                )

                # Negative prompt for better results
                negative_prompt = (
                    "text, watermark, logo, blur, duplicate, "
                    "multiple items, distortion, noise, grain, "
                    "dark, shadows"
                )

                # Generate image using specific implementation
                image = self.generate_image(prompt, negative_prompt)

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
            return self._handle_error(e, product_name, product_dir)

    def _handle_error(
        self, error: Exception, product_name: str, product_dir: str
    ) -> dict:
        """Handle errors by creating a placeholder image.

        Args:
            error: The exception that occurred.
            product_name: Name of the product.
            product_dir: Directory for the product files.

        Returns:
            dict: Contains placeholder image information.
                Keys:
                - base64: None
                - file_path: Path to placeholder image
        """
        logger.warning(f"Using placeholder due to error: {str(error)}")
        name = product_name.replace(" ", "+")
        placeholder_url = (
            "https://placehold.co/1024x1024/FFFFFF/333333/png?" f"text={name}"
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
