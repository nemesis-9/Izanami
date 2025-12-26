from core.config.global_config import GlobalConfig

global_config = GlobalConfig().get()
location_config = global_config.location_item_list()
crafter_config = global_config.agent_item_list('crafter')


class CrafterSell:
    def __init__(self, crafter):
        self.crafter = crafter

    def need_to_sell(self):
        if sum(self.crafter.inventory.values()) <= 0:
            return False

        selling_resources = [
            resource
            for resource, amount in self.crafter.inventory.items()
            if (
                    resource in crafter_config['sell'] and
                    amount > self.crafter.selling_power.get(resource, 0)
            )
        ]

        return selling_resources or False

    def sell_goods(self):

        selling_resources = self.need_to_sell()
        if not selling_resources:
            return None

        market = self.crafter.model.city_network.points_of_interest["market"]
        market_goods = location_config['market']

        city_center = self.crafter.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_config['city_center']

        sell_candidates = []
        for resource in selling_resources:
            current_price = self.crafter.model.economy.calculate_price(resource)
            sell_candidates.append((resource, current_price))

        sell_candidates.sort(key=lambda x: x[1], reverse=True)

        final_list = []
        for resource, current_price in sell_candidates:
            if (
                    (self.crafter.pos == city_center and resource not in city_center_goods)
                    or (self.crafter.pos == market and resource not in market_goods)
            ):
                continue

            excess = (
                    self.crafter.inventory.get(resource, 0)
                    - self.crafter.selling_power.get(resource, 0)
            )

            quantity = max(0, excess)

            if quantity > 0:
                final_list.append((resource, quantity))

        return final_list or None
