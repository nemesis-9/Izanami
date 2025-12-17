import random

import networkx as nx


class CityNetwork:
    def __init__(self, model, width, height):
        self.model = model
        self.width = width
        self.height = height

        self.graph = nx.grid_2d_graph(width, height)

        for u, v in self.graph.edges():
            self.graph.edges[u, v]['cost'] = 1.0 + random.random() * 0.05
            self.graph.edges[u, v]['base_cost'] = self.graph.edges[u, v]['cost']

        self.points_of_interest = {
            "market": (width//2, height//2),
            "farm_plot_1": (5, height-5),
            "farm_plot_2": (width-5, 5),
            "city_center": (width//2, 5),
        }

        nx.set_edge_attributes(self.graph, 0, 'current_usage')

    def get_path(self, start_pos, end_pos):
        if (start_pos not in self.graph) or (end_pos not in self.graph):
            return None
        try:
            path = nx.shortest_path(
                self.graph,
                source=start_pos,
                target=end_pos,
                weight='cost'
            )
            return path
        except nx.NetworkXNoPath:
            return None

    def adjust_cost_for_step(self, congestion_factor=0.1):
        for u, v in self.graph.edges():
            base_cost = self.graph.edges[u, v]['base_cost']
            usage = self.graph.edges[u, v]['current_usage']

            new_cost = base_cost * (1 + usage * congestion_factor)
            self.graph.edges[u, v]['cost'] = new_cost
            self.graph.edges[u, v]['current_usage'] = 0

    def record_usage(self, edge_u, edge_v):
        if self.graph.has_edge(edge_u, edge_v):
            self.graph.edges[edge_u, edge_v]['current_usage'] += 1

        elif self.graph.has_edge(edge_v, edge_u):
            self.graph.edges[edge_u, edge_v]['current_usage'] += 1
