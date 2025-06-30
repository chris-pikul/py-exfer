from .capabilities import Capability
from .model import Model


class BaseProvider:
    """Base class for further providers which provide inference from an external API."""

    key: str
    """Unique URL-safe key for this provider. Should be lower kebab-case and uses only ASCII characters."""

    name: str
    """Human-friendly displayable name for this provider."""

    base_url: str
    """Base url for the provider in which API endpoints will be appended to. Should follow standard HTTP protocol and domain name. Does not need the ending slash."""

    capabilities: list[Capability] = []
    """List of capabilities the provider can offer. Will be used by a global provider class to choose the right provider for a given task."""

    models: dict[str, Model] = {}
    """Dictionary mapping model keys to their model definition. These are the available models within a given provider."""

    def path(self, *segments: str) -> str:
        """Combine the given segments and prefix it with this models `base_url` to form a complete URL. Does not perform splitting if the components contain their own slashes, but it will ensure that they are all separated by a slash.

        Args:
            *segments (str): Variadic list of strings to combine with the base_url.

        Returns:
            str: URL path including the `base_url` and all segments combined with forward-slashes.
        """
        result = self.base_url.rstrip("/")
        for seg in segments:
            result += seg + "/" if not seg.startswith("/") else seg
        return result

    def has_capability(
        self, capability: str | Capability | list[str | Capability]
    ) -> bool:
        """Check if this provider has a given capability. Accepts either a single argument, or a list of capabilities. In the case of a list, each entry must match to return true (AND).

        Args:
            capability (str | Capability | list[str  |  Capability]): Individual, or a list, of capabilities to test for.

        Returns:
            bool: True if the capability (or all capabilities) are provided by this provider.
        """

        if isinstance(capability, list):
            for cap in capability:
                if not self.has_capability(cap):
                    return False
            return True
        elif isinstance(capability, str):
            capability = Capability(capability)

        for cap in self.capabilities:
            if cap == capability:
                return True
        return False

    def register_model(self, model: Model) -> None:
        """Adds or replaces a model within this provider. Uses the `model.key` field to set the `Model` within this provider's `models` dictionary. If the key already exists it will be replaced.

        Args:
            model (Model): Given model to register

        Raises:
            Exception: if the key field within the given model argument is empty
        """
        if model.key == "":
            raise Exception("cannot register model with an empty/unset key field")
        self.models[model.key] = model
