from typing import *

import numpy as np
from PIL import Image
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor

from ..schemas import OcrModel

config = Cfg.load_config_from_name("vgg_transformer")
config["cnn"]["pretrained"] = False
config["device"] = "cpu"

class VietOcr(OcrModel.OcrModel):
    model: Any = Predictor(config)
    model_name: str = "VietOcr"

    def forward(self, img: np.ndarray) -> str:
        img = Image.fromarray(img)
        return self.model.predict(img).lower() + " "


vietocr_model = VietOcr()