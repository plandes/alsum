"""Utility classes for discovering graph based data from an aligned document.

"""
__author__ = 'Paul Landes'

from typing import Tuple, List, Dict, Iterable
from dataclasses import dataclass, field
import logging
from igraph import Vertex, Edge
from zensols.config import Dictable
from zensols.persist import persisted, Stash, ReadOnlyStash, PrimeableStash
from zensols.calamr import (
    GraphNode, GraphEdge, DocumentGraph, DocumentGraphEdge, TerminalGraphEdge,
    FlowGraphResult
)
from zensols.calamr.render.base import RenderContext, GraphRenderer, rendergroup

logger = logging.getLogger(__name__)


@dataclass
class FlowGraphData(Dictable):
    """A utility class to analyze an aligned graph.

    """
    renderer: GraphRenderer = field(repr=False)
    """Used to render the :obj:`graph_result`."""

    child_graph_name: str = field()
    """The target graph name to analyze used in :obj:`child_doc_graph`."""

    key: str = field()
    """The stash key used in uniquely identify :obj:`graph_result` used in
    reporting.

    """
    graph_result: FlowGraphResult = field()
    """The flow graph data."""

    prune: bool = field()
    """Whether :obj:`doc_graph` will have 0-flow edges pruned."""

    def _delete_terminals(self, doc_graph: DocumentGraph):
        """Remove the source (S) and sink (T) nodes and their flow edges."""
        edges: Iterable[GraphEdge] = filter(
            lambda e: isinstance(e, TerminalGraphEdge), doc_graph.es.values())
        doc_graph.delete_edges(edges, True)

    def _prune_graph(self, doc_graph: DocumentGraph):
        """Remove all 0-flow links, except for document edges in the source
        since the source component in the reversed source graph have no flow
        between its root and sentence nodes.

        """
        def to_str(e: Edge) -> str:
            """Logging."""
            ge: GraphNode = doc_graph.edge_by_id(e.target)
            gnt: GraphNode = doc_graph.node_by_id(e.target)
            gns: GraphNode = doc_graph.node_by_id(e.source)
            return f'{gns} -> f={ge.flow} {gnt}'

        # populated with what to delete
        to_del: List[GraphEdge] = []
        # source igraph edge IDs to to avoid remove the component's doc edges
        src_edges: Dict[int, int] = doc_graph.components_by_name['source'].\
            graph_edge_id_to_edge_ref
        # 0-flow deletion candidates
        edges: Iterable[Tuple[Edge, GraphEdge], ...] = filter(
            lambda e: e[1].flow == 0, doc_graph.es.items())
        e: Edge
        ge: GraphEdge
        for e, ge in edges:
            # parent vertex and graph node
            pv: Vertex = doc_graph.vertex_ref_by_id(e.target)
            pgn: GraphNode = doc_graph.to_node(pv)
            # children edges of parent vertex (reverse flow so outgoing)
            nes: List[Edge] = pv.incident('out')
            # max flow from all children edges
            max_child_flow: int = 0
            # if not a terminal connected, find the max flow (if any) from them
            if len(nes) > 0:
                max_child_flow = max(map(
                    lambda e: doc_graph.edge_by_id(e.target).flow, nes))
            # reversed source doc nodes have no flow, but their children might
            is_doc_edge: bool = isinstance(ge, DocumentGraphEdge)
            is_src: bool = ge.id in src_edges
            # TODO: doc edges that should be deleted with children flow are not
            if not is_src or not is_doc_edge:
                if logger.isEnabledFor(logging.DEBUG):
                    ids = ', '.join(map(to_str, nes))
                    logger.debug(
                        f'deleting: id={ge.id} ({type(ge).__name__}, ' +
                        f'f={ge.flow}, mf={max_child_flow}, '
                        f'par: {pgn} ({pgn.id}), neigh={ids}')
                to_del.append(ge)
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'pruning {len(to_del)} edges')
        doc_graph.delete_edges(to_del, True)

    @property
    def child_doc_graph(self) -> DocumentGraph:
        """The target aligned bipartite child document graph before any
        modification.

        """
        return self.graph_result.doc_graph.children[self.child_graph_name]

    @property
    @persisted('_doc_graph')
    def doc_graph(self) -> DocumentGraph:
        """A non-reversed (nascent direction) graph without terminal nodes or
        edges.

        """
        doc_graph: DocumentGraph = self.child_doc_graph.clone(
            reverse_edges=True, deep=True)
        # remove terminal nodes and edges
        self._delete_terminals(doc_graph)
        # optionally prune the graph
        if self.prune:
            self._prune_graph(doc_graph)
        return doc_graph

    def render(self, include_child: bool = False):
        """Render :obj:`doc_graph` and optionally :obj:`child_doc_graph`.

        :param include_child: if ``True`` render :obj:`child_doc_graph`

        """
        child_title: str = self.child_graph_name.replace('_', ' ').capitalize()
        head: str = 'Pruned Graph' if self.prune else 'Reduced'
        ctxs: List[RenderContext] = []
        if include_child:
            ctxs.append(RenderContext(
                doc_graph=self.child_doc_graph,
                heading=f'{child_title} ({self.key})'))
        ctxs.append(RenderContext(
            doc_graph=self.doc_graph,
            heading=head))
        with rendergroup(self.renderer) as rg:
            ctx: RenderContext
            for ctx in ctxs:
                rg(ctx)


@dataclass
class FlowGraphDataStash(ReadOnlyStash):
    """CRUDs instances of :class:`.FlowGraphResult`.

    """
    factory: Stash = field()
    """A stash that CRUDs :class:`.FlowGraphResult`."""

    renderer: GraphRenderer = field(repr=False)
    """Used to render the :obj:`graph_result`."""

    child_graph_name: str = field()
    """The target graph name to analyze used in :obj:`child_doc_graph`."""

    prune: bool = field()
    """Whether :obj:`FlowGraphData.doc_graph` will have 0-flow edges pruned."""

    def load(self, name: str) -> FlowGraphData:
        res: FlowGraphResult = self.factory.load(name)
        if res is not None:
            return FlowGraphData(
                renderer=self.renderer,
                child_graph_name=self.child_graph_name,
                key=name,
                graph_result=res,
                prune=self.prune)

    def keys(self) -> Iterable[str]:
        return self.factory.keys()

    def exists(self, name: str) -> bool:
        return self.factory.exists(name)
