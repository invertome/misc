#!/usr/bin/env python3

import argparse
from gedcom.parser import Parser
from gedcom.element.individual import Individual
from gedcom.element.family import Family
from gedcom.element.header import Header
from gedcom.element.trailer import Trailer
from gedcom.element.note import Note
from gedcom.element.date import Date
from gedcom.element.place import Place
from gedcom.element.address import Address
import networkx as nx
from networkx.algorithms.bipartite.projection import projection
import matplotlib.pyplot as plt

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--ged', help='Gedcom file', required=True)
parser.add_argument('--id', help='The ID of the person whose family tree to plot', required=True)
parser.add_argument('--gen', help='Number of generations', type=int, required=True)
parser.add_argument('--out', help='Output folder', required=True)
args = parser.parse_args()

# Parse the gedcom file
gedcom_parser = Parser()
gedcom_parser.parse_file(args.ged)

# Create a dictionary of individuals
individuals = {}
for i in gedcom_parser.individuals:
    individuals[i.pointer] = i

# Create a dictionary of families
families = {}
for f in gedcom_parser.families:
    families[f.pointer] = f

# Create a directed graph
graph = nx.DiGraph()

# Add nodes to graph
for ind in individuals:
    graph.add_node(individuals[ind].pointer, name=individuals[ind].name, gender=individuals[ind].gender)

# Add edges to graph
for fam in families:
    for child in families[fam].children:
        for parent in families[fam].parents:
            graph.add_edge(individuals[parent].pointer, individuals[child].pointer)

# Get the list of ancestors of the given individual
ancestors = nx.ancestors(graph, args.id)

# Get the subgraph containing the given individual and his/her ancestors
subgraph = graph.subgraph(ancestors.union({args.id}))

# Project the bipartite graph to get the family tree
family_tree = projection(subgraph, args.id)

# Plot the family tree
plt.figure(figsize=(20, 10))
pos = nx.spring_layout(family_tree, k=4)
nx.draw_networkx(family_tree, pos, arrows=True, with_labels=True, 
                 node_color=[individuals[node].gender for node in family_tree.nodes()],
                 edge_color='gray', node_size=1000, 
                 labels={node: individuals[node].name for node in family_tree.nodes()})
plt.savefig(args.out + '/family_tree.pdf')
