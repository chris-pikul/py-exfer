from typing import Optional
from .capabilities import Capability


class Model:
    """Individual model that a provider can issue inference for. Contains the information describing the model, and it's capabilities."""

    key: str
    """Unique URL-safe key for this model. Should be lower kebab-case and uses only ASCII characters."""

    name: str
    """Human-friendly displayable name for this provider. Should exclude any version information."""

    version: str = "latest"
    """Version of the model. Suggested format is SEMVER."""

    tag: Optional[str] = None
    """Optional tag that can be used to label quantization methods and bit sizing. """

    capabilities: list[Capability] = []
    """List of capabilities which this model provides. Can be more than one for multi-modal AI providers."""

    def __eq__(self, other):
        if isinstance(other, Model):
            return self.key == other.key
        elif type(other) is str:
            return self.key == other
        return False

    def __hash__(self):
        return hash((self.key, self.version, self.tag))

    def __str__(self):
        result = self.name
        if self.tag is not None and self.tag != "":
            result += ":" + self.tag
        if self.version != "" and self.version != "latest":
            result += "@" + self.version
        return result

    def __repr__(self):
        return f"Model#{self.key}"

    def has_capability(
        self, capability: str | Capability | list[str | Capability]
    ) -> bool:
        """Check if this model has a given capability. Accepts either a single argument, or a list of capabilities. In the case of a list, each entry must match to return true (AND).

        Args:
            capability (str | Capability | list[str  |  Capability]): Individual, or a list, of capabilities to test for.

        Returns:
            bool: True if the capability (or all capabilities) are provided by this model.
        """

        if isinstance(capability, list):
            for cap in capability:
                if not self.has_capability(cap):
                    return False
            return True

        for cap in self.capabilities:
            if cap == capability:
                return True
        return False
