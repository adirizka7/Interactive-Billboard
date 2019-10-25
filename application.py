import requests
import os
import json
import logging
from flask import Flask, render_template, request
from config import cfg

PEOPLE_FOLDER = os.path.join('static', 'Photos')
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/<string:image>')
def show_index(image):
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], image)
    return render_template("index.html", user_image = full_filename)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    text = request.form['q']

    logging.info('Text Input : {}'.format(text))
    s = requests.post(
            "https://geist.kata.ai/nlus/adirizka7:Billboard/predict",
            data={"text": text},
            headers={"Authorization":"Bearer " + cfg['bearer']}
            )

    logging.info('Response received : {}'.format(json.dumps(json.loads(s.text), indent=4)))
    s = json.loads(s.text)['result']
    intent = [x for x in s if s[x] != []]
    logging.info('Intent extracted : {}'.format(intent))

    return show_index(intent[0] + '/1.png') if len(intent) else show_index('Mulai.png')

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
