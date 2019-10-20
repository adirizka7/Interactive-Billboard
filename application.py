from flask import Flask, render_template
import os

PEOPLE_FOLDER = os.path.join('static', 'Photos')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/<string:image>')
def show_index(image):
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], image)
    return render_template("index.html", user_image = full_filename)

if __name__ == '__main__':
    app.run(debug = True)
