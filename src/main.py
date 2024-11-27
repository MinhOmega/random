"""Main module for generating e-commerce data.

This module handles the generation of product and category data,
combining them into a JSON file for use in an e-commerce system.
"""

import json
import logging
import os
from generators.product_generator import ProductGenerator
from generators.category_generator import CategoryGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def generate_data() -> None:
    """Generate product and category data and save to JSON file.

    This function:
    1. Creates product data using ProductGenerator
    2. Creates category data using CategoryGenerator
    3. Combines the data and saves it to a JSON file
    """
    # Log API key (masked for security)
    api_key = os.getenv("GEMINI_API_KEY", "")
    masked_key = (
        f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "Not found"
    )
    logger.debug(f"Using Gemini API Key: {masked_key}")

    # Create product generator instance
    product_generator = ProductGenerator()

    # Generate only 3 products for testing
    products = [
        product_generator.generate_product(product_id)
        for product_id in range(1, 4)
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
