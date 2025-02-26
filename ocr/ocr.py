from typing import *

import numpy as np
from pydantic import BaseModel

from .models import VietOcr, Pytesseract
from .modules import preprocessing_pipeline
from .modules.forward.sub_forward import sub_predict
from .helpers import timer

class OCR(BaseModel):
    model_1: Any = VietOcr.vietocr_model
    model_2: Any = Pytesseract.pytesseract_model

    @timer.timer
    def forward(self, file_path: Union[str, np.ndarray]):
        resp_objs = preprocessing_pipeline.preprocessing_pipeline(file_path)

        predictions = []
        for key, value in resp_objs.items():
            if key == "VietOcr":
                detector = self.model_1
            
            else: detector = self.model_2

            for img in value:
                predictions.append(
                    sub_predict(img = img, detector = detector)
                )
        
        return predictions