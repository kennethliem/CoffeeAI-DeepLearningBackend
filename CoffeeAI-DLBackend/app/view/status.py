from flask import Blueprint, request, jsonify
import os

statusCheck = Blueprint("check", __name__)

@statusCheck.route("/", methods=["GET"])
def engineCheck():
    path_name = "app/models/model.h5"

    data = {
        "error": True,
        "status": "Server Offline",
        "message": "Error!"
    }

    if os.path.isfile(path_name):
        data["error"] = False

        f = open("app/retrainStatus.txt", "r")
        engStatus = f.read()
        if engStatus == "Running":
            data["status"] = "Online"
            data["message"] = "Engine Ready - Retraining in progress"
        else:
            data["status"] = "Online"
            data["message"] = "Engine Ready"
            
        return jsonify(data)
    else:
        data["error"] = False
        data["status"] = "Offline"
        data["message"] = "Engine Offline"

        return jsonify(data)

@statusCheck.route("/disable", methods=["POST"])
def disableEngine():
    path_name = "app/models/model.h5"
    data = {
        "error": True,
        "status": None,
        "message": "Engine error!"
    }
    if request.form.get("key"):
        if os.path.isfile(path_name):
            if request.form.get("key") == "CoffeeAI-IAeeffoC":
                try:
                    data["error"] = False
                    data["status"] = None
                    data["message"] = "Engine turned off"
                    os.rename(path_name, 'app/models/model-disabled.h5')
                    return jsonify(data)
                except:
                    return jsonify(data)
            else:
                data["error"] = True
                data["status"] = None
                data["message"] = "Wrong key"
                return jsonify(data)
        else:
            data["error"] = True
            data["status"] = None
            data["message"] = "Engine already offline"
            return jsonify(data)
    else:
        data["error"] = True
        data["status"] = None
        data["message"] = "Please insert secret key"
        return jsonify(data)
    
@statusCheck.route("/enable", methods=["POST"])
def enableEngine():
    path_name = "app/models/model.h5"

    data = {
        "error": True,
        "status": None,
        "message": "Error!"
    }

    if request.form.get("key"):
        if os.path.isfile('app/models/model-disabled.h5'):
            if request.form.get("key") == "CoffeeAI-IAeeffoC":
                try:
                    data["error"] = False
                    data["status"] = None
                    data["message"] = "Engine turned on"
                    os.rename('app/models/model-disabled.h5', path_name)
                    return jsonify(data)
                except:
                    return jsonify(data)
            else:
                data["error"] = True
                data["status"] = None
                data["message"] = "Wrong key"
                return jsonify(data)
        else:
            data["error"] = True
            data["status"] = None
            data["message"] = "Engine already online"
            return jsonify(data)
    else:
        data["error"] = True
        data["status"] = None
        data["message"] = "Please insert secret key"
        return jsonify(data)