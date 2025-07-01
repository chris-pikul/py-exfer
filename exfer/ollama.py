from typing import Generator, Optional, Sequence, Union
from PIL.Image import Image

from .provider import Provider
from .model import Model
from .capabilities import Capability
from .utils import ping, encode_images


class Ollama(Provider):
    @staticmethod
    def check_env() -> bool:
        return ping("http://localhost:11434/api/version")

    @classmethod
    def from_env(cls):
        return cls()

    def __init__(self, url_override: str | None = None):
        super().__init__(base_url=url_override)

    @property
    def key(self) -> str:
        return "ollama"

    @property
    def name(self) -> str:
        return "Ollama"

    @property
    def capabilities(self) -> list[Capability]:
        return [Capability.TEXT]

    def _default_base_url(self) -> str:
        return "http://localhost:11434"

    def _make_generate_request(
        self,
        model: Union[str, Model],
        prompt: str,
        system_prompt: Optional[str] = None,
        images: Optional[Union[str, Image, Sequence[Union[str, Image]]]] = None,
        stream: bool = False,
    ) -> dict:
        capabilities = [Capability.TEXT]
        if images is not None:
            capabilities.append(Capability.VISION)

        model = self.get_model(model, capabilities)

        request: dict = {
            "model": model.key,
            "prompt": prompt,
            "stream": stream,
        }
        if system_prompt is not None:
            request["system"] = system_prompt
        if images is not None:
            request["images"] = encode_images(images)

        return request

    def _generate_sync(
        self,
        model: Union[str, Model],
        prompt: str,
        system_prompt: Optional[str] = None,
        images: Optional[Union[str, Image, Sequence[Union[str, Image]]]] = None,
    ) -> str:
        request = self._make_generate_request(
            model, prompt, system_prompt, images, False
        )
        return ""

    def _generate_async(
        self,
        model: str | Model,
        prompt: str,
        system_prompt: str | None = None,
        images: Optional[Union[str, Image, Sequence[Union[str, Image]]]] = None,
    ) -> Generator[str, None, None]:
        request = self._make_generate_request(
            model, prompt, system_prompt, images, True
        )
        yield ""
