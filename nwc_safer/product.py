from enum import Enum

class Product(str, Enum):
    CT = "NWC GEO Cloud Type Product"
    CMA = "NWC GEO Cloud Mask Product"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Product))