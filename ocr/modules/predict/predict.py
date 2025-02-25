# import built-in dependencies
import time
from typing import *

# import 3rd party dependencies
import numpy as np

# import project dependencies
from ..preprocessing.preprocessing_pipeline import preprocessing_pipeline
from ..preprocessing.segment import profile_projection_segment
from .predict import sub_predict
from ...helpers.file_helpers import add_white_padding

def predict(
        file_path: Union[str, np.ndarray],
        detector
):
    t0 = time.time()
    process_time = {"predict_total": 0,
                    "preprocessing": {},
                    "predict_parts": {
                        "sub_predict": [],
                        "parse_words": [],
                        "parse_lines": []
                    }}

    resp_objs, preprocessing_time = preprocessing_pipeline(file_path)
    process_time["preprocessing"] = preprocessing_time
    
    predictions = []
    for resp_obj in resp_objs:
        text, subpredict_time = sub_predict.sub_predict(resp_obj, detector)
        process_time["predict_parts"]["sub_predict"].append(subpredict_time["predict_total"])
        process_time["predict_parts"]["parse_words"].append(subpredict_time["parse_words"])
        process_time["predict_parts"]["parse_lines"].append(subpredict_time["parse_lines"])
        predictions.append(text)
    
    t1 = time.time()
    process_time["predict_total"] = t1 - t0
    return predictions, process_time
    
