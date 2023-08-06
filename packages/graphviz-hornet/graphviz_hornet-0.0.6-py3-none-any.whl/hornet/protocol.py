"""Define protocols."""
import typing
import graphviz as graphviz


class NodeProtocol(typing.Protocol):
    """Interface of a node."""

    @property
    def identity(self) -> str:
        """ID of a node."""


class SubGraphProtocol(typing.Protocol):
    """Represent a subgraph."""


class DigGraphProtocol(typing.Protocol):
    """Represent a digraph."""

    def has(self, digraph: graphviz.Digraph) -> bool:
        """Return `True` if this instance holds `digraph`."""

    def is_cluster(self) -> bool:
        """Return `True` if this instance is a cluster."""
