import abc
from typing import TYPE_CHECKING, Any, List

import numpy as np

if TYPE_CHECKING:
    from docarray.typing import DocumentContentType


class BaseCollate(abc.ABC):
    @abc.abstractmethod
    def __call__(self, inputs: List['DocumentContentType']) -> Any:
        ...


class DefaultCollate(BaseCollate):
    """
    Default built-in collate class to create batch from a list of inputs for an
    embedding model.
    """

    def __call__(self, inputs: List['DocumentContentType']) -> Any:
        """
        Constructs a batch to pass into the embedding model from a list of contents.

        :param inputs: List of content objects to pass into the embedding model.
        :return: Any type of object that can be fed to an embedding model.
        """
        if isinstance(inputs[0], str):
            return inputs
        else:
            from torch.utils.data._utils.collate import default_collate

            return default_collate(inputs)


class TransformersCollate(BaseCollate):
    """
    Built-in collate class which applies a HuggingFace's transformer ``AutoTokenizer``
    on the given text inputs.

    :param name: The model id of a pretrained huggingface tokenizer or a path to a
        directory with the weights.
    :param padding: Set to True if padding should be applied during tokenization.
    :param kwargs: Keyword arguments to pass to the call of the ``AutoTokenizer``.
    """

    def __init__(self, name: str = 'bert-base-cased', padding: bool = True, **kwargs):
        from transformers import AutoTokenizer

        self._tokenizer = AutoTokenizer.from_pretrained(name)
        self._padding = padding
        self._kwargs = kwargs

    def __call__(self, inputs: List[str]):
        """
        Creates a ``BatchEncoding`` object from a list of input text values for the
        tokenizer.

        :param inputs: List of text values provied for the tokenization.
        :return: ``BatchEncoding`` objects to pass into a HuggingFace transformer
            embedding model.
        """
        return self._tokenizer(
            inputs, padding=self._padding, return_tensors='pt', **self._kwargs
        )


class VisionTransformersCollate(BaseCollate):
    """
    Built-in collate class which applies a HuggingFace's transformer
    ``AutoFeatureExtractor`` model on the given input image tensors.

    :param name: The model id of a pretrained HuggingFace model or a path to a
        directory with the model weights.
    :param kwargs: Keyword arguments to pass to the call of the feature extractor.
    """

    def __init__(self, name: str = 'openai/clip-vit-base-patch32', **kwargs):
        from transformers import AutoFeatureExtractor

        self._processor = AutoFeatureExtractor.from_pretrained(name)
        self._kwargs = kwargs

    def __call__(self, inputs: List[np.ndarray]):
        """
        Creates a ``BatchFeature`` object from a list of tensor values for the
        feature extractor.

        :param inputs: List tensors to pass into the feature extractor.
        :return: ``BatchFeature`` objects to pass into a vision transformer encoder
            model.
        """
        return self._processor(images=inputs, return_tensors='pt', **self._kwargs)


class OpenCLIPTextCollate(BaseCollate):
    """
    Built-in collate class which applies the tokenizer of OpenCLIP on the given text
    inputs.
    """

    def __init__(self):
        from open_clip import tokenize

        self._tokenize = tokenize

    def __call__(self, inputs: List[str]) -> 'torch.LongTensor':  # noqa: F821
        """
        Creates a tensor with a list of token ids for each text sequence passed to the
        collate function.
        """
        return self._tokenize(inputs)
