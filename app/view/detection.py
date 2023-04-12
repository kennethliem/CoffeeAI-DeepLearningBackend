import tensorflow as tf
from keras.models import load_model 
import numpy as np
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
		"error":True,
		"coffeeType": None,
		"message": "Error!"
	}
 
	if os.path.isfile(path_name):
		if request.method == "POST":
			model = load_model("app/models/model.h5")
			if request.files.get("image"):
				image = None
				image = request.files['image'].read()
				image = tf.keras.preprocessing.image.load_img(io.BytesIO(image), target_size=(240, 240), color_mode = "grayscale")
				image = prepare_dataset(image)
				preds = model.predict(image, batch_size=64)

				if(preds[0][np.argmax(preds[0])]>=0.8):
					data["coffeeType"] = labels[np.argmax(preds[0])]
					try:
						data["error"] = False
						data["message"] = "Success"
					except:
						data["error"] = True
						data["message"] = "Under Construction! Currently not available in our databases"
				else:
					data["error"] = True
					data["message"] = "Not Detected"
			else:
				data["error"] = True
				data["message"] = "Can't get Image"
		else:
			data["error"] = True
			data["message"] = "Wrong Method"
	else:
		data["error"] = True
		data["message"] = "Model File Is Missing!"

	return jsonify(data)
