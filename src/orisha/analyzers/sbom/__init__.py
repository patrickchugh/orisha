"""SBOM tool adapters (Principle V: Tool Agnosticism).

All SBOM adapters output CanonicalSBOM format.
"""

from orisha.analyzers.sbom.base import SBOMAdapter
from orisha.analyzers.sbom.syft import SyftAdapter

__all__ = ["SBOMAdapter", "SyftAdapter"]
