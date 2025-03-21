from typing import *

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import ocr

def get_application() -> FastAPI:
    application = FastAPI(
        title = "OCR",
        docs_url = "/docs"
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(ocr.router)

    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload = True)