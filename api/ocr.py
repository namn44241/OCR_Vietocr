import base64

import numpy as np
from pdf2image import convert_from_bytes
from pydantic import BaseModel, field_validator
from fastapi import APIRouter, status, HTTPException

from ocr.ocr import ocr_model

router = APIRouter()

# --------------HELPERS----------------
def pdf2img(uri: str) -> np.ndarray:
    base64_string = uri.split(",")[1]
    pdf_bytes = base64.b64decode(base64_string)

    images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
    if not images:
        raise ValueError("Không thể chuyển đổi PDF sang ảnh")
    
    img = np.array(images[0])
    return img 

# --------------SCHEMAS-----------------
class OcrRequestData(BaseModel):
    uri: str
    id: str

    @field_validator("uri")
    @classmethod
    def check_uri(cls, value):
        if not value.startswith("data:application/"):
            raise ValueError("URI phải là chuỗi base64 bắt đầu với 'data:application/...'")

        encoded_data_parts = value.split(",")
        if len(encoded_data_parts) < 2:
            raise ValueError(f"Lỗi format chuỗi base64")
        
        return value

# ----------------API---------------------
@router.post("/api/ocr")
def get_abstract(data: OcrRequestData):
    if not data:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Không nhận được dữ liệu")
    
    id = data.id
    uri = data.uri

    img = pdf2img(uri)
    try:
        pred = ocr_model.forward(file_path = img)
        return {
            "success": True, 
            "status_code": 200, 
            "payload": {"id": id, "abstract": pred}
        }

    except Exception as err:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(err)) from err
 
    