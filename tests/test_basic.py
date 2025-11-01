from src.dataset import encode
from src.model import SmallTransformerClassifier
from src.dataaset import CHARS
import torch

def test_encode_pad_length():
    ids = encode("abc", maxlen=8)
    assert len(ids) == 8

def test_model_forward():
    m = SmallTransformerClassifier(vocab_size=len(CHARS))
    x = torch.randint(0, len(CHARS)+2, (4, 32), dtype=torch.long)
    y = m(x)
    assert y.shape == (4, 3)
