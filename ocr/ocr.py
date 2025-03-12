from typing import *

import numpy as np
from pydantic import BaseModel

from .models import Pytesseract
from .modules import preprocessing_pipeline
from .modules.forward.sub_forward import sub_predict
from .helpers import timer, plot

class OCR(BaseModel):
    model_2: Any = Pytesseract.pytesseract_model

    def forward(self, file_path: Union[str, np.ndarray]):
        resp_objs = preprocessing_pipeline.preprocessing_pipeline(file_path)

        predictions = []
        for resp_obj in resp_objs:
            predictions.append(
                sub_predict(img = resp_obj, detector = self.model_2)
            )
        
        return predictions

ocr_model = OCR()