import pytesseract
from PIL import Image

class OCRService:
    def __init__(self):
        # tesseract path windows için
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def read_text(self, image_path):
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="tur")
        return text
