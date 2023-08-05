"""Expose the node."""
import typing
import graphviz as _graphviz
from hornet import state as _state


class Node:
    """Represent a node."""

    def __init__(self, identity: str, attrs: dict = {}):
        """Put a node in a graph."""
        self.identity = identity
        self.digraph: _graphviz.Digraph = _state.get_digraph()
        self.digraph.node(self.identity, None, attrs)

    def __lshift__(
        self, other: "Node" | typing.Iterable["Node"] | typing.Iterator["Node"]
    ) -> "Node":
        """Add an edge from `other` to `self`."""
        nodes = other
        if hasattr(other, "__iter__"):
            result = None
            nodes = other
        else:
            result = other
            nodes = [other]

        for node in nodes:
            self._select_edge_holder(node).edge(node.identity, self.identity)

        return result

    def __rlshift__(
        self, others: typing.Iterable["Node"] | typing.Iterator["Node"]
    ) -> "Node":
        """Add an edge from `self` to `others`."""
        # [nodes] << node
        self >> others
        return self

    def __rshift__(
        self, other: "Node" | typing.Iterable["Node"] | typing.Iterator["Node"]
    ) -> "Node":
        """Add an edge from `self` to `other`."""
        nodes = other
        if hasattr(other, "__iter__"):
            result = None
            nodes = other
        else:
            result = other
            nodes = [other]

        for node in nodes:
            self._select_edge_holder(node).edge(
                self.identity,
                node.identity,
            )
        return result

    def __rrshift__(
        self, others: typing.Iterator["Node"] | typing.Iterable["Node"]
    ) -> "Node":
        """Add edges from `others` to `self`."""
        # [others] >> self
        self << others
        return self

    def __sub__(self, other: "Node") -> "Node":
        """Implement - ."""
        self._select_edge_holder(other).edge(
            self.identity,
            other.identity,
            None,
            arrowhead="none",
            arrowtail="none",
        )
        return other

    def _select_edge_holder(self, other: "None") -> _graphviz.Digraph:
        """Return the `inner` digraph of `self` or `other`."""
        return _state.select_edge_holder(self.digraph, other.digraph)
