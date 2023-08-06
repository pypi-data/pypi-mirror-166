import sklearn
import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from .templating import return_function


def convert_graph(graph):
    """
    Convert graph to adjacency matrix.
    """
    nodes = graph["nodes"]
    edges = graph["edges"]
    edge_map = {}
    node_map = {}
    for node in nodes:
        node_map[node["id"]] = node
    for edge in edges:
        edge_map[edge["source"]] = edge["target"]
    return node_map, edge_map


def generate_steps(nodes, edges):
    """
    Generate steps for processing data.
    """
    steps_list = []
    current_node = edges["999"]
    traversing = True
    while traversing:
        if current_node in nodes:
            current_node = edges[current_node]
            steps_list.append(return_function(nodes[current_node]))
        else:
            raise Exception("Invalid node")
        if edges[current_node] == "998":
            traversing = False
    return steps_list


def generate_script():
    """
    Generate script for processing data.
    """
    file_loader = FileSystemLoader("src/huble/sklearn/templates")
    env = Environment(loader=file_loader)
    template = env.get_template("preprocess.j2")
    parameters = {"steps_list": ["huble.sklearn.drop_duplicates(data)", "huble.sklearn.drop_duplicates(data1)"]}
    output = template.render(parameters)
    print(output)
