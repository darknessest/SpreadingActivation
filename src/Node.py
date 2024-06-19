from SchemaType import SchemaType
from threading import Lock


class Node:
    def __init__(self, weight: float, _type: SchemaType, name: str) -> None:
        self.weight = weight
        self._value: float = 0
        self.__value_lock = Lock()
        self.value_lock_ext = Lock()
        self.type: SchemaType = _type
        self.name: str = name

    @property
    def value(self) -> float:
        with self.__value_lock:
            return self._value

    @value.setter
    def value(self, value: float) -> None:
        with self.__value_lock:
            self._value = value

    def __repr__(self) -> str:
        # include the weight, value, and type of the node
        # and list the names of the nodes it is connected to
        return (
            "Node("
            f"{self.name=}, {self.weight=:.4f}, {self.value=:.4f}, {self.type=}"
            ")"
        )

    def __str__(self) -> str:
        return (
            "Node("
            f"{self.name!r}, {self.weight:.4f}, {self.value:.4f}, {self.type}"
            ")"
        )

    def __eq__(self, other) -> bool:
        # compare the edges and weight of the nodes
        if not isinstance(other, Node):
            return NotImplemented("Cannot compare Node with non-Node type")

        return (
            self.weight == other.weight
            and self.type == other.type
            and self.name == other.name
            and self.value == other.value
        )

    def __hash__(self) -> int:
        return hash((self.weight, self.type, self.name))
