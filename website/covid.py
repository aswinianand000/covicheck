# Importing the necessary libraries
import h5py
import numpy as np
import tensorflow                       as tf
from keras.preprocessing.image          import load_img, img_to_array
from PIL                                import Image
from flask                              import flash, send_file

img_width = 256
img_height = 256

trained_model = 'website/aiml/trained_models/01_20032022-193359_model.h5'
classes=["COVID", "Lung_Opacity", "Normal", "Viral Pneumonia"]

def predict_covid(img_file):
    model = tf.keras.models.load_model(trained_model)
    image = load_img(img_file)
    image = image.resize((img_width,img_height))
    imgArray = img_to_array(image)
    imgArray = np.expand_dims(imgArray,axis=0)
    imgArray = imgArray*1./255
    y_class = model.predict(imgArray)
    class_pred = classes[np.argmax(y_class)]
    return class_pred

# print(predict_covid(normal_img))
# print(predict_covid(covid_img))

def downloadFile (path = None):
    if path is None:
        flash("No file exist!", category="error")
    else:
        return send_file(path, as_attachment=True)