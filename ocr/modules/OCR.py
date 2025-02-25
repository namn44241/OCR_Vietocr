# import built-in dependencies
import time
from typing import *

# import 3rd party dependencies
import numpy as np
from transformers import pipeline
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor

# import project dependencies
from .forward.sub_predict import sub_predict
from .pre_processing.preprocessing_pipeline import preprocessing_pipeline
from ..helpers.timer import timer
from ..helpers.plot import display_img

class OCR:
    def __init__(self):
        config = Cfg.load_config_from_name('vgg_transformer')
        config['cnn']['pretrained'] = False
        config['device'] = 'cpu'
        
        self.corrector = pipeline("text2text-generation", model="bmd1905/vietnamese-correction-v2")
        self.detector = Predictor(config) 

    @timer
    def predict(self, file_path: Union[str, np.ndarray]):
        resp_objs = preprocessing_pipeline(file_path)
        
        predictions = []
        for key, value in resp_objs.items():
            corrected = True if key == "corrected" else False

            for resp_obj in value:
                text = sub_predict(
                    resp_obj, 
                    self.detector, 
                    self.corrector,
                    corrected)
                
                predictions.append(text)

        return predictions
    
ocr = OCR()