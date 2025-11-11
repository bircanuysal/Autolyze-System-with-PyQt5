import cv2
import numpy as np
from services.ocr.OCRService import OCRService
from services.ocr.postprocessing import extract_listing_info

class ImageProcessingService:
    def __init__(self):
        self.ocr = OCRService()

    def analyze_listing_image(self, image_path):
        """
        Sahibinden ilan görselinden ilan bilgilerini çıkarır.
        """
        # 1. OCR ile tüm metni oku
        text = self.ocr.read_text(image_path)

        # 2. Regex + postprocessing ile bilgileri çıkar
        data = extract_listing_info(text)

        return data
