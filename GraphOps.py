from Graph import Graph
from Node import Node
from SchemaType import SchemaType

from concurrent.futures import ThreadPoolExecutor
from queue import PriorityQueue
from loguru import logger


class GraphOps:
    def __init__(
        self,
        graph: Graph,
        spread_schema: SchemaType,
        decay_factor: float = 0.8,
        threshold: float = 0.6,
        max_steps: int = 10,
        self_activation: bool = False,
        orderly_spreading: bool = False,
        directional_spreading: bool = True,
        stop_at_leafs: bool = True,
        num_processes: int = 4,
    ):
        self.__graph: Graph = graph
        self.__spread_schema: SchemaType = spread_schema
        # in case of a fully connected graph
        self.__activation_queue = PriorityQueue(maxsize=len(self.__graph.nodes) ** 2)
        self.decay_factor = decay_factor
        self.__threshold = threshold
        self.__max_steps = max_steps
        self.__self_activation = self_activation
        self.__orderly_spreading = orderly_spreading
        self.__directional_spreading = directional_spreading
        self.__stop_at_leafs = stop_at_leafs
        self.__n_proc = num_processes

    def _activate_node(
        self,
        node: Node,
        parent_node: Node,
        pre_value: float,
    ):
        with node.value_lock_ext:
            node.value = parent_node.value * pre_value
            if node.value > self.__threshold:
                node.value = min(node.value, 1.0)
            else:
                logger.trace(
                    f"Node {node.name} calculated value {node.value:.4f} "
                    "is below the threshold"
                )
                node.value = 0

    def _is_traversable(
        self, node_a: Node, node_b: Node, priority_value: float
    ) -> bool:
        """Check if the node a can be activated from node b.

        Args:
            node_a (Node): Source node
            node_b (Node): Destination node
        """
        # parameter-based checks
        if not self.__self_activation and node_a.type == node_b.type:
            logger.trace(
                f"Node {node_a.name} and {node_b.name} are of the same type. Skipping."
            )
            return False
        if self.__stop_at_leafs and node_b.type in (
            self.__spread_schema.last(),
            self.__spread_schema.first(),
        ):
            logger.trace(f"Node {node_b.name} is a leaf node. Skipping.")
            return False
        if self.__directional_spreading and node_a.type + 1 != node_b.type:
            logger.trace(
                f"Node {node_a.name} and {node_b.name} are not adjacent in the schema. Skipping."
            )
            return False
        if self.__orderly_spreading and node_a.type <= node_b.type:
            logger.trace(
                f"Node {node_a.name} is not of a lower type than {node_b.name}. Skipping."
            )
            return

        # regular checks
        if node_b.value != 0:
            logger.trace(f"Node {node_b.name} is already activated. Skipping.")
            return False
        if priority_value < self.__threshold:
            logger.trace(
                f"Priority value {priority_value:.4f} is below the threshold. Skipping."
            )
            return False

        # TODO: add more checks

        return True

    def activate_priority_queue(self):
        # pop the traversal pair with the highest value from the priority queue
        # activate the node (i.e., calculate the value of the node:
        # (`decay_factor` ^ `step_num`) * `edge_weight` * `node_a.value`
        # or "priority value" *  `node_a.value`
        # )
        with ThreadPoolExecutor(self.__n_proc) as pool:
            results = []
            while not self.__activation_queue.empty():
                step_num, priority_value, node_a, node_b = self.__activation_queue.get()
                priority_value *= -1
                logger.debug(
                    f"Activating {node_b.name} from {node_a.name} on step "
                    f"{step_num} with priority value {priority_value:.4f}"
                )

                results.append(
                    pool.submit(
                        self._activate_node,
                        node=node_b,
                        parent_node=node_a,
                        pre_value=priority_value,
                    )
                )
            for result in results:
                try:
                    result.result()
                except Exception:
                    logger.exception("Error in activating the node")

    def _traverse(
        self,
        node: Node,
        steps_left: int,
    ):
        """Traverse the graph starting from the given node.

        Args:
            node (Node): Starting node
            steps_left (int): Number of steps left to traverse
        """
        if steps_left == 0:
            logger.warning(f"Reached max steps at the {node.name}")
            return

        cur_step = self.__max_steps - steps_left

        for edge in self.__graph.get_adjacent_edges(node):

            priority_value = (self.decay_factor ** (cur_step)) * edge.weight

            if not self._is_traversable(node, edge.node_b, priority_value):
                continue

            # populate the queue with the edge weight and the node
            logger.trace(
                f"Pushing {node.name} -> {edge.node_b.name} to the queue: {priority_value}"
            )
            self.__activation_queue.put(
                (
                    # queue is sorted by cur_step, then by priority_value
                    # so we want the lowest step and the highest priority value to be at the top
                    cur_step,
                    priority_value * -1,
                    node,
                    edge.node_b,
                )
            )

            self._traverse(edge.node_b, steps_left - 1)

    def create_priority_queue(self):
        # find all nodes that have non-zero value, sort them by value

        with ThreadPoolExecutor(self.__n_proc) as pool:
            results = []
            for node in graph_ops.__graph.nodes:
                if node.value != 0:
                    logger.trace(f"Starting traversal from node {node.name}")
                    results.append(
                        pool.submit(
                            self._traverse,
                            node=node,
                            steps_left=self.__max_steps - 1,
                        )
                    )
            for result in results:
                try:
                    result.result()
                except Exception:
                    logger.exception("Error in traversing the graph")
