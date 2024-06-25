import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

from firstml.helpers.pipe_combine import PipeCombine


class GraphResolver:
    def __init__(self):
        self.pipe_combine = PipeCombine()

    @staticmethod
    def build_graph(gr):

        graph = nx.DiGraph()
        for node in gr["nodebooks"]:
            for input_n in node["inputs"]:
                for output_n in node["outputs"]:

                    graph.add_edge(input_n, output_n, name=f"""{node['nodebook_id']}_{node['nodebook_id_suffix']}""")

        return graph

    @staticmethod
    def _sort_nodes(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def resolve_run(self, gr):
        graph = self.build_graph(gr)
        sorted_graph = list(nx.topological_sort(nx.line_graph(graph)))
        sorted_nodes = []

        for el in sorted_graph:
            sorted_nodes.append(graph.get_edge_data(el[0], el[1])["name"])
        sorted_run = list(reversed(self._sort_nodes(reversed(sorted_nodes))))
        print(f"""..sorted graph: {sorted_run} """)
        return sorted_run

    def viz_graph(self, gr, size=(20, 20)):
        self._create_graph(gr, size)
        plt.show()

    def save_graph(self, gr, size=(20, 20), file_name="./data/graph.png"):
        self._create_graph(gr, size)
        plt.savefig(file_name)

    def _create_graph(self, gr, size=(20, 20)):
        gr_ = self.pipe_combine.combine_pipelines(gr)
        graph = self.build_graph(gr_)
        pos = graphviz_layout(graph, prog="dot")
        # pos = nx.multipartite_layout(graph, subset_key="name")
        # pos = nx.spring_layout(graph)
        plt.figure(figsize=size)

        nx.draw(graph, pos, arrows=True, with_labels=True)
        edge_labels = nx.get_edge_attributes(graph, "name")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels)
