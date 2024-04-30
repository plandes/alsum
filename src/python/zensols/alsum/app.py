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
    flow_graph_stash: Stash = field()
    """CRUDs instances of :class:`~.flow.FlowGraphResult`."""

    def render(self, key: str, prune: bool = True):
        """Render the reduced graph.

        :param key: the corpus key identifying the graph to render

        :param prune: whether or not to prune 0-flow edges

        """
        from .flow import FlowGraphData
        self.flow_graph_stash.prune = prune
        flow: FlowGraphData = self.flow_graph_stash[key]
        flow.render()


@dataclass
class PrototypeApplication(object):
    CLI_META = {'is_usage_visible': False}

    app: Application = field()

    def _tmp(self):
        from .flow import FlowGraphData
        self.app.flow_graph_stash.prune = False
        flow: FlowGraphData = self.app.flow_graph_stash['earthquake']
        flow.render()

    def proto(self, run: int = 0):
        """Prototype test."""
        {
            0: self._tmp,
            1: lambda: self.app.render('earthquake'),
         }[run]()
