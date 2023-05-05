from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
import os

app = Flask(__name__)


def extract_colors(image):
    # Resize the image to speed up processing
    image = image.resize((150, 150))

    # Convert the image to an array
    img_array = np.array(image)

    # Flatten the array and count the unique colors
    colors, counts = np.unique(img_array.reshape(-1, 3), axis=0, return_counts=True)

    # Sort the colors by count and select the top 10
    top_colors = colors[np.argsort(-counts)][:10]

    # Convert the colors to HEX format
    hex_colors = [f'#{r:02x}{g:02x}{b:02x}' for r, g, b in top_colors]

    return hex_colors


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(url_for('index'))

    image = request.files['image']
    img = Image.open(image)
    colors = extract_colors(img)
    print("Extracted colors:", colors)

    return render_template('result.html', colors=colors)


if __name__ == '__main__':
    app.run(debug=True)
