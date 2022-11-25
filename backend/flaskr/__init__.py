from cmath import nan
from flask import Flask,jsonify,request,session,send_from_directory
from flask_cors import CORS
from . import ALController

global ALControllerdb
ALControllerdb = {}


def create_app():
    app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'redis'
    app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
    CORS(app)

    @app.route('/')
    def index():
        return 'hi'

    @app.route('/ALsetting/<datasetname>/<initial_labelled>/<modelname>',methods=["GET"])
    def set_ALController(datasetname,initial_labelled,modelname):
        initial_labelled = float(initial_labelled)
        myALController = ALController.ALController(datasetname,initial_labelled,modelname)
        score = 0 
        predictions = []
        prediction_probs = []
        probs = []
        embedded_data = []
        if initial_labelled>0:
            score = myALController.get_modelmetrics()
            predictions=myALController.get_predictions().tolist()
            prediction_probs=myALController.get_prediction_probs().tolist()
            probs = myALController.get_predprobs().tolist()
            embedded_data=myALController.dataembedding.tolist()
        if not session.get("uid") is None:
            session['uid'] = uuid.uuid4()
        ALControllerdb[session.get('uid')]=myALController
        return jsonify(
            datatype=myALController.data.datatype,
            labelnames=myALController.data.labelnames.tolist(),
            ylabel=myALController.data.y_raw.tolist(),
            embedding=embedded_data,
            labeleddata=myALController.data.labelarr.tolist(),
            acc=score,
            predictions=predictions,
            allprobs=probs,
            prediction_probs=prediction_probs,
            )

    @app.route('/itertraining',methods=["POST"])
    def iter_training():
        request_json = request.get_json()
        new_labelled_indices = request_json.get('indexarr')
        print(f'{len(new_labelled_indices)} of instances are retrained!')
        new_labels = request_json.get('labelarr')
        myALController = ALControllerdb[session.get('uid')]
        if len(new_labelled_indices)>0:
            myALController.updatedata(new_labelled_indices,new_labels)
            # myALController.data.update_pool(new_labelled_indices)
            myALController.iter_train(new_labelled_indices,new_labels)
            score = myALController.get_modelmetrics()

        embedded_data = []
        return jsonify(
            acc=score,
            predictions=myALController.get_predictions().tolist(),
            allprobs=myALController.get_predprobs().tolist(),
            prediction_probs=myALController.get_prediction_probs().tolist(),
        )

    @app.route('/images/<path:path>',methods=["GET"])
    def send_image(path):
        return send_from_directory('../data/', path)

    @app.route('/images',methods=["POST"])
    def get_images():
        request_json = request.get_json()
        indices = request_json.get('indices')
        myALController = ALControllerdb[session.get('uid')]
        ids=myALController.data.query_ids(indices)
        labels=myALController.data.query_labels(indices)
        paths = myALController.data.query_datapath(indices,labels,ids)
        return jsonify(paths)

    @app.route('/candidates/<strategy>',methods=["GET"])
    def get_candidates(strategy):
        myALController = ALControllerdb[session.get('uid')]
        suggestedindices =  myALController.get_candidates(strategy)
        print(suggestedindices)
        return jsonify(
            suggestedindices.tolist()
        )

    return app