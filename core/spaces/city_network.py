import networkx as nx


class CityNetwork:
    def __init__(self, model, width, height):
        self.model = model
        self.graph = nx.grid_2d_graph(width, height)
        nx.set_edge_attributes(self.graph, 1, 'cost')
        self.points_of_interest = {
            "market": (width//2, height//2),
            "farm_plot_1": (5, height-5),
            "farm_plot_2": (width-5, 5),
            "city_center": (width//2, 5),
        }

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
        except Exception:
            return None
