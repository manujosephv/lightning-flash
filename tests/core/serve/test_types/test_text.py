from dataclasses import dataclass

import pytest
import torch

from flash.core.utilities.imports import _TOPIC_SERVE_AVAILABLE


@dataclass
class CustomTokenizer:
    name: str

    def encode(self, text, return_tensors="pt"):
        return f"encoding from {self.name}"

    def decode(self, tensor):
        return f"decoding from {self.name}"


@pytest.mark.skipif(not _TOPIC_SERVE_AVAILABLE, reason="Not testing serve.")
def test_custom_tokenizer():
    from flash.core.serve.types import Text

    tokenizer = CustomTokenizer("test")
    text = Text(tokenizer=tokenizer)
    assert text.deserialize("random string") == "encoding from test"
    assert text.serialize(torch.tensor([[1, 2]])) == "decoding from test"


@pytest.mark.skipif(not _TOPIC_SERVE_AVAILABLE, reason="Not testing serve.")
def test_tokenizer_string():
    from flash.core.serve.types import Text

    text = Text(tokenizer="prajjwal1/bert-tiny")
    assert "some string" in text.serialize(text.deserialize("some string"))
