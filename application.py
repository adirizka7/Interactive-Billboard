import requests, os
from flask import Flask, render_template, request
from config import cfg

PEOPLE_FOLDER = os.path.join('static', 'Photos')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/<string:image>')
def show_index(image):
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], image)
    return render_template("index.html", user_image = full_filename)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    text = request.form['q']

    s = requests.post(
            "https://geist.kata.ai/nlus/adirizka7:Billboard/predict",
            data={"text": text},
            headers={"Authorization":"Bearer " + cfg['bearer']}
            )

    return s.text

if __name__ == '__main__':
    app.run(debug = True)
