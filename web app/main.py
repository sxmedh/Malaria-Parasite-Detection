# pip3 install flask opencv-python
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2
from predict_utils import predict

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename):
    if (predict(filename)):
        return "Infected"
    return "Uninfected"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = processImage(filename)
            img = cv2.imread(f"uploads/{filename}")
            cv2.imwrite(f"static/{filename}", img)
            return render_template("result.html", filename=filename, result=result)

    return render_template("index.html")


app.run(debug=True, port=5001)
