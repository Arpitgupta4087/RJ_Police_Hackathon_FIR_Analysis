import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\Users\kanak gupta\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"

def extract_text_from_pdf(pdf_file):
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.getbuffer())
    pages = convert_from_path("temp.pdf", dpi=150, poppler_path=POPPLER_PATH)
    text = "\n".join(pytesseract.image_to_string(p, lang="hin+eng") for p in pages)
    return text.strip()
