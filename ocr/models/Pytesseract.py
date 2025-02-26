from typing import *

import numpy as np
from PIL import Image
import pytesseract

from ..schemas import OcrModel

class Pytesseract(OcrModel.OcrModel):
    model: Any = pytesseract
    model_name: str = "Pytesseract"

    def forward(self, img: np.ndarray):
        img = Image.fromarray(img)
        return self.model.image_to_string(img, lang = "vie").lower()
    

pytesseract_model = Pytesseract()
