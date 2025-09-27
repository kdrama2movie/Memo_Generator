from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import uuid

app = Flask(__name__)

# A4 size in pixels (300 DPI)
A4_WIDTH, A4_HEIGHT = 2480, 3508
ROWS, COLS = 2, 2

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def make_a4_collage(image_paths, output_path):
    collage = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
    slot_width = A4_WIDTH // COLS
    slot_height = A4_HEIGHT // ROWS

    for idx in range(ROWS * COLS):
        row = idx // COLS
        col = idx % COLS
        x = col * slot_width
        y = row * slot_height

        if idx < len(image_paths):
            img = Image.open(image_paths[idx])
            img.thumbnail((slot_width, slot_height), Image.LANCZOS)
            offset_x = x + (slot_width - img.width) // 2
            offset_y = y + (slot_height - img.height) // 2
            collage.paste(img, (offset_x, offset_y))

    collage.save(output_path, "JPEG", quality=95)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_files = request.files.getlist("photos")
        paths = []

        for file in uploaded_files[:4]:  # Max 4 files
            filename = str(uuid.uuid4()) + ".jpg"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            paths.append(filepath)

        output_filename = str(uuid.uuid4()) + ".jpg"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        make_a4_collage(paths, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3737, debug=True)