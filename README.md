![enter image description ssad](https://sites.google.com/a/afridar.ort.org.il/python/_/rsrc/1563114502427/home/python.jpg)
# Weighted Directed Graphs in Python
This project is the third assignment given to us in the Object Oriented Programming course in Ariel University.
In this project we'll take a look at a few algorithms concerning Weighted Directed Graphs in Python.

## File List

***NodeData (inside of DiGraph) :***
	***Fields :**
	node_id = an Integer representing the node's id
	
	tag  = an Integer representing the node's tag
	
	weight  = a Float representing the node's weight
	
	info  = a String representing the node's info
	
	neighbors = a Dictionary representing a specific node's neighbors
	
	pos = a Tuple representing a node's postion*
	
***Methods :***	
| Method's Name | Description |
|--|--|
|get_node_id  | returns a specific node's id  |
|get/set_weight | returns or sets a specific node's weight |
|get/set_info  | returns or sets a specific node's info |
|get/set_tag  | returns or sets a specific node's tag  |
|get/set_pos |	returns or sets a specific node's postion  |
|get_nei  | returns a specific node's neighbor dictionary |
|add_nei  | adds to a specific node's neighbor dictionary  |
|remove_nei  |removes a neighbor from a specific node's neighbor dictionary |
|remove_all_nei|removes all the neighbors in a specific node's neighbor dictionary

***DiGraph***
***Fields :***
*graph =  a Dictionary of  { Int : NodeData }  representing the graph's Nodes
edges = a Dictionary of { Tuple : Float}  representing the graph's Edges
mc = an Integer representing the number of changes a Graph has been through.*

***Methods :***

| Method's Name | Description |
|--|--|
| v_size |Returns the number of nodes in the graph Dictionary  |
| e_size |Returns the number of edges in the edge Dictionary  |
| get_all_v |Returns a Dictionary of all nodes in the graph  |
| get_node |Returns a specific NodeData  |
| all_in_edges_of_node |Returns a Dictionary containing all the edges that are going into a specific node  |
| all_out_edges_of_node |Returns a Dictionary containing all the edges that are going out of a specific node  |
| get_mc |Returns the mc of a specific Graph  |
| has_edge |Returns a Boolean (true or false) marking if 2 nodes has an Edge beteween them  |
| add_edge |Attempts to add an edge to the Edges Dictionary  |
| add_node |Attempts to add a node to the Graph|
| remove_node |Attempts to remove a node from the Graph  |
| get_edge|Returns a Float marking the weight between two Nodes  |

***GraphAlgo :***
***Fields :***
	graph = DiGraph object representing the graph which we're going to work on.

***Methods :***
| Method's Name | Description |
|--|--|
|get_graph  |Returns a specific DiGraph  |
|load_from_json  |Attempts to load a Graph from a given Json File  |
|save_to_json  |Attempts to save a Graph to a given String representing the file's name  |
|shortest_path  |Finds the shortest path between two given node ids, after finding the shortest path we're returning it via List  |
|connected_component  |Finds a specific connected component via given node id  |
|connected_components  |Finds all the SCC(Strongly Connected Components) inside a given graph, then returning them as a List  |
|plot_graph  |The graph's GUI  |
|transpose_graph  |Attempts to transpose a graph, transposes it's edges ddirections  |
|graph_reset  |Attempts to reset all of the node's tags |





