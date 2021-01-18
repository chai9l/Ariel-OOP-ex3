import random
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
import json
import networkx
import time


class Comparing:

    def __init__(self):
        self.g = DiGraph()
        self.graph = GraphAlgo(self.g)

    def get_graph(self):
        return self.graph.get_graph()

    def check(self, str=None, nodes=None):
        print(f"Testing:{str} \n")
        print("With python")
        self.graph.load_from_json(str)
        print("shortest path:")
        start_time = time.time()
        size = self.get_graph().v_size()
        src = self.get_graph().get_node(int(random.uniform(0, size)))
        dest = self.get_graph().get_node(int(random.uniform(0, size)))
        self.graph.shortest_path(src.get_node_id(), dest.get_node_id())
        time_took = time.time() - start_time
        print("Time took:", time_took, "\n")
        print("connected component:")
        start_time = time.time()
        self.graph.connected_component(src.get_node_id())
        time_took = time.time() - start_time
        print("Time took:", time_took, "\n")
        print("connected components:")
        start_time = time.time()
        self.graph.connected_components()
        time_took = time.time() - start_time
        print("Time took:", time_took)

        # networkx

        print(f"\nTesting:{str}")
        print("\nWith networkX:")
        try:
            with open(str, 'r') as my_file:
                j_read = my_file.read()
                j_graph = json.loads(j_read)
                n_graph = networkx.DiGraph()
                for n in j_graph['Nodes']:
                    pos = n.get('pos')
                    if pos is not None:
                        pos = tuple(map(float, n['pos'].split(',')))
                    key = n['id']
                    n_graph.add_node(key, pos=pos)

                for e in j_graph['Edges']:
                    n_graph.add_edge(int(e['src']), int(e['dest']), weight=float(e['w']))

        except IOError as e:
            print(e)

        nodes = (src, dest)
        print("shortest path:")
        networkx.shortest_path_length(n_graph, source=nodes[0].get_node_id(), target=nodes[1].get_node_id(),
                                      method="dijkstra")
        start_time = time.time()
        networkx.shortest_path(n_graph, source=nodes[0].get_node_id(), target=nodes[1].get_node_id(), method="dijkstra",
                               weight="weight")
        time_took = time.time() - start_time
        print("Time took:", time_took, "\n")
        print("connected components:")
        start_time = time.time()
        list(networkx.strongly_connected_components(n_graph))
        time_took = time.time() - start_time
        print("Time took:", time_took, "\n")
        print("*************** Finished ***************")


if __name__ == '__main__':
    g1 = "../data/Graphs_on_circle/G_10_80_1.json"
    g2 = "../data/Graphs_on_circle/G_100_800_1.json"
    g3 = "../data/Graphs_on_circle/G_1000_8000_1.json"
    g4 = "../data/Graphs_on_circle/G_10000_80000_1.json"
    g5 = "../data/Graphs_on_circle/G_20000_160000_1.json"
    g6 = "../data/Graphs_on_circle/G_30000_240000_1.json"
    compare_graphs = [g1, g2, g3, g4, g5, g6]
    for i in compare_graphs:
        Comparing().check(str=i)
