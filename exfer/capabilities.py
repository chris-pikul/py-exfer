from enum import StrEnum


class Capability(StrEnum):
    """Enumeration of a providers/models capabilities regarding the type of inference it offers."""

    TEXT = "TEXT"
    """Allows for text generation."""

    TTS = "TTS"
    """Text-to-Speech for generating spoken audio from given text. """

    STT = "STT"
    """Speech-to-Text for transcribing given audio speech into text. """

    IMAGE = "IMAGE"
    """Generates images from a given text prompt. """

    VISION = "VISION"
    """Describing or using images within the model for textual output. """

    AUDIO = "AUDIO"
    """General purpose audio generation for things like music and sound effects. """

    VIDEO = "VIDEO"
    """Generate video snippets from a given text prompt. """

    REASONING = "REASONING"
    """Allows the model to self-optimize for generation tasks. """

    TOOLS = "TOOLS"
    """Usage of tool calling by the model to help in accomplishing a given task. """


class CapabilitiesException(Exception):
    pass
