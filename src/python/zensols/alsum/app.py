"""Summarize text using Component ALignment Abstract Meaning Representation
(CALAMR) alignment.

"""
__author__ = 'Paul Landes'

from dataclasses import dataclass, field
import logging
from zensols.persist import Stash

logger = logging.getLogger(__name__)


@dataclass
class Application(object):
    """Summarize text using Component ALignment Abstract Meaning Representation
    (CALAMR) alignment.

    """
    reduced_graph_stash: Stash = field()
    """CRUDs instances of :class:`~.flow.FlowGraphResult`."""

    def render(self, key: str, prune: bool = True):
        """Render the reduced graph.

        :param key: the corpus key identifying the graph to render

        :param prune: whether or not to prune 0-flow edges

        """
        from .graph import ReducedGraph
        self.reduced_graph_stash.prune = prune
        flow: ReducedGraph = self.reduced_graph_stash[key]
        flow.render()
