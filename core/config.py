# import build-in dependencies
import os
from typing import *

# import 3rd part dependencies
from pydantic import BaseModel

class Config(BaseModel):
    base_url: str = "https://dichvucong.gov.vn/p/home"
    raw_data_dir: str = "D:\\hoc-AI-ML\\OCR\\raw_data"
    image_data_dir: str = "D:\\hoc-AI-ML\\OCR\\data"

    def __init__(self, **data):
        super().__init__(**data)
        os.makedirs(self.raw_data_dir, exist_ok = True)
        os.makedirs(self.image_data_dir, exist_ok = True)

config = Config()