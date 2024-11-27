from faker import Faker

fake = Faker()

class CategoryGenerator:
    @staticmethod
    def generate_categories() -> list:
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
            
            categories.append({
                "id": category_id,
                "name": fake.word().capitalize(),
                "url": fake.url(),
                "children": children,
            })
        return categories 