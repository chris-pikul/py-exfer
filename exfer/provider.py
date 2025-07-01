from abc import ABC, abstractmethod
from typing import Generator, Literal, Optional, Union, overload

from .capabilities import Capability
from .model import Model


class Provider(ABC):
    """Abstract Base Class for further providers which provide inference from an external API."""

    base_url: str
    """Base url for the provider in which API endpoints will be appended to. Should follow standard HTTP protocol and domain name. Does not need the ending slash."""

    models: dict[str, Model] = {}
    """Dictionary mapping model keys to their model definition. These are the available models within a given provider."""

    @staticmethod
    @abstractmethod
    def check_env() -> bool:
        """Check if this Provider type might exist based on OS environment.

        Returns:
            bool: True if we believe there are settings or availability for this provider type.
        """
        ...

    @classmethod
    @abstractmethod
    def from_env(cls):
        """Construct a new instance of this Provider type based on environment settings.
        Should use `Provider.check_env()` first to ensure it is possible."""
        return cls()

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or self._default_base_url()

    @property
    @abstractmethod
    def key(self) -> str:
        """Unique URL-safe key for this provider. Should be lower kebab-case and uses only ASCII characters."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-friendly displayable name for this provider."""
        ...

    @property
    @abstractmethod
    def capabilities(self) -> list[Capability]:
        """List of capabilities the provider can offer. Will be used by a global provider class to choose the right provider for a given task."""
        ...

    @abstractmethod
    def _default_base_url(self) -> str:
        """Return the default base URL for this provider."""
        ...

    @property
    def models_list(self) -> list[Model]:
        """The available models in this Provider returned as a list."""
        return [model for model in self.models.values()]

    @property
    def models_set(self) -> set[Model]:
        return set(self.models_list)

    def __eq__(self, other):
        if isinstance(other, Provider):
            return self.key == other.key
        elif type(other) is str:
            return self.key == other
        return False

    def __hash__(self):
        return hash((self.key, self.base_url))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Provider#{self.key}"

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

    @overload
    def generate(
        self,
        model: Union[str, Model],
        prompt: str,
        stream: Literal[False] = False,
        system_prompt: Optional[str] = None,
    ) -> str: ...

    @overload
    def generate(
        self,
        model: Union[str, Model],
        prompt: str,
        stream: Literal[True],
        system_prompt: Optional[str] = None,
    ) -> Generator[str]: ...

    def generate(
        self,
        model: Union[str, Model],
        prompt: str,
        stream: bool = False,
        system_prompt: Optional[str] = None,
    ) -> Union[str, Generator[str]]:
        """Generate a text completion. Requires that the model supports `Compatibility.TEXT`.

        Args:
            model (str | Model): Key for the model to use, or the actual model card.
            prompt (str): Given prompt string to provide as user context.
            stream (bool, optional): Whether to use streaming. Defaults to False.
            system_prompt (str, optional): An additional top-level system prompt to inject into the context. Defaults to None.

        Returns:
            Union[str, Generator[str]]: Either the complete response, or a generator which yields fragments (requires stream = True).
        """
        if stream:
            return self._generate_async(model, prompt, system_prompt)
        return self._generate_sync(model, prompt, system_prompt)

    @abstractmethod
    def _generate_sync(
        self, model: Union[str, Model], prompt: str, system_prompt: Optional[str] = None
    ) -> str: ...

    @abstractmethod
    def _generate_async(
        self, model: Union[str, Model], prompt: str, system_prompt: Optional[str] = None
    ) -> Generator[str]: ...
