import tensorflow as tf
from keras.models import load_model 
from flask import Blueprint, request, jsonify
import shutil
import os
import threading
import io

retrain = Blueprint("retrain", __name__)

IMAGE_SIZE = (240, 240)
BATCH_SIZE = 64
EPOCHS = 10
SEED = 991    

def retrainer():

    with open('app/retrainStatus.txt', 'w') as file:
        file.write('Running')
    file.close

    train_dir = 'app/datasets/exported/Train'
    test_dir = 'app/datasets/exported/Test'
        
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
        
    cnn_model = load_model('app/models/model.h5')

    cnn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
                    loss='categorical_crossentropy', 
                    metrics=['accuracy'])

    cnn_model.fit(
            x=train_data,
            epochs=EPOCHS,
            validation_data=test_data,
    )

    cnn_model.save('app/models/new-models-versions.h5')
    from datetime import date
    today = date.today()

    date = today.strftime("%d-%m-%Y")
    os.rename('app/models/model.h5', 'app/models/model-old-'+date+'.h5')
    os.rename('app/models/new-models-versions.h5', 'app/models/model.h5')

    with open('app/retrainStatus.txt', 'w') as file:
        file.write('Finished')
    file.close

@retrain.route("/", methods=["POST"])
def prepareRetrain():
    data = {
		"error":True,
		"message": "Error!"
	}
    retrain_thread = threading.Thread(target=retrainer, name="Retrainer")
    if request.method == "POST":
        if request.files.get('datasets'):
            dataset = request.files['datasets']
            file_name = dataset.filename.split("/")[-1]
            dataset.save(file_name)
            shutil.move(file_name, 'app/datasets/datasets.zip')
            import zipfile
            with zipfile.ZipFile('app/datasets/datasets.zip', 'r') as zip_ref:
                zip_ref.extractall('app/datasets/exported')
            os.remove('app/datasets/datasets.zip')
            retrain_thread.start()

            data["error"] = False
            data["message"] = "Retrain requested successfuly"
        else:
            data["error"] = True
            data["message"] = "Can't get Datasets file" 
    else:
        data["error"] = False
        data["message"] = "Wrong Method"            
  

    return jsonify(data)

