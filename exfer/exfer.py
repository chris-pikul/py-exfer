from typing import Optional, Union
from .provider import Provider
from .model import Model

from .ollama import Ollama
from .lmstudio import LMStudio


class Exfer:
    """Class which holds data-structures for managing and mapping different providers and models."""

    providers: dict[str, Provider] = {}
    """Dictionary of available providers which have been setup and can be used for further requests. Key is the provider's key, and the value is the provider itself. """

    models: set[Model] = set()
    """List of all available models that have been propagated from the providers. """

    model_providers: dict[str, Union[str, set[str]]] = {}
    """Mapping dictionary of all model-keys to their respective providers. The key is the model key, and the value is an ordered list of the providers that can use them. """

    @classmethod
    def from_env(cls):
        """Constructs a new Exfer instance. Will attempt to automatically populate the providers based
        on the process environment. For local providers it will ping the common ports and known API endpoints
        to check for existence. For external third-party providers it will iterate the environment variables
        for commonly known API keys and connection settings.

        See: Exfer.populate_from_env() for implementation details.

        Returns:
            Exfer: pre-populated Exfer instance.
        """
        instance = cls()
        instance.populate_from_env()
        return instance

    def __init__(self, providers: list[Provider] = []):
        """Constructs a new Exfer instance. Each provider given (optional) will be registered, including
        all of it's constituent Models it provides for. These will be deduplicated.

        Args:
            providers (list[Provider], optional): List of providers to register. Defaults to [].
        """
        for provider in providers:
            self.register_provider(provider)

    def _add_model(self, model: Model, provider_key: str) -> None:
        """Adds a model to the internal `self.models` and `self.model_providers` mappings while maintaining the data types and uniqueness."""
        self.models.add(model)
        if model.key in self.model_providers:
            current = self.model_providers[model.key]
            if type(current) is set:
                current.add(provider_key)
            elif type(current) is str:
                self.model_providers[model.key] = set([current, provider_key])
        else:
            self.model_providers[model.key] = provider_key

    def _remove_model(self, model: Union[str, Model]) -> None:
        """Removes a model from the internal `self.models` and `self.model_providers` mappings."""
        self.models = {existing for existing in self.models if existing != model}

        key = model.key if isinstance(model, Model) else model
        if key in self.model_providers:
            current = self.model_providers[key]
            if type(current) is set:
                current.remove(key)
                if len(current) == 1:
                    current = current.pop()
                self.model_providers[key] = current
            elif type(current) is str:
                del self.model_providers[key]

    def register_provider(self, provider: Provider) -> bool:
        """Adds a provider and all of the models it provides to the internal mappings. This will deduplicate based on the keys.

        Args:
            provider (Provider): The provider to add.

        Returns:
            bool: True if the addition was a new registration that did not exist before, False if it already existed.
        """
        exists = provider.key in self.providers
        if exists:
            # We need to remove the previous entries since this provider is being overridden.
            self.unregister_provider(provider)

        # Register the provider to the key
        self.providers[provider.key] = provider

        # Add any models it provides
        for model in provider.models_list:
            self._add_model(model, provider.key)

        return not exists

    def unregister_provider(self, provider: Union[str, Provider]) -> bool:
        """Removes a provider and deregisters all the models it provided.

        Args:
            provider (Union[str, Provider]): Either the key of the provider, or the Provider object itself.

        Returns:
            bool: True if the provider did exist and was removed, False if it did not.
        """
        key = provider.key if isinstance(provider, Provider) else provider
        if key in self.providers:
            # First we need to remove any models it registered.
            for model in self.providers[key].models_list:
                self._remove_model(model)

            # Then we can delete the provider entry
            del self.providers[key]

            # Return true to indicate it did exist.
            return True
        return False

    def populate_from_env(self):
        """Populates this `Exfer` instance will all the known available providers by checking the current system environment.

        For local providers like `LMStudio`, `Ollama`:
            Will check if the common ports are open and responding to their known API endpoints.

        For external providers like `OpenAI`, `Google`, `Anthropic`, etc:
            Checks for environment variables that commonly hold their API keys.
        """
        if LMStudio.check_env():
            self.register_provider(LMStudio.from_env())
        if Ollama.check_env():
            self.register_provider(Ollama.from_env())
