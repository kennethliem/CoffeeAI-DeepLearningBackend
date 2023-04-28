from app import app

from app.view.detection import detection
from app.view.retrain import retrain
from app.view.status import statusCheck

@app.route('/')
def hello():
    return 'Welcome to CoffeeAI Private EndPoint'

app.register_blueprint(detection, url_prefix="/api/detection")
app.register_blueprint(retrain, url_prefix="/api/retrain")

app.register_blueprint(statusCheck, url_prefix="/api/check")

