class Edge:
    def __init__(self, node_a, node_b, weight: float) -> None:
        """Initializes an edge between two nodes.
            Directed edge from node_a to node_b with a weight.

        Args:
            node_a (Node): Starting node
            node_b (Node): Ending node
            weight (float): Weight of the edge
        """
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight

    def __repr__(self) -> str:
        return f"Edge({self.node_a.name} -> {self.node_b.name}, {self.weight=:.4f})"

    def __str__(self) -> str:
        return f"Edge({self.node_a.name} -> {self.node_b.name}, {self.weight})"

    def __eq__(self, other) -> bool:
        # NOTE: This is a directed edge, so the order of the nodes matters
        if not isinstance(other, Edge):
            return NotImplemented("Cannot compare Edge with non-Edge type")

        return (
            self.node_a == other.node_a
            and self.node_b == other.node_b
            and self.weight == other.weight
        )

    def __hash__(self) -> int:
        return hash((self.node_a, self.node_b, self.weight))
