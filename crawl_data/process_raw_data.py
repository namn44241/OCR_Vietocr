# import build-in dependencies
import os

# import 3rd part dependencies
from tqdm import tqdm

# import project dependencies
from core.config import config
from helpers import file_helpers

def process_raw_data():
    files = os.listdir(config.raw_data_dir)
    num_files = len(files)

    for i in tqdm(range(num_files)):
        file = files[i]
        
        file_helpers.pdf_2_jpg(
            file = file,
            dir = config.raw_data_dir,
            output_dir = config.image_data_dir
        )