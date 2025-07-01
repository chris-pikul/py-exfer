import base64
from io import BytesIO
from typing import Sequence, Union
from PIL import Image
from PIL.Image import Image as ImageType


def to_image(obj: Union[str, ImageType]) -> ImageType:
    """Ensures the given argument is returned as a `PIL.Image`. If a string is provided,
    it is treated as a filepath and the image will be loaded. Otherwise the object is
    returned as it is.

    Args:
        obj (Union[str, ImageType]): Either a filepath to an image, or the image itself.

    Raises:
        TypeError: If an invalid type was provided as an argument.

    Returns:
        ImageType: Image data.
    """
    if isinstance(obj, str):
        return Image.open(obj)
    elif isinstance(obj, Image.Image):
        return obj
    else:
        raise TypeError(f"Unsupported type: {type(obj)}")


def encode_image(img: ImageType, as_data: bool = False) -> str:
    """Encodes the given image as a Base64 encoded string. Optionally includes the
    data URI formatting.

    Args:
        img (ImageType): Image to encode.
        as_data (bool, optional): Whether to format as a data URI. Defaults to False.

    Returns:
        str: Encoded image string.
    """
    buffer = BytesIO()
    img_format = "PNG"
    img.save(buffer, format=img_format)
    b64_bytes = base64.b64encode(buffer.getvalue()).decode("utf-8")
    if as_data:
        return f"data:image/{img_format.lower()};base64,{b64_bytes}"
    return b64_bytes


def encode_images(
    images: Union[str, ImageType, Sequence[Union[str, ImageType]]],
    as_data: bool = False,
) -> list[str]:
    """Encodes one or more images or filepaths to images, as Base64 strings with
    optional data URI formatting.

    Args:
        images (Union[str, ImageType, Sequence[Union[str, ImageType]]]): Either an image, a list of images, a path to an image, or a list of paths to images.
        as_data (bool, optional): Whether to format the results as data URIs. Defaults to False.

    Returns:
        list[str]: List of Base64 encoded strings.
    """
    if isinstance(images, (str, Image.Image)):
        images = [images]
    return [encode_image(to_image(img), as_data) for img in images]
