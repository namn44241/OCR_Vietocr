import base64
import os

def get_pdf_base64(pdf_path: str, output_file: str = "pdf_base64.txt"):
    """
    Đọc file PDF và lưu chuỗi base64 ra file
    Args:
        pdf_path: Đường dẫn đến file PDF
        output_file: Tên file để lưu chuỗi base64
    """
    # Đọc file PDF và chuyển base64
    with open(pdf_path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read()).decode('utf-8')
        base64_pdf = f"data:application/pdf;base64,{encoded_string}"
    
    # Lưu ra file
    with open(output_file, "w") as f:
        f.write(base64_pdf)
    
    print(f"Đã lưu chuỗi base64 vào file: {output_file}")
    print(f"Kích thước file: {os.path.getsize(output_file)} bytes")

if __name__ == "__main__":
    get_pdf_base64("KL-91-BCT.pdf")  # Thay bằng đường dẫn PDF của bạn