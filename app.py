from fileinput import filename
from importlib.resources import path
from flask import Flask, flash, redirect, render_template, url_for, request
import os
import urllib.request
from werkzeug.utils import secure_filename

import tensorflow
from tensorflow import keras
from keras import models
from keras.preprocessing import image
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt



UPLOAD_FOLDER = 'static/code_images'
IMPORT_FOLDER = 'static/images'

app = Flask(__name__)
app.secret_key = "secret_key"
app.config["IMPORT_FOLDER"] = IMPORT_FOLDER
app.config["CODE_FOLDER"] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def solution(filename):
    model = models.load_model("CNN_Project_Model-Trans_learn(VGG16).h5")
    img_path = 'static/code_images/' + filename
    img = image.load_img(img_path, target_size = (150, 150))
    plt.imshow(img)
    img = image.img_to_array(img)
    x = np.expand_dims(img, axis = 0)
    img = np.vstack([x])
    result = model.predict(img)
    return result

@app.route('/')
def homes():
    global dog_img, cat_img, upload_img, arrow_img
    dog_img = os.path.join(app.config["IMPORT_FOLDER"], 'dog.jpg')
    cat_img = os.path.join(app.config["IMPORT_FOLDER"], 'cat.jpg')
    arrow_img = os.path.join(app.config["IMPORT_FOLDER"], 'arrow.png')
    upload_img = os.path.join(app.config["IMPORT_FOLDER"], 'upload.png')
    return render_template("main.html", dog = dog_img, cat = cat_img, upload = upload_img)

@app.route('/', methods = ['POST'])
def upload_image():
    print(request.files)
    print("Uploaded in the html page")
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['CODE_FOLDER'], filename))
        print("Saved File in images folder :", filename)
        sol = solution(filename)
        if sol == 1:
            return render_template('result.html', result = dog_img, arrow = arrow_img, mess = "Dog")
        else:
            return render_template('result.html', result = cat_img, arrow = arrow_img, mess = "Cat")
    
    else:
        return render_template(request.url)
        
if __name__ == "__main__":
    app.run()
    