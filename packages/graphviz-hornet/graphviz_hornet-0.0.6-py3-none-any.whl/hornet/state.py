"""States for graphs."""
import graphviz as _graphviz

from hornet.protocol import (
    DigGraphProtocol,
    SubGraphProtocol,
)

_state: list[DigGraphProtocol | SubGraphProtocol] = []

_last_cluster_id = 0


def generate_cluster_id() -> int:
    """Generate a cluster id."""
    global _last_cluster_id
    result = _last_cluster_id
    _last_cluster_id += 1
    return result


def put_diggraph(graph: DigGraphProtocol):
    """Put a diggraph to state."""
    _state.append(graph)


def get_digraph() -> _graphviz.Digraph:
    """Get the current digraph."""
    return _state[-1].digraph


def get_inner_graph() -> _graphviz.Digraph:
    """Return the most inner graph."""
    if not _state:
        raise RuntimeError("Unexpected state.")
    return _state[-1].digraph


def remove_digraph(graph: DigGraphProtocol):
    """Remove a graph."""
    if _state[-1] is not graph:
        raise RuntimeError("Unexpected state.")
    _state.pop()


def remove_subgraph(graph: SubGraphProtocol):
    """Remove a graph."""
    if _state[-1] is not graph:
        raise RuntimeError("Unexpected state.")
    _state.pop()


def select_edge_holder(
    digraph1: _graphviz.Digraph, digraph2: _graphviz.Digraph
) -> _graphviz.Digraph:
    """Return one of the two parameters that shall own edges."""
    order = []
    for digraph in _state[::-1]:
        for param in [digraph1, digraph2]:
            if digraph.has(param):
                order.append((digraph, param))

    if len(order) == 1:
        return order[0][1]
    elif len(order) == 2:
        if order[0][0].is_cluster:
            return order[1][1]
        else:
            return order[0][1]
    else:
        raise RuntimeError("Out of context.")
