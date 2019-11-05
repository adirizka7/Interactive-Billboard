import requests
import os
import json
import logging
from flask import Flask, render_template, request, send_from_directory
from config import cfg

PEOPLE_FOLDER = os.path.join('static', 'Photos')
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/<string:image_folder>')
def show_index(image_folder):

    if image_folder == '':
        image_folder = os.path.join(app.config['UPLOAD_FOLDER'] + '/')
        return render_template("index.html", user_image = [image_folder, ['Mulai.png']])

    image_folder = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + image_folder)
    images = os.listdir(image_folder)
    return render_template("index.html", user_image = [image_folder, images])

@app.route('/', methods=['POST', 'GET'])
def handle_data():
    if request.method == 'POST':
        text = request.form['q']

        logging.info('Text Input : {}'.format(text))
        s = requests.post(
                "https://geist.kata.ai/nlus/adirizka7:Billboard/predict",
                data={"text": text},
                headers={"Authorization":"Bearer " + cfg['bearer']}
                )

        logging.info('Response received : {}'.format(json.dumps(json.loads(s.text),
            indent=4)))
        s = json.loads(s.text)['result']

        maxi = 0
        intent = ''
        for entities in s:
            if s[entities] == []:
                continue
            if s[entities][0]['score'] > maxi:
                maxi = s[entities][0]['score']
                intent = [entities]

        print(intent)
        logging.info('Intent extracted : {}'.format(intent))

        return show_index(intent[0] + '/') if len(intent) else show_index('')
    else:
        return show_index('')

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
