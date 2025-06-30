from enum import StrEnum


class Capability(StrEnum):
    """Enumeration of a providers/models capabilities regarding the type of inference it offers."""

    TEXT = "TEXT"
    """Allows for text generation."""
