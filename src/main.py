import json
import logging
from generators.product_generator import ProductGenerator
from generators.category_generator import CategoryGenerator
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def generate_data():
    # Log API key (masked for security)
    api_key = os.getenv("GEMINI_API_KEY", "")
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "Not found"
    logger.debug(f"Using Gemini API Key: {masked_key}")

    # Generate only 3 products for testing
    products = [
        ProductGenerator.generate_product(product_id)
        for product_id in range(1, 4)  # Changed to generate only 3 products
    ]

    # Generate categories
    categories = CategoryGenerator.generate_categories()

    # Combine data
    data = {
        "products": products,
        "categories": categories,
    }

    # Save to file
    with open("ecommerce_data.json", "w") as f:
        json.dump(data, f, indent=4)
    logger.info("Data saved to ecommerce_data.json")


if __name__ == "__main__":
    generate_data()
