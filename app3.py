from flask import Flask, request, send_file
from flask_cors import CORS
import edge_tts
import asyncio

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/tts', methods=['POST'])
def tts():
    async def async_tts(text, filename):
        communicate = edge_tts.Communicate(text, 'km-KH-SreymomNeural')
        await communicate.save(filename)

    data = request.json
    text = data.get('text')

    if not text:
        return {"error": "Text is required"}, 400

    filename = "output.mp3"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_tts(text, filename))

    return send_file(filename, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(debug=True)
