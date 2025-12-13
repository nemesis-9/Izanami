from core.config.global_config import GlobalConfig

global_config = GlobalConfig().get()
crafter_config = global_config.agent_item_list('crafter')
items_config = global_config.items


class CrafterCraft:
    def __init__(self, crafter):
        self.crafter = crafter

    def perform_craft(self, item_name, quantity, materials_used):
        if quantity <= 0:
            return

        for material, required_qty in materials_used.items():
            self.crafter.inventory[material] -= required_qty * quantity

        self.crafter.inventory[item_name] = self.crafter.inventory.get(item_name, 0) + quantity

        if sum(self.crafter.inventory.values()) >= self.crafter.max_inventory * self.crafter.inventory_margin:
            self.crafter.mode = 'selling'

    def craft_optimized(self):
        craftable_items = {}
        for item_name, item_details in items_config.items():
            if item_name not in crafter_config['sell']:
                continue

            required_materials = item_details.get('crafting_material', {})
            max_crafts = float('inf')
            can_craft = True

            for material, required_quantity in required_materials.items():
                available_qty = self.crafter.inventory.get(material, 0)
                if available_qty < required_quantity:
                    can_craft = False
                    break

                max_crafts = min(max_crafts, available_qty // required_quantity)

            if can_craft and max_crafts > 0:
                craftable_items[item_name] = {'max_crafts': max_crafts, 'materials': required_materials}

        if not craftable_items:
            if self.crafter.selling_logic.need_to_sell(self.crafter):
                self.crafter.mode = 'selling'
            else:
                self.crafter.toggle_mode()
            return

        best_item = max(craftable_items.items(), key=lambda x: x[1]['max_crafts'])
        item_to_craft, details = best_item
        craft_quantity = details['max_crafts']
        materials_used = details['materials']

        self.perform_craft(item_to_craft, craft_quantity, materials_used)

    def craft_profitable(self):
        craftable_items = {}

        for item_name, item_details in items_config.items():
            if item_name not in items_config['sell']:
                continue

            required_materials = item_details.get('crafting_material', {})
            item_sell_price = self.crafter.model.economy.calculate_price(item_name)
            total_material_cost = 0

            can_craft_at_all = True
            for material, required_qty in required_materials.items():
                material_price = self.crafter.model.economy.calculate_price(material)
                total_material_cost += required_qty * material_price

                if self.crafter.inventory.get(material, 0) < required_qty:
                    can_craft_at_all = False

            if can_craft_at_all:
                profit_per_unit = item_sell_price - total_material_cost

                max_crafts = float('inf')

                for material, required_quantity in required_materials.items():
                    available_qty = self.crafter.inventory.get(material, 0)
                    max_crafts = min(max_crafts, available_qty // required_quantity)

                if max_crafts > 0:
                    craftable_items[item_name] = {
                        'profit': profit_per_unit,
                        'max_crafts': max_crafts,
                        'materials': required_materials
                    }

        if not craftable_items:
            if self.crafter.selling_logic.need_to_sell(self.crafter):
                self.crafter.mode = 'selling'
            else:
                self.crafter.toggle_mode()
            return

        best_item = max(craftable_items.items(), key=lambda x: x[1]['profit'])
        item_to_craft, details = best_item
        craft_quantity = details['max_crafts']
        materials_used = details['materials']

        self.perform_craft(item_to_craft, craft_quantity, materials_used)

    def craft(self):
        crafter = self.crafter
        if (
                sum(crafter.inventory.values()) >= crafter.max_inventory * crafter.inventory_margin
                and crafter.selling_logic.need_to_sell(crafter)
        ):
            crafter.mode = 'selling'
            return

        if not any(crafter.inventory.get(mat > 0) for mat in crafter_config['buy']):
            crafter.mode = 'buying'

        current_inventory_volume = sum(crafter.inventory.values())
        inventory_utilization = current_inventory_volume / crafter.max_inventory if crafter.max_inventory > 0 else 0

        high_inventory_threshold = crafter_config['high_inventory_threshold']
        low_wealth_threshold = crafter.wealth_margin * crafter_config['low_wealth_threshold']

        if inventory_utilization >= high_inventory_threshold or crafter.wealth <= low_wealth_threshold:
            self.craft_profitable()
        else:
            self.craft_optimized()
