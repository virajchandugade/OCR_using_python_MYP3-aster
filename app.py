from flask import Flask, render_template, request
from PIL import Image
import pytesseract
from googletrans import Translator
import os

app = Flask(__name__)

# Path to Tesseract-OCR (for Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return "No image uploaded", 400
    
    image = request.files["image"]
    if image.filename == "":
        return "No selected file", 400

    image_path = os.path.join("static", image.filename)
    image.save(image_path)

    extracted_text = pytesseract.image_to_string(Image.open(image_path))

    return render_template("index.html", extracted_text=extracted_text)

@app.route("/translate", methods=["POST"])
def translate_text():
    text = request.form.get("text")
    lang_code = request.form.get("language")

    translator = Translator()
    translated_text = translator.translate(text, dest=lang_code).text

    lang_map = {"hi": "Hindi", "fr": "French", "es": "Spanish"}
    lang_name = lang_map.get(lang_code, "Unknown")

    return render_template("index.html", extracted_text=text, translated_text=translated_text, lang_name=lang_name)


