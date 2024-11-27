"""Factory module for creating image generators."""

from .huggingface_image_generator import HuggingFaceImageGenerator
from .base_image_generator import BaseImageGenerator


def create_image_generator() -> BaseImageGenerator:
    """Create and return appropriate image generator instance.

    Returns:
        BaseImageGenerator: Instance of image generator.
    """
    return HuggingFaceImageGenerator()
