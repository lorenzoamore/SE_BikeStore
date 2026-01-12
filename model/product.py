from dataclasses import dataclass


@dataclass
class Product:
    id: int
    product_name: str
    category_id : int
    vendite : int


    def __str__(self):
        return (f"{self.product_name}")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id