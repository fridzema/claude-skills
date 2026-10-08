"""Mechanische controle voor dutch-humanizer. Zie core.analyze."""

from .core import Finding, Report, analyze, check, SCHEMA_VERSION, TASKS
from .markdown import block_spans, parse

__all__ = ["Finding", "Report", "analyze", "check", "block_spans", "parse", "SCHEMA_VERSION", "TASKS"]
