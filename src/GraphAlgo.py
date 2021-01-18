import functools
import sys
from collections import deque
from typing import List
from src import GraphInterface
from src.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph, NodeData
import json
from queue import *
import matplotlib.pyplot as plt
import random
from src.GraphAlgoInterface import GraphAlgoInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = None):
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        loaded_graph = DiGraph()

        try:
            with open(file_name, 'r') as j_file:
                json_str = j_file.read()
                j_graph = json.loads(json_str)

            for node in j_graph['Nodes']:
                pos = node.get('pos')
                if pos is not None:
                    pos = tuple(map(float, node['pos'].split(',')))
                key = node['id']
                loaded_graph.add_node(key, pos)

            for edge in j_graph['Edges']:
                if edge['w'] is None:
                    loaded_graph.add_edge(int(edge['src']), int(edge['dest']), 0.0)
                else:
                    loaded_graph.add_edge(int(edge['src']), int(edge['dest']), float(edge['w']))

            self.graph = loaded_graph
        except IOError:
            return False

        if self.graph is not None:
            return True

        return False

    def save_to_json(self, file_name: str) -> bool:

        if self.graph is None:
            return False

        j_graph = dict()
        j_nodes = []
        j_edges = []

        try:
            with open(file_name, 'w') as file:

                for node in self.graph.get_all_v().values():
                    node_info = dict()
                    pos = node.get_pos()
                    if pos is not None:
                        pos_str = str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2])
                        node_info["pos"] = pos_str
                    node_info["id"] = node.get_node_id()
                    j_nodes.append(node_info)

                    for edge in self.graph.edges:
                        edge_info = dict()
                        edge_info["src"] = edge[0]
                        edge_info["dest"] = edge[1]
                        edge_info["w"] = self.graph.all_out_edges_of_node(node.get_node_id()).get(edge)
                        j_edges.append(edge_info)
                j_graph["Edges"] = j_edges
                j_graph["Nodes"] = j_nodes

                json.dump(j_graph, indent=4, fp=file)
            return True
        except IOError as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self.graph is None:
            return []
        src = self.graph.get_node(id1)
        dest = self.graph.get_node(id2)
        #prio_que = PriorityQueue()
        p_que = deque()
        prev = {}
        vis = {}
        directions = []
        if src is not None and dest is not None:


            if id1 == id2:
                directions.append(id1)
                return 0, directions

            for t in self.graph.get_all_v():
                self.graph.get_node(t).set_tag(-1)

            src.set_tag(0)
            #prio_que.put(src)
            p_que.append(src)
            vis[src.get_node_id()] = True
            current = src
            new_ret = src

            #while not prio_que.empty():
            while len(p_que) != 0:

                #current = prio_que.get()
                current = p_que.pop()

                # if current.get_node_id() == dest.get_node_id():
                #     break

                for out_node in self.graph.all_out_edges_of_node(current.node_id):
                    d = self.graph.get_edge(current.get_node_id(), out_node)
                    node_dest = self.graph.get_node(out_node)
                    node_dest_id = out_node

                    if node_dest.get_tag() == -1:
                        node_dest.set_tag(sys.maxsize)

                    new_dis = current.get_tag() + d
                    prev_dis = node_dest.get_tag()

                    if new_dis < prev_dis:
                        node_dest.set_tag(new_dis)
                        prev[node_dest.get_node_id()] = current.get_node_id()
                        #prio_que.put(node_dest)
                        p_que.appendleft(node_dest)
                if current.get_node_id() == dest.get_node_id():
                    new_ret = current

                vis[new_ret.get_node_id] = True

            eq = new_ret.get_node_id() == dest.get_node_id()
            if not eq:
                return float('inf'), []

            node_finish = dest
            directions.append(dest.get_node_id())
            temp_weight = 0

            while node_finish is not None:
                node_finish = prev.get(node_finish.get_node_id())
                if node_finish is not None:
                    directions.append(node_finish)
                node_finish = self.graph.get_node(node_finish)

            for s, d in prev.items():
                if s in directions and d in directions:
                    e = (d, s)
                    if e in self.graph.edges.keys():
                        temp_weight = temp_weight + self.graph.edges[e]

            directions.reverse()

            return temp_weight, directions

        elif src is None or dest is None:
            return float('inf'), []

        else:
            return directions

    def connected_component(self, id1: int) -> list:
        if self.graph is None or id1 not in self.graph.get_all_v().keys():
            return []
        que = deque()
        que.append(id1)
        visited = {id1: True}
        connected = [id1]
        while len(que) != 0:
            curr = que.popleft()
            curr_nei = self.graph.all_out_edges_of_node(curr)
            for nei in curr_nei.keys():
                if visited.get(nei) is None:
                    que.append(nei)
                    visited[nei] = True
                    connected.append(nei)
        tran_graph = self.transpose_graph(self.graph)

        que.append(id1)
        tran_graph_vis = {id1: True}
        tran_connected = [id1]
        while len(que) != 0:
            curr = que.popleft()
            curr_nei = tran_graph.all_out_edges_of_node(curr)
            for nei in curr_nei.keys():
                if tran_graph_vis.get(nei) is None:
                    que.append(nei)
                    tran_graph_vis[nei] = True
                    tran_connected.append(nei)

        return list(set(connected) & set(tran_connected))

    def connected_components(self) -> List[list]:
        if self.graph is None:
            return []
        nodes_id = self.graph.get_all_v().keys()
        checked = []
        connected_comp = []
        for key in nodes_id:
            if key not in checked:
                connected_nodes = self.connected_component(key)
                checked.extend(connected_nodes)
                connected_comp.append(connected_nodes)
        return connected_comp

    def plot_graph(self) -> None:
        if self.graph is None:
            return None

        plt.grid(color='purple', linestyle='dashed', linewidth=0.4)
        for e in self.get_graph().edges:
            src = self.get_graph().get_node(e[0])
            dest = self.get_graph().get_node(e[1])

            if src.get_pos() is None:
                src.set_pos(random.uniform(0, 100), random.uniform(0, 100), 0)
            if dest.get_pos() is None:
                dest.set_pos(random.uniform(0, 100), random.uniform(0, 100), 0)

            x_list = [src.get_pos()[0], dest.get_pos()[0]]
            y_list = [src.get_pos()[1], dest.get_pos()[1]]
            plt.plot(x_list, y_list, color="teal")

        for node_id, node in self.get_graph().get_all_v().items():
            plt.annotate(str(node_id), (node.get_pos()[0], node.get_pos()[1]), color='black')
            plt.plot(node.get_pos()[0], node.get_pos()[1], ".", color='red', markersize=10)

        plt.xlabel(
            "X ------------------------------------------------------------------------------------------------------>")
        plt.ylabel("Y -------------------------------------------------------------------------->")
        plt.title("Ex3")
        plt.show()

    def transpose_graph(self, to_transpose: DiGraph) -> DiGraph:

        ret = DiGraph()

        for node in to_transpose.graph:
            temp_node = to_transpose.get_node(node)
            temp_node.set_tag(0)
            ret.add_node(temp_node.get_node_id())

        for edge, weight in to_transpose.edges.items():
            e_temp = edge
            w_temp = weight
            ret.add_edge(e_temp[1], e_temp[0], w_temp)

        return ret

    def graph_reset(self):
        for node in self.graph:
            node = self.graph.get_node(node)
            node.set_tag(0)
