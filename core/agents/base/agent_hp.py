class AgentHP:
    def __init__(self, agent):
        self.agent = agent

    def die(self):
        self.agent.alive = False
        if self.agent.location:
            self.agent.model.grid.remove(self.agent)

        self.agent.model.agents.remove(self.agent)

    def death_check(self):
        if not self.agent.alive:
            return True

        if self.agent.hp <= 0:
            self.agent.alive = False
            return True

        # TODO: add doctor visit logic here
        # elif self.agent.hp <= self.agent.hp_min_margin:

        return False
