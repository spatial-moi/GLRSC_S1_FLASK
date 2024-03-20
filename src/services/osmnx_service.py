import networkx
import osmnx
from geoalchemy2 import shape
import math
from shapely import set_srid
import threading


def midpoint_two(origin, destination):
    print(threading.active_count())
    print(threading.enumerate())
    print(threading.current_thread())
    user_graph = osmnx.graph_from_point(origin, 3200, 'network', 'walk')

    print(user_graph)

    destinationNode = osmnx.nearest_nodes(user_graph, destination[1], destination[0])
    print(destinationNode)
    ## Origin node

    originNode = osmnx.nearest_nodes(user_graph, origin[1], origin[0])
    print(originNode)


    ## Route

    route = networkx.shortest_path(user_graph, originNode, destinationNode)

    midpoint_val = math.trunc(len(route) / 2 - 1)

    midpoint_node = route[midpoint_val]
    print("midpoint node")
    print(midpoint_node)

    midpoint_lat = user_graph.nodes[midpoint_node]['y']
    midpoint_long = user_graph.nodes[midpoint_node]['x']
    print(midpoint_lat)
    print(type(midpoint_lat))
    print(midpoint_long)
    midpoint_tuple = (midpoint_lat, midpoint_long)
    locations = [origin, midpoint_tuple]
    return locations


def get_graph(origin):
    return osmnx.graph_from_point(origin, 3200, 'network', 'walk')


def midpoint_more(origin, longitudes, latitudes):
    midpoint_x = average_x(longitudes)
    midpoint_y = average_y(latitudes)

    midpoint_tuple = (midpoint_x, midpoint_y)
    user_graph = osmnx.graph_from_point(origin, 3200, 'network', 'walk')

    midpointNode = osmnx.nearest_nodes(user_graph, midpoint_tuple[1], midpoint_tuple[0])
    print(midpointNode)

    midpoint_lat = user_graph.nodes[midpointNode]['y']
    midpoint_long = user_graph.nodes[midpointNode]['x']

    print(midpoint_lat)
    print(midpoint_long)
    refined_midpoint_tuple = (midpoint_lat, midpoint_long)
    locations = [origin, refined_midpoint_tuple]
    return locations


def average_x(longitudes):
    total_x = 0
    for longitude in longitudes:
        total_x += longitude
    new_x = total_x / len(longitudes)
    return new_x


def average_y(latitudes):
    total_y = 0
    for latitude in latitudes:
        total_y += latitude

    new_y = total_y / len(latitudes)
    return new_y
