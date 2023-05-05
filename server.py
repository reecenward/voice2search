from flask import Flask, request
import base64
import io
import pytesseract
from PIL import Image
app = Flask(__name__)

@app.route('/photo', methods=['POST'])
def handle_photo():
    # Get the photo data from the request
    photo_data = request.json.get('photo')

    # Decode the base64 encoded photo data into bytes
    photo_bytes = base64.b64decode(photo_data)

    # Convert the bytes into a PIL Image object
    photo = Image.open(io.BytesIO(photo_bytes))

    # Extract the text from the image using pytesseract
    text = pytesseract.image_to_string(photo)

    # Do something with the extracted text (e.g. print it)
    print("the text is: ",text, ".")

    return {'message': 'Text extracted successfully'}

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)