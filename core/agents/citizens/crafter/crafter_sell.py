from mesa import Agent

from core.config.global_config import global_var

global_variables = global_var()
location_global_var = global_variables.get('location_items', {})
crafter_global_var = global_variables.get('agent_items', {}).get('crafter', {})


class CrafterSell:
    def need_to_sell(self, crafter):
        if sum(crafter.inventory.values()) <= 0:
            return False

        selling_resources = [
            resource
            for resource, amount in crafter.inventory.items()
            if (
                    resource in crafter_global_var['sell'] and
                    amount > crafter.selling_power.get(resource, 0)
            )
        ]

        if not selling_resources:
            return False
        return selling_resources

    def sell_goods(self, crafter):
        market = crafter.model.city_network.points_of_interest["market"]
        market_goods = location_global_var['market']

        city_center = crafter.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_global_var['city_center']

        selling_resources = self.need_to_sell(crafter)
        if not selling_resources:
            crafter.toggle_mode()
            return

        sell_candidates = []
        for resource in selling_resources:
            current_price = crafter.model.economy.calculate_price(resource)
            sell_candidates.append((resource, current_price))
        sell_candidates.sort(key=lambda x: x[1])

        final_list = []

        for resource, current_price in sell_candidates:
            if sum(crafter.inventory.values()) <= 0:
                break

            if resource in market_goods and crafter.pos != market:
                continue
            if resource in city_center_goods and crafter.pos != city_center:
                continue

            quantity = min(crafter.inventory.get(resource, 0), crafter.selling_power.get(resource, 0))

            if quantity > 0:
                final_list.append((resource, quantity))

        return final_list
