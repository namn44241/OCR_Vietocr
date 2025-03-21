import base64
import requests

def test_ocr(pdf_path: str):
    """
    Test API OCR với file PDF
    Args:
        pdf_path: Đường dẫn đến file PDF cần OCR
    """
    # 1. Đọc file PDF và chuyển thành base64
    print(f"Đang đọc file: {pdf_path}")
    with open(pdf_path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read()).decode('utf-8')
        base64_pdf = f"data:application/pdf;base64,{encoded_string}"
    print("Đã chuyển đổi PDF sang base64")

    # 2. Tạo payload cho API
    payload = {
        "uri": base64_pdf,
        "id": "test_001"
    }

    # 3. Gọi API
    print("Đang gọi API OCR...")
    response = requests.post(
        "http://localhost:5050/api/ocr",
        json=payload
    )

    # 4. Xử lý kết quả
    if response.status_code == 200:
        result = response.json()
        print("\nKết quả OCR thành công:")
        print("-" * 50)
        print(result['payload']['abstract'])
        print("-" * 50)
    else:
        print(f"Lỗi: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Thay đổi đường dẫn PDF tại đây
    pdf_file = "KL-91-BCT.pdf"  # Đặt file PDF của bạn cùng thư mục với file test_ocr.py
    test_ocr(pdf_file)