import json
from typing import List

from networkx import DiGraph, dfs_tree, node_link_graph, shortest_path
from networkx.classes.reportviews import OutEdgeView


class Auditor(object):

    def __init__(self, graph_specification: str) -> None:
        self.graph = self._load_graph(graph_specification)

    def _load_graph(self, graph_specification: str) -> DiGraph:
        with open(graph_specification, "r") as inf:
            graph: dict = json.load(inf)
        return node_link_graph(graph)

    def _explore_from_vertex(self,
                             vertex: str,
                             depth_limit: int = 5) -> List[str]:
        subgraph: DiGraph = dfs_tree(self.graph,
                                     vertex,
                                     depth_limit=depth_limit)
        edges: OutEdgeView = subgraph.edges()
        can_reach: List[str] = []
        for edge, edge_info in edges.items():
            u, v = edge  # edge is a tuple ("u", "v"), python type hints don't work with .items?  # type: ignore  # noqa:E501
            can_reach.append(v)
        return can_reach

    def search_for_iv_violations(self,
                                 proposed_instrument: str = "weather",
                                 proposed_outcome: str = "research",
                                 depth_limit: int = 5) -> None:

        can_reach: List[str] = self._explore_from_vertex(
            vertex=proposed_instrument, depth_limit=depth_limit
        )

        if proposed_outcome in can_reach:
            print("[*] Found a possible violation")
            print(shortest_path(self.graph,
                                source=proposed_instrument,
                                target=proposed_outcome))
        else:
            print("[*] No violations found")