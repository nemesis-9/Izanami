from core.config.global_config import GlobalConfig

global_config = GlobalConfig().get()
crafter_config = global_config.agent_item_list('crafter')
items_config = global_config.items


class CrafterCraft:
    def __init__(self, crafter):
        self.crafter = crafter

    def can_craft_anything(self):
        for item_name, item_details in items_config.items():
            if item_name not in crafter_config['sell']:
                continue

            mats = item_details.get('crafting_material', {})
            if all(self.crafter.inventory.get(m, 0) >= qty for m, qty in mats.items()):
                return True

        return False

    def craft(self):
        if not self.can_craft_anything():
            return None

        space_left = self.crafter.max_inventory - sum(self.crafter.inventory.values())
        if space_left <= 0:
            return None

        craftable = {}

        for item, details in items_config.items():
            if item not in crafter_config['sell']:
                continue

            mats = details.get('crafting_material', {})
            max_crafts = min(
                self.crafter.inventory.get(m, 0) // q
                for m, q in mats.items()
            )

            if max_crafts > 0:
                profit = (
                    self.crafter.model.economy.calculate_price(item) -
                    sum(
                        q * self.crafter.model.economy.calculate_price(m)
                        for m, q in mats.items()
                    )
                )
                craftable[item] = (profit, max_crafts, mats)

        if not craftable:
            return None

        item, (profit, max_crafts, mats) = max(craftable.items(), key=lambda x: x[1][0])
        qty = min(max_crafts, space_left)

        for mat, q in mats.items():
            self.crafter.inventory[mat] -= q * qty

        self.crafter.inventory[item] = self.crafter.inventory.get(item, 0) + qty
        return item, qty

    # def perform_craft(self, item_name, quantity, materials_used):
    #     max_possible = self.crafter.max_inventory - sum(self.crafter.inventory.values())
    #     actual_quantity = min(quantity, max_possible)
    #     if actual_quantity <= 0:
    #         return
    #
    #     for material, required_qty in materials_used.items():
    #         self.crafter.inventory[material] -= required_qty * actual_quantity
    #
    #     self.crafter.inventory[item_name] = self.crafter.inventory.get(item_name, 0) + actual_quantity
    #
    #     if sum(self.crafter.inventory.values()) >= self.crafter.max_inventory * self.crafter.inventory_margin:
    #         self.crafter.mode = 'selling'
    #
    # def craft_optimized(self):
    #     craftable_items = {}
    #     for item_name, item_details in items_config.items():
    #         if item_name not in crafter_config['sell']:
    #             continue
    #
    #         required_materials = item_details.get('crafting_material', {})
    #         max_crafts = float('inf')
    #         can_craft = True
    #
    #         for material, required_quantity in required_materials.items():
    #             available_qty = self.crafter.inventory.get(material, 0)
    #             if available_qty < required_quantity:
    #                 can_craft = False
    #                 break
    #
    #             max_crafts = min(max_crafts, available_qty // required_quantity)
    #
    #         if can_craft and max_crafts > 0:
    #             craftable_items[item_name] = {'max_crafts': max_crafts, 'materials': required_materials}
    #
    #     if not craftable_items:
    #         if self.crafter.selling_logic.need_to_sell(self.crafter):
    #             self.crafter.mode = 'selling'
    #         else:
    #             self.crafter.toggle_mode()
    #         return
    #
    #     best_item = max(craftable_items.items(), key=lambda x: x[1]['max_crafts'])
    #     item_to_craft, details = best_item
    #     craft_quantity = min(details['max_crafts'], self.space_left)
    #     materials_used = details['materials']
    #
    #     self.perform_craft(item_to_craft, craft_quantity, materials_used)
    #
    # def craft_profitable(self):
    #     craftable_items = {}
    #
    #     for item_name, item_details in items_config.items():
    #         if item_name not in crafter_config['sell']:
    #             continue
    #
    #         required_materials = item_details.get('crafting_material', {})
    #         item_sell_price = self.crafter.model.economy.calculate_price(item_name)
    #         total_material_cost = 0
    #
    #         can_craft_at_all = True
    #         for material, required_qty in required_materials.items():
    #             material_price = self.crafter.model.economy.calculate_price(material)
    #             total_material_cost += required_qty * material_price
    #
    #             if self.crafter.inventory.get(material, 0) < required_qty:
    #                 can_craft_at_all = False
    #
    #         if can_craft_at_all:
    #             profit_per_unit = item_sell_price - total_material_cost
    #
    #             max_crafts = float('inf')
    #
    #             for material, required_quantity in required_materials.items():
    #                 available_qty = self.crafter.inventory.get(material, 0)
    #                 max_crafts = min(max_crafts, available_qty // required_quantity)
    #
    #             if max_crafts > 0:
    #                 craftable_items[item_name] = {
    #                     'profit': profit_per_unit,
    #                     'max_crafts': max_crafts,
    #                     'materials': required_materials
    #                 }
    #
    #     if not craftable_items:
    #         if self.crafter.selling_logic.need_to_sell(self.crafter):
    #             self.crafter.mode = 'selling'
    #         else:
    #             self.crafter.toggle_mode()
    #         return
    #
    #     best_item = max(craftable_items.items(), key=lambda x: x[1]['profit'])
    #     item_to_craft, details = best_item
    #     craft_quantity = min(details['max_crafts'], self.space_left)
    #     materials_used = details['materials']
    #
    #     self.perform_craft(item_to_craft, craft_quantity, materials_used)
    #
    # def craft(self):
    #     crafter = self.crafter
    #
    #     if not self.can_craft_anything():
    #         crafter.mode = 'buying'
    #         return
    #
    #     current_inventory_volume = sum(crafter.inventory.values())
    #     self.space_left = crafter.max_inventory - current_inventory_volume
    #     if self.space_left <= 0:
    #         crafter.mode = 'selling'
    #         return
    #
    #     inventory_utilization = current_inventory_volume / crafter.max_inventory if crafter.max_inventory > 0 else 0
    #     high_inventory_threshold = crafter_config.get('high_inventory_threshold', 0.8)
    #     low_wealth_threshold = crafter.wealth_margin * crafter_config.get('low_wealth_threshold', 0.2)
    #
    #     if inventory_utilization >= high_inventory_threshold or crafter.wealth <= low_wealth_threshold:
    #         self.craft_profitable()
    #     else:
    #         self.craft_optimized()
