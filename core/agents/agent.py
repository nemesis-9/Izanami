from mesa import Agent


class BaseAgent(Agent):
    def __init__(self, model, wealth):
        super().__init__(model)
        self.age = 20
        self.wealth = wealth
        self.alive = True
        self.location = None
        self.path = None

    def execute_pathfinding_move(self, current_pos, destination_pos):
        if current_pos == destination_pos:
            self.path = None
            return False

        if self.path is None or len(self.path) < 2:
            self.path = self.model.city_network.get_path(current_pos, destination_pos)
            if self.path is None or len(self.path) < 2:
                return False

        next_pos = self.path[1]
        self.model.grid.move_agent(self, next_pos)
        self.location = next_pos
        self.path = self.path[1:]
        return True

    def step(self):
        self.age += 1
        pass
