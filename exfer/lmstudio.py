from typing import Generator, Optional, Union

from .provider import Provider
from .model import Model
from .capabilities import Capability
from .utils import ping


class LMStudio(Provider):
    @staticmethod
    def check_env() -> bool:
        return ping("http://localhost:1234/api/v1/models")

    @classmethod
    def from_env(cls):
        return cls()

    def __init__(self, url_override: str | None = None):
        super().__init__(base_url=url_override)

    @property
    def key(self) -> str:
        return "lm-studio"

    @property
    def name(self) -> str:
        return "LM Studio"

    @property
    def capabilities(self) -> list[Capability]:
        return [Capability.TEXT]

    def _default_base_url(self) -> str:
        return "http://localhost:1234"

    def _generate_sync(
        self,
        model: Union[str, Model],
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        return ""

    def _generate_async(
        self, model: str | Model, prompt: str, system_prompt: str | None = None
    ) -> Generator[str, None, None]:
        yield ""
