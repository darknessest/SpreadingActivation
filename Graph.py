from Edge import Edge
from Node import Node
from SchemaType import SchemaType


class Graph:
    def __init__(self) -> None:
        self.nodes: list[Node] = []
        self.edges: dict[Node, list[Edge]] = dict()

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def add_edge(self, node_a: Node, node_b: Node, weight: float) -> None:
        if self.edges.get(node_a):
            self.edges[node_a].append(Edge(node_a, node_b, weight))
        else:
            self.edges[node_a] = [Edge(node_a, node_b, weight)]
        if self.edges.get(node_b):
            self.edges[node_b].append(Edge(node_b, node_a, weight))
        else:
            self.edges[node_b] = [Edge(node_b, node_a, weight)]

    def remove_node(self, node: Node) -> None:
        self.nodes.remove(node)

        for edge in self.edges.pop(node):
            self.remove_edge(edge)

    def remove_edge(self, edge: Edge) -> None:
        try:
            self.edges[edge.node_a].remove(edge)
        except ValueError:
            pass
        try:
            self.edges[edge.node_b].remove(edge)
        except ValueError:
            pass

    def get_adjacent_edges(self, node: Node) -> list[Edge]:
        return self.edges[node]

    def __str__(self) -> str:
        # include the weight, value, and type of the node and list the names of the nodes it is connected to
        return (
            "Graph(\n"
            + ",\n".join(
                [
                    f"{node!s} -> {', '.join([edge.node_b.name for edge in self.edges[node]])}"
                    for node in self.nodes
                ]
            )
            + "\n)"
        )

    def __repr__(self) -> str:
        # include the weight, value, and type of the node and list the names of the nodes it is connected to
        return (
            "Graph(\n"
            + ",\n".join(
                [
                    f"{node!r} -> {', '.join([edge.node_b.name for edge in self.edges[node]])}"
                    for node in self.nodes
                ]
            )
            + "\n)"
        )


if __name__ == "__main__":
    g = Graph()
    n1 = Node(1, SchemaType.partnership, "n1")
    n2 = Node(2, SchemaType.feature, "n2")
    n3 = Node(3, SchemaType.value_prop, "n3")
    n4 = Node(4, SchemaType.customer_seg, "n4")

    g.add_node(n1)
    g.add_node(n2)
    g.add_node(n3)
    g.add_node(n4)

    g.add_edge(n1, n2, 1.0)
    g.add_edge(n2, n3, 1.0)
    g.add_edge(n3, n4, 1.0)
    g.add_edge(n4, n1, 1.0)

    print(repr(g))
