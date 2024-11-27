"""Configuration settings for image generation.

This module contains configuration settings for different image generation
backends including Stable Diffusion.
"""

MODEL_CONFIG = {
    "model_id": "stabilityai/stable-diffusion-3-medium-diffusers",
    "height": 1024,
    "width": 1024,
    "num_inference_steps": 28,
    "guidance_scale": 7.0,
}
