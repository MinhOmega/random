import json
import random
from faker import Faker

fake = Faker()

# Function to generate a random product
def generate_product(product_id):
    product_name = fake.sentence(nb_words=3).strip(".")
    product_sku = product_name.replace(" ", "_").lower()
    description = fake.paragraph(nb_sentences=5)
    category_ids = random.sample(range(1, 30), random.randint(1, 3))
    price = random.randint(10, 1000) * 1000
    special_price = random.choice([0, price - random.randint(1000, 5000)])
    image_url = f"https://via.placeholder.com/300?text={product_name.replace(' ', '+')}"
    product_type = random.choice(["SIMPLE", "CONFIGURABLE"])

    variations = []
    if product_type == "CONFIGURABLE":
        variations = [
            {
                "attribute_code": "option",
                "attribute_name": "Options",
                "options": [
                    {
                        "attribute_option_code": f"{product_sku}_v{n}",
                        "attribute_option_price": price - random.randint(1000, 5000),
                    }
                    for n in range(1, 6)
                ],
            }
        ]

    return {
        "product_id": product_id,
        "product_name": product_name,
        "product_sku": product_sku,
        "category": category_ids,
        "description": description,
        "short_description": description[:100],
        "price": price,
        "special_price": special_price,
        "image_url": image_url,
        "product_type": product_type,
        "variations": variations,
    }

# Function to generate categories
def generate_categories():
    categories = []
    for category_id in range(1, 11):
        children = [
            {
                "id": category_id * 10 + child_id,
                "name": fake.word().capitalize(),
                "url": fake.url(),
            }
            for child_id in range(1, 4)
        ]
        categories.append(
            {
                "id": category_id,
                "name": fake.word().capitalize(),
                "url": fake.url(),
                "children": children,
            }
        )
    return categories

# Generate the products and categories
def generate_data():
    products = [generate_product(product_id) for product_id in range(1, 101)]
    categories = generate_categories()

    data = {
        "products": products,
        "categories": categories,
    }

    with open("ecommerce_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Data saved to ecommerce_data.json")

if __name__ == "__main__":
    generate_data()
