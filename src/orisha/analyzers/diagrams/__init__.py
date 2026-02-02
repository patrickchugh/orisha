"""Diagram tool adapters (Principle V: Tool Agnosticism).

All diagram adapters output CanonicalArchitecture format.
"""

from orisha.analyzers.diagrams.base import DiagramGenerator
from orisha.analyzers.diagrams.terravision import TerravisionAdapter

__all__ = ["DiagramGenerator", "TerravisionAdapter"]
