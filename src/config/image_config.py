import os
from dotenv import load_dotenv

load_dotenv()

# Image generation configuration
IMAGE_CONFIG = {
    "generator_type": os.getenv("IMAGE_GENERATOR_TYPE", "local"),  # "local" or "replicate"
    "replicate_model": os.getenv("REPLICATE_MODEL", "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478"),
    "replicate_api_token": os.getenv("REPLICATE_API_TOKEN", ""),
} 