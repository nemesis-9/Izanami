from mesa import Model
from mesa.space import MultiGrid


class CityModel(Model):
    def __init__(self, unique_id, parent_world, width=100, height=100, agents=5):
        super().__init__()
        self.unique_id = unique_id
        self.parent_world = parent_world

        self.grid = MultiGrid(width, height, torus=False)

        from core.agents.agent import BaseAgent
        for _ in range(agents):
            agent = BaseAgent(self, wealth=self.random.randrange(10, 50))
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x,y))

    def step(self):
        self.agents.shuffle_do("step")
