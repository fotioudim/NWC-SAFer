from enum import Enum

class Product(str, Enum):
    """
    Enum class with all the currently supported
    NWC-SAF products
    """

    CT = "NWC GEO Cloud Type Product"
    CMA = "NWC GEO Cloud Mask Product"


    @staticmethod
    def list():
        """
        Provide an enum list of the currently supported
        NWC-SAF products
        """
        return list(map(lambda c: c.value, Product))