"""Orisha template rendering (Principle II: Reproducibility).

This module provides Jinja2-based template rendering with deterministic output.
Templates are designed to produce identical output for identical input.
"""

from orisha.templates.renderer import DocumentRenderer, SectionLoader

__all__ = ["DocumentRenderer", "SectionLoader"]
