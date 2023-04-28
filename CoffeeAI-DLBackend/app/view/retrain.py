import tensorflow as tf
from keras.models import load_model 
from flask import Blueprint, request, jsonify
import shutil
import os
import io

retrain = Blueprint("retrain", __name__)

IMAGE_SIZE = (240, 240)
BATCH_SIZE = 64
EPOCHS = 100
SEED = 991

@retrain.route("/start", methods=["POST"])
def modelRetrain():

    data = {
		"error":True,
		"message": "Error!"
	}

    try:
        train_dir = 'datasets/exported/train'
        test_dir = 'datasets/exported/test'
        
        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                                                rescale=1./255,
                                                zoom_range=0.2,
                                                horizontal_flip=True
                                            )
        
        validation_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                                                rescale=1./255,
                                                zoom_range=0.2,
                                                horizontal_flip=True
                                            )

        train_data = train_datagen.flow_from_directory(train_dir,
                                                        target_size=IMAGE_SIZE,
                                                        batch_size=BATCH_SIZE,
                                                        shuffle=True,
                                                        color_mode='grayscale',
                                                        class_mode='categorical'
                                                    )

        test_data = validation_datagen.flow_from_directory(test_dir,
                                                        target_size=IMAGE_SIZE,
                                                        batch_size=BATCH_SIZE,
                                                        shuffle=True,
                                                        color_mode='grayscale',
                                                        class_mode='categorical'
                                                    )
        
        cnn_model = load_model('app/models/model-new.h5')

        cnn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
                    loss='categorical_crossentropy', 
                    metrics=['accuracy'])

        cnn_model.fit(
            x=train_data,
            epochs=EPOCHS,
            validation_data=test_data,
        )

        cnn_model.save('models/new-models-versions.h5')

        data["error"] = False
        data["message"] = "Model Succesfully Trained"
    except:
        data["error"] = True
        data["message"] = "Training process error"

    return jsonify(data)

def extractDatasets(path):
    import zipfile
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall('datasets/exported')
    os.remove('datasets/datasets.zip')

    return jsonify()

@retrain.route("/", methods=["POST"])
def datasets():
    data = {
		"error":True,
		"message": "Error!"
	}

    if request.method == "POST":
        if request.files.get('datasets'):
            dataset = request.files['datasets']
            dataset.save(dataset.filename)
            shutil.move(dataset.filename, 'datasets/datasets.zip')
            extractDatasets('datasets/datasets.zip')

            data["error"] = False
            data["message"] = "Datasets uploaded succesfully" 
        else:
            data["error"] = True
            data["message"] = "Can't get Datasets file" 
    else:
        data["error"] = True
        data["message"] = "Wrong Method"

    return jsonify(data)