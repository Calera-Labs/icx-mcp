"""Calera Agent Memory SDK — Plug-and-Play Epistemic Memory for AI Agents."""

from .client import CaleraMemoryClient
from .langchain_memory import CaleraMemorySubstrate

__version__ = "0.4.0"
__all__ = ["CaleraMemoryClient", "CaleraMemorySubstrate"]
