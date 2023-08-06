from faker import Faker

from .models.items import Item


class DummyItemsGenerator:
    def __init__(self, num_items: int):
        self.num_items = num_items
        self.fake = Faker()
        self.names = [
            "Apple",
            "Pear",
            "Lemon",
            "Chair",
            "Window",
            "Door",
            "Computer",
            "Fridge",
        ]
        self.items = []

    def create_items(self):
        for i in range(self.num_items):
            item_attrs = {}
            item_attrs["id"] = i
            item_attrs[
                "name"
            ] = f"{self.fake.color_name()} {self.fake.word(ext_word_list=self.names)}"
            item_attrs["price"] = self.fake.pyfloat(
                min_value=1, max_value=500, right_digits=2
            )
            item_attrs["tax"] = self.fake.pyfloat(
                min_value=0, max_value=0.35, right_digits=2
            )
            item_attrs["description"] = self.fake.sentence(nb_words=5)
            self.items.append(Item(**item_attrs))

        return self.items
