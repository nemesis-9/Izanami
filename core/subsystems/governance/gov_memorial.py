class GovMemorial:
    def __init__(self, gov):
        self.gov = gov

    def memorial(self, agents):
        for agent in agents:
            entry = {
                key: func(agent)
                for key, func in self.gov.memorial_template.items()
            }
            self.gov.memorial_log.append(entry)

            self.gov.treasury += agent.wealth
            agent.wealth = 0

            update_inventory = lambda acc, src: {
                k: acc.get(k, 0) + src.get(k, 0)
                for k in set(acc) | set(src)
            }
            self.gov.inventory = update_inventory(self.gov.inventory, agent.inventory)
            agent.inventory = {}

            agent.memorial = True

