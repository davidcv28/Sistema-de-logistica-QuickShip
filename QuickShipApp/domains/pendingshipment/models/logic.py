from QuickShipApp.domains.prices.models.models import PriceBase
from decimal import Decimal
"""

Este módulo contiene funciones privadas pertenecientes al módulo pendingshipmentmodels.py

"""
######CALCULATE PRICES CLASS
class CalculatePrices:
    def __init__(self):
        try:
            self.price_obj = PriceBase.objects.latest('id')
            self.shipmentprice = Decimal(str(self.price_obj.shipment_price or 0))
            self.weightprice = Decimal(str(self.price_obj.weight_price or 0))
            self.divider = Decimal(str(self.price_obj.volumetric_divider or 1)) 
        except PriceBase.DoesNotExist:
            self.price_obj = None
            self.shipmentprice =  0
            self.weightprice = 0
            self.divider =  1  

    def calculate(self):
        return self.shipmentprice
######CALCULATE WEIGHT_PRICE
class CalculateWeightPrice(CalculatePrices):
    def __init__(self, weight, height, length, width):
        super().__init__()
        self.weight = Decimal(str(weight or 0))
        self.height = Decimal(str(height or 0))
        self.length = Decimal(str(length or 0))
        self.width = Decimal(str(width or 0))    
    def calculate(self):
        volumetric_weight = (self.height * self.length * self.width) / self.divider
        total_weight = max(self.weight, volumetric_weight)
        total_weight_price = total_weight * self.weightprice
        return round(total_weight_price,2)
######CALCULATE TOTALs
class CalculateSubTotal(CalculatePrices):
    def __init__(self, weight,height, length, width, quantity):
        super().__init__()
        self.weight = Decimal(str(weight or 0))
        self.height = Decimal(str(height or 0))
        self.length = Decimal(str(length or 0))
        self.width = Decimal(str(width or 0))
        self.quantity = quantity or 1

    def calculate(self):

        volumetric_weight = (self.height * self.length * self.width) / self.divider 
        total_volumetric_weight = max(self.weight, volumetric_weight)
        total_weight_price = (total_volumetric_weight * self.weightprice) * self.quantity
        return round(total_weight_price, 2)


#####CALCULATE TOTAL_PRICE
class CalculateTotalPrice(CalculatePrices):
    def __init__(self,details):
        super().__init__()
        self.details = details
    
    def calculate(self):
        try:
            total_price = sum(self.details) + Decimal(str(self.shipmentprice))
            return round(Decimal(total_price), 2)
        except(TypeError,ValueError):
            raise TypeError('Solo se admiten números para calcular el total de precio')
