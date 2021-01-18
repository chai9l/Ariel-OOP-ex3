from src.GraphInterface import GraphInterface


class NodeData:

    def __gt__(self, other):
        return self.weight > other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __init__(self, node_id: int, tag: int = -1, weight: float = 0.0, info: str = "", pos: tuple = None):
        self.node_id = node_id
        self.tag = tag
        self.weight = weight
        self.info = info
        self.neighbors = {}
        self.pos = pos

    def get_node_id(self):
        return self.node_id

    def get_weight(self) -> float:
        return self.weight

    def set_weight(self, weight: float):
        self.weight = weight

    def get_info(self):
        return self.info

    def set_info(self, info: str):
        self.info = info

    def get_tag(self):
        return self.tag

    def set_tag(self, tag: int):
        self.tag = tag

    def get_nei(self):
        return self.neighbors.keys()

    def add_nei(self, n, w: float):
        self.neighbors[n] = w

    def remove_nei(self, n):
        if n in self.neighbors.keys():
            self.neighbors.pop(n)

    def remove_all_nei(self):
        self.neighbors.clear()

    def set_pos(self, x, y, z):
        self.pos = (x, y, z)

    def get_pos(self):
        return self.pos

    def __repr__(self) -> str:
        return f"{self.node_id}"


class DiGraph(GraphInterface):
    def __init__(self, mc: int = 0):
        self.graph = {}  # { Int : NodeData }
        self.edges = {}  # { Tuple : Float}
        self.mc = mc

    def v_size(self) -> int:
        if len(self.graph) is None:
            return 0
        return len(self.graph)

        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """

    def e_size(self) -> int:
        return len(self.edges)

        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """

    def get_all_v(self) -> dict:
        return self.graph

        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """

    def get_node(self, key) -> NodeData:
        if key in self.graph.keys():
            return self.graph[key]
        return None

    def all_in_edges_of_node(self, key: int) -> dict:
        if key in self.graph.keys():
            connected_nodes = {}
            node = self.get_node(key)
            for temp in self.graph.values():
                if node.get_node_id() in temp.get_nei():
                    weight = node.get_weight()
                    connected_nodes[temp.get_node_id()] = weight
            return connected_nodes
        return None

        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """

    def all_out_edges_of_node(self, key: int) -> dict:
        if key in self.graph.keys():
            out_nodes = {}
            node = self.get_node(key)
            for ni in node.get_nei():
                temp = self.get_node(ni)
                weight = temp.get_weight()
                out_nodes[ni] = weight
            return out_nodes
        return None

        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """

    def get_mc(self) -> int:
        return self.mc

        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """

    def has_edge(self, node_id1: int, node_id2: int, ) -> bool:
        if node_id1 not in self.graph or node_id2 not in self.graph:
            return False
        src = self.get_node(node_id1)
        dest = self.get_node(node_id2)
        gen_key = (src.get_node_id(), dest.get_node_id())
        ret = self.edges.get(gen_key)
        if ret is None:
            return False
        return True

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.graph.keys() or id2 not in self.graph.keys() or weight <= 0:
            return False

        src = self.get_node(id1)
        gen_key = (id1, id2)

        if not self.has_edge(id1, id2):
            self.edges[gen_key] = weight
            dest = self.get_node(id2)
            dest.set_weight(weight)
            src.add_nei(id2, weight)
            self.mc = self.mc + 1
            return True

        return False
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """

    def add_node(self, key: int, pos: tuple = None) -> bool:
        if key in self.graph.keys():
            return False

        new_node = NodeData(node_id=key)
        if pos is not None:
            new_node.set_pos(pos[0], pos[1], pos[2])
        self.graph[key] = new_node
        self.mc = self.mc + 1
        return True

        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.graph:
            node = self.get_node(node_id)
            for n in self.all_in_edges_of_node(node_id):
                temp = self.get_node(n)
                temp.neighbors.pop(node)
            self.graph.pop(node_id)
            self.mc = self.mc + 1
            return True
        return False

        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        gen_key = (node_id1, node_id2)
        if gen_key in self.edges:
            self.edges.pop(gen_key)
            node1 = self.get_node(node_id1)
            node2 = self.get_node(node_id2)
            node1.neighbors.pop(node_id2)
            self.mc = self.mc + 1
            return True
        return False
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """

    def get_edge(self, id1: int, id2: int) -> float:
        if self.has_edge(id1, id2):
            tup = (id1, id2)
            return self.edges[tup]
        return None

    def __repr__(self) -> str:
        main_str = f"Graph: |V|={self.v_size()} , |E|={self.e_size()}\n"
        main_str += "{"
        counter = 0
        for vertex in self.graph.keys():
            counter += 1
            main_str += f"{vertex}: {vertex}: |edges out| "
            main_str += f"{len(self.all_out_edges_of_node(vertex).keys())} "
            main_str += "|edges in| "
            main_str += f"{len(self.all_in_edges_of_node(vertex).keys())} "

            if len(self.graph.keys()) == counter:
                main_str += "}"
            else:
                main_str += ", "
        return main_str
