class AgroSell:
    def __init__(self, agro):
        self.agro = agro

    def sell_goods(self):
        resource = 'food'
        resource_amount = self.agro.inventory.get(resource, 0)

        sellable_amount = max(0, resource_amount - self.agro.personal_minimum)

        if sellable_amount <= 0:
            return None

        current_price = self.agro.model.economy.current_price(resource)
        base_price = self.agro.model.economy.base_prices.get('food', 0)
        price_threshold = base_price * self.agro.selling_power.get('food', 1)

        if self.agro.is_emergency:
            return [(resource, sellable_amount)]

        if current_price >= price_threshold:
            return [(resource, round(sellable_amount * self.agro.selling_cap, 3))]

        if sellable_amount >= self.agro.selling_margin:
            return [(resource, round(sellable_amount * self.agro.selling_cap, 3))]

        return None
