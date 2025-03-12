from abc import ABC, abstractmethod
from typing import *

import numpy as np

class OcrModel(ABC):
    model: Any
    model_name: str

    @abstractmethod
    def forward(self, img: np.ndarray):
        raise NotImplementedError()