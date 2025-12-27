class FarmerSell:
    def __init__(self, farmer):
        self.farmer = farmer

    def sell_goods(self):
        resource = 'food'
        resource_amount = self.farmer.inventory.get(resource, 0)

        sellable_amount = max(0, resource_amount - self.farmer.personal_minimum)

        if sellable_amount <= 0:
            return None

        current_price = self.farmer.model.economy.current_price(resource)
        base_price = self.farmer.model.economy.base_prices.get(resource, 0)
        price_threshold = base_price * self.farmer.selling_power.get(resource, 1)

        if current_price >= price_threshold:
            return [(resource, round(sellable_amount * self.farmer.selling_cap, 3))]

        if sellable_amount >= self.farmer.selling_margin:
            return [(resource, round(sellable_amount * self.farmer.selling_cap, 3))]

        return None
