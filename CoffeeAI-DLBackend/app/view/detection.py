import tensorflow as tf
from keras.models import load_model
import numpy as np
import cv2
from flask import Blueprint, request, jsonify
import os
import io

detection = Blueprint("detection", __name__)

labels = ["Arabika Gayo", "Robusta Gayo"]

def prepare_dataset(image):

    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image.reshape(1, 240, 240, 1)

    return image


@detection.route("/", methods=["POST"])
def coffeeTypeDetection():
    model = None
    preds = None
    path_name = "app/models/model.h5"

    data = {
        "error": True,
        "coffeeType": None,
        "message": "Error!"
    }

    if os.path.isfile(path_name):
        if request.method == "POST":
            model = load_model("app/models/model.h5")
            if request.files.get("image"):
                try:
                    imaging = cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
                    imaging_gray = cv2.cvtColor(imaging, cv2.COLOR_BGR2GRAY)
                    imaging_rgb = cv2.cvtColor(imaging, cv2.COLOR_BGR2RGB)
                    xml_data = cv2.CascadeClassifier('app/models/cascade.xml')
                    detecting = xml_data.detectMultiScale(imaging_gray,
                                                    minSize = (30, 30))
                    amountDetecting = len(detecting)
                    if amountDetecting != 0:
                        for (a, b, width, height) in detecting:
                            cv2.rectangle(imaging_rgb, (a, b),
                                        (a + height, b + width),
                                        (255, 255, 255), 5)
                            X = a
                            Y = b
                            W = width
                            H = height

                    cropped_image = imaging_rgb[Y:Y+H, X:X+W]
                    cv2.imwrite('app/view/temp.jpg',cropped_image)
                    image = None
                    image = tf.keras.preprocessing.image.load_img(
                        'app/view/temp.jpg', target_size=(240, 240), color_mode="grayscale")
                    image = prepare_dataset(image)
                    preds = model.predict(image, batch_size=64)
                    os.remove('app/view/temp.jpg')
                    if (preds[0][np.argmax(preds[0])] >= 0.8):
                        data["coffeeType"] = labels[np.argmax(preds[0])]
                        try:
                            data["error"] = False
                            data["message"] = "Success"
                        except:
                            data["error"] = True
                            data["message"] = "Not Detected, Currently not available in our databases - Engine"
                    else:
                        data["error"] = True
                        data["message"] = "Not Detected, Currently not available in our databases - Engine"
                except:
                    data["error"] = True
                    data["message"] = "Not Detected, Currently not available in our databases - Engine"
            else:
                data["error"] = True
                data["message"] = "Can't get Image - Engine"
        else:
            data["error"] = True
            data["message"] = "Wrong Method - Engine"
    else:
        data["error"] = True
        data["message"] = "Engine Offline, Please Contact service@coffeeai.online - Engine"

    return jsonify(data)
