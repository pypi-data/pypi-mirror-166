import abc
from typing import TYPE_CHECKING

import numpy as np
from docarray import Document

if TYPE_CHECKING:
    from docarray.typing import DocumentContentType


_CHANNEL_LAST = [-1, 2]


class BasePreprocess(abc.ABC):
    @abc.abstractmethod
    def __call__(self, doc: Document) -> 'DocumentContentType':
        ...


class DefaultPreprocess(BasePreprocess):
    """
    Default built-in preprocess class to unpack the content from a ``Document`` object.
    """

    def __call__(self, doc: Document) -> 'DocumentContentType':
        """
        Returns the content of a ``Document`` object.

        :param doc: A docarray ``Document`` object.
        :return: Content of the input document.
        """
        return doc.content


class TextPreprocess(DefaultPreprocess):
    """
    Default built-in preprocess class to unpack the text from a ``Document`` object.
    """

    pass


class VisionPreprocess(BasePreprocess):
    """
    Built-in preprocess class for ``Document`` objects holding image data. It
    transforms an image given by a URI or a tensor into a tensor which can be passed
    into an image embedding model.
    If the image is passed as an int8 tensor or a URI, normalization is applied.
    If the image is passed as a float32 tensor, normalization is omitted.

    :param height: The target height of the image.
    :param width: The target width of the image.
    :param channel_axis: The default channel axis of the image. After preprocess will be
      set to 0 (C * H * W).
    :param augmentation: If `True`, apply random augmentation for the image content.
    """

    def __init__(
        self,
        height: int = 224,
        width: int = 224,
        channel_axis: int = -1,
        augmentation: bool = False,
    ):
        self._height = height
        self._width = width
        self._channel_axis = channel_axis
        self._augmentation = augmentation

    def __call__(self, doc: Document) -> np.ndarray:
        """
        Unpacks and preprocesses the content of a ``Document`` object with image
        content.

        :param doc: A docarray ``Document`` object.
        :return: Preprocessed tensor content of the input document.
        """
        current_channel_axis = self._channel_axis
        doc = Document(doc, copy=True)
        if doc.tensor is None:
            if doc.uri:
                doc.load_uri_to_image_tensor(
                    width=self._width,
                    height=self._height,
                    channel_axis=self._channel_axis,
                )
            else:
                raise AttributeError(
                    f'Document `tensor` is None, loading it from url: {doc.uri} failed.'
                )
        doc.set_image_tensor_shape(
            shape=(self._height, self._width), channel_axis=self._channel_axis
        )
        # Normalize image as np.float32.
        if doc.tensor.dtype in [np.int8, np.uint8]:
            doc.tensor = doc.tensor.astype(np.uint8)
            doc.set_image_tensor_normalization(channel_axis=self._channel_axis)
        elif doc.tensor.dtype == np.float64:
            doc.tensor = np.float32(doc.tensor)
        if self._augmentation:
            import albumentations as A

            if self._channel_axis not in _CHANNEL_LAST:
                # if image is not channel_last, move C to last axis.
                # This is required for albumentations.
                doc.set_image_tensor_channel_axis(self._channel_axis, _CHANNEL_LAST[0])
                current_channel_axis = _CHANNEL_LAST[0]

            transform = A.Compose(
                [
                    A.HorizontalFlip(p=0.5),
                    A.ColorJitter(p=1),
                    A.RandomResizedCrop(width=self._width, height=self._height, p=1),
                    A.GaussianBlur(p=1),
                    A.GridDropout(
                        ratio=0.2, p=0.5
                    ),  # random erase 0.2 percent of image with 0.5 probability
                ]
            )
            doc.tensor = transform(image=doc.tensor)['image']

        # Set image channel axis to pytorch default channel 0.
        doc.set_image_tensor_channel_axis(current_channel_axis, 0)

        return doc.tensor
