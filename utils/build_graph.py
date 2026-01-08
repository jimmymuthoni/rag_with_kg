import networkx as nx
import matplotlib.pyplot as plt

class KnowledgeGraph:
    def __init__(self, df:str = None):
        self.df = df

    def create_graph(self):
        """method for creating graph"""
        self.G = nx.from_pandas_edgelist(self.df, 'node_1', 'node_2', edge_attr='edge', create_using=nx.MultiGraph())
        nx.draw(self.G, with_labels=True)
    
    def query_sub_graph(self, query_node):
        """method to perform query on nodes"""
        neighbors = list(self.G.neighbors(query_node)) + [query_node]
        subgraph = self.G.subgraph(neighbors)
        pos = nx.spring_layout(subgraph)
        plt.figure(figsize=(8,8))

        node_size = 2000
        node_color = 'lightblue'
        font_color = 'black'
        font_weight = 'bold'
        font_size = 8
        edge_color = 'gray'
        edge_style = 'dashed'

        #drawing subgraph
        nx.draw(subgraph, pos, with_labels=True, node_size=node_size, node_color=node_color, font_color=font_color,
                font_size=font_size, font_weight=font_weight, edge_color=edge_color, style=edge_style)
        
        plt.title(f"Graph of Node: {query_node}")
        plt.savefig('subgraph.png')
