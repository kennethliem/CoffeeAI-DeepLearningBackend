from flask import Flask

with open('app/retrainStatus.txt', 'w') as file:
    file.write('Finished')
file.close
app = Flask(__name__)

from app import routes