from flask import Flask, request, jsonify, send_from_directory
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image
from colorthief import ColorThief
import tempfile
import os

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/cover-palette', methods=['POST'])
def cover_palette():
    if 'audio' not in request.files:
        return "No audio file", 400

    file = request.files['audio']

    # Guardar en un archivo temporal
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        audio = MP3(tmp_path, ID3=ID3)

        # Buscar frame APIC (portada)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):  # mutagen reconoce la portada como APIC
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as img_tmp:
                    img_tmp.write(tag.data)
                    img_tmp.flush()

                    ct = ColorThief(img_tmp.name)
                    palette = ct.get_palette(color_count=6)

                # limpiar archivo temporal
                os.remove(img_tmp.name)
                os.remove(tmp_path)

                return jsonify(palette)

    except Exception as e:
        print("Error extracting palette:", e)

    # limpiar si no hay portada
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    return jsonify([[255, 255, 255]]), 200  # fallback blanco


if __name__ == '__main__':
    app.run(debug=True)
