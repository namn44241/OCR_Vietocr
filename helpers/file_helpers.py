# import build-in dependencies
import os

# import 3rd part dependencies
import pdf2image

def pdf_2_jpg(file, dir, output_dir):
    file_path = os.path.join(dir, file)
    if not file.endswith(".pdf"):
        print(f"Chỉ hỗ trợ file .pdf") 
        return
    
    imgs = pdf2image.convert_from_path(file_path, first_page = 1)
    file_name = file.replace("pdf", "jpg")
    imgs[0].save(os.path.join(output_dir, file_name))
    return

