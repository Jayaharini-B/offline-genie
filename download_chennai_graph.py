import osmnx as ox

# Download Chennai walking network graph
G = ox.graph_from_place("Chennai, India", network_type='walk')

# Save to file
ox.save_graphml(G, "chennai_walk.graphml")
