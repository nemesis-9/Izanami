from mesa import Agent


class BaseAgent(Agent):
    def __init__(self, model, wealth):
        super().__init__(model)
        self.age = 0
        self.wealth = wealth
        self.alive = True
        self.location = None

    def step(self):
        self.age += 1
        pass
