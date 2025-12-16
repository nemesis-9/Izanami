class AgentHP:
    def __init__(self, agent):
        self.agent = agent

    def death_check(self):
        if not self.agent.alive:
            return True

        if self.agent.hp <= 0:
            self.agent.alive = False
            return True

        # elif self.agent.hp <= self.agent.hp_min_margin:
            # TODO: add doctor visit logic here

        elif self.agent.hp > self.agent.hp_min_margin:
            return False
