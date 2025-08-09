# pip install pytesseract opencv-python
# sudo apt install tesseract-ocr


import sys
import cv2
import pytesseract

def extract_text(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] Cannot open image: {image_path}")
        return

    # Convert to grayscale (helps OCR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Optional: Apply a threshold to clean the image
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(gray)

    print("\n--- Extracted Text ---\n")
    print(text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ocr_image.py <image_path>")
    else:
        extract_text(sys.argv[1])


