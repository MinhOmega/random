"""Module for generating category data.

This module provides functionality to generate fake category data
for an e-commerce system, including parent categories and their children.
"""

from faker import Faker

fake = Faker()


class CategoryGenerator:
    """Class for generating category data.

    This class provides methods to generate a hierarchical category structure
    with parent categories and child subcategories.
    """

    @staticmethod
    def generate_categories() -> list:
        """Generate a list of categories with child subcategories.

        Returns:
            list: A list of dictionaries containing category data.
                Each category has:
                - id: Unique identifier
                - name: Category name
                - url: Category URL
                - children: List of child subcategories
        """
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
