import random
from faker import Faker
from .image_generator import ImageGenerator

fake = Faker()


class ProductGenerator:
    @staticmethod
    def generate_product(product_id: int) -> dict:
        product_name = fake.sentence(nb_words=3).strip(".")
        product_sku = product_name.replace(" ", "_").lower()
        description = fake.paragraph(nb_sentences=5)

        # Generate image using Gemini
        image_result = ImageGenerator.generate_product_image(product_name, description)

        product_data = {
            "product_id": product_id,
            "product_name": product_name,
            "product_sku": product_sku,
            "category": random.sample(range(1, 30), random.randint(1, 3)),
            "description": description,
            "short_description": description[:100],
            "price": random.randint(10, 1000) * 1000,
            "special_price": 0,  # Will be updated below
            "image_url": image_result["file_path"],
            "image_base64": image_result["base64"],
            "product_type": random.choice(["SIMPLE", "CONFIGURABLE"]),
            "variations": [],
        }

        # Set special price
        product_data["special_price"] = random.choice(
            [0, product_data["price"] - random.randint(1000, 5000)]
        )

        # Add variations if configurable
        if product_data["product_type"] == "CONFIGURABLE":
            product_data["variations"] = ProductGenerator._generate_variations(
                product_sku, product_data["price"]
            )

        return product_data

    @staticmethod
    def _generate_variations(product_sku: str, base_price: int) -> list:
        return [
            {
                "attribute_code": "option",
                "attribute_name": "Options",
                "options": [
                    {
                        "attribute_option_code": f"{product_sku}_v{n}",
                        "attribute_option_price": base_price
                        - random.randint(1000, 5000),
                    }
                    for n in range(1, 6)
                ],
            }
        ]
