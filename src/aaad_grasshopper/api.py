import base64
import time

import plotly
from aaad.data.dataset import Dataset
from aaad.visualisation.plotter import Plotter
from flask import Flask, request, make_response
import pickle

from controller import SessionController
import json
from compas.data import DataEncoder, DataDecoder

app = Flask(__name__)


@app.route("/x", methods=["GET"])
def x():
    args = request.args
    session_id = args["session_id"]
    sc = SessionController.create(session_id)


@app.route("/project_setup", methods=["GET"])
def project_setup():
    args = request.args
    session_id = args["session_id"]
    sc = SessionController.create(session_id)

    root = args["root"]
    dataset_name = args["dataset_name"]
    sc.project_setup(root, dataset_name)
    return "Done!"


@app.route("/create_dataset_object", methods=["POST"])
def create_dataset_object():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    design_parameters = data["design_parameters"]
    performance_attributes = data["performance_attributes"]

    response = sc.create_dataset_object(design_parameters, performance_attributes)

    return str(response)


@app.route("/generate_dp_samples", methods=["POST"])
def generate_dp_samples():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    n_samples = data["n_samples"]
    samples_per_file = data["samples_per_file"]

    result = sc.generate_dp_samples(n_samples, samples_per_file)
    response = json.dumps(result, cls=DataEncoder)

    return str(response)


@app.route("/load_dataset", methods=["GET"])
def load_dataset():
    args = request.args
    session_id = args["session_id"]
    sc = SessionController.create(session_id)
    response = sc.load_dataset()
    return str(response)


@app.route("/dataset_summary", methods=["GET"])
def dataset_summary():
    args = request.args
    session_id = args["session_id"]
    sc = SessionController.create(session_id)
    response = sc.dataset_summary()
    return str(response)


@app.route("/getdata_design_parameters", methods=["POST"])
def getdata_design_parameters():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    result = sc.getdata_design_parameters()
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/import_data_from_dict", methods=["POST"])
def import_data_from_dict():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    datadict = data["datadict"]
    sc = SessionController.create(session_id)

    result = sc.import_data_from_dict(datadict)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/datablocks_dataobjects", methods=["POST"])
def datablocks_dataobjects():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)
    result = sc.datablocks_dataobjects
    print(result)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/plot_distrib_attributes", methods=["POST"])
def plot_distrib_attributes():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    output_type = data["output_type"]
    attributes = data["attributes"]
    fig = sc.plot_distrib_attributes(dataobjects=attributes)
    fig = _fig_output(fig, output_type)

    response = json.dumps(fig, cls=DataEncoder)
    return response


@app.route("/plot_correlations", methods=["POST"])
def plot_correlations():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    output_type = data["output_type"]
    attributes = data["attributes"]
    fig = sc.plot_correlations(dataobjects=attributes)
    fig = _fig_output(fig, output_type)

    response = json.dumps(fig, cls=DataEncoder)
    return response


@app.route("/plot_distrib_attributes2d", methods=["POST"])
def plot_distrib_attributes2d():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    output_type = data["output_type"]
    attributes = data["attributes"]
    fig = sc.plot_distrib_attributes2d(dataobjects=attributes)
    fig = _fig_output(fig, output_type)

    response = json.dumps(fig, cls=DataEncoder)
    return response


@app.route("/design_parameters", methods=["GET"])
def get_design_parameters():
    data = request.args
    session_id = data["session_id"]

    sc = SessionController.create(session_id)
    result = sc.get_design_parameters()
    return result


@app.route("/run_training", methods=["POST"])
def run_training():
    data = request.data
    data = pickle.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    settings = data["settings"]
    inputML = settings["inputML"]
    outputML = settings["outputML"]
    model_type = settings["model_type"]
    latent_dim = settings["latent_dim"]
    layer_widths = settings["layer_widths"]
    batch_size = settings["batch_size"]
    epochs = data["epochs"]

    result = "False"
    if model_type == "CAE":
        result = sc.train_cae(inputML, outputML, latent_dim, layer_widths, batch_size, epochs)
    elif model_type == "VAE":
        raise NotImplementedError("API to VAE models is not implemented at the moment.")
    else:
        raise ValueError("Wrong model type. Select 'CAE' or 'VAE'.")

    return str(result)


@app.route("/request_designs", methods=["POST"])
def request_designs():
    data = request.data
    data = pickle.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    requested_values = data["requested_values"]
    n_designs = data["n_designs"]
    result = sc.request_designs(n_designs, requested_values)
    result = json.dumps(result, cls=DataEncoder)
    return result


@app.route("/get_one_sample", methods=["POST"])
def get_one_sample():
    data = request.data
    data = pickle.loads(data)
    session_id = data["session_id"]

    sc = SessionController.create(session_id)

    item = data["item"]
    result = sc.get_one_sample(item)
    print(result)
    result = json.dumps(result, cls=DataEncoder)
    return result


@app.route("/load_model", methods=["GET"])
def load_model():
    args = request.args
    session_id = args["session_id"]
    sc = SessionController.create(session_id)

    checkpoint_path = args["checkpoint_path"]
    checkpoint_name = args["checkpoint_name"]
    inputML = args["inputML"].split(",")
    outputML = args["outputML"].split(",")

    result = "False"
    result = sc.load_cae_model(
        checkpoint_path=checkpoint_path,
        checkpoint_name=checkpoint_name,
        inputML=inputML,
        outputML=outputML,
    )

    return str(result)


@app.route("/nn_summary", methods=["GET"])
def nn_summary():
    args = request.args
    session_id = args["session_id"]
    sc = SessionController.create(session_id)

    level = args["level"]
    result = "False"
    result = sc._model_summary(max_depth=int(level))

    return str(result)


def _fig_output(fig, output_type):
    if fig:
        if output_type == "static":
            fig = _fig_to_str(fig)
            response = fig
        elif output_type == "interactive":
            fig.show()
            response = True
    else:
        response = False
    return str(response)


def _fig_to_str(fig):
    """
    Convert a plotly figure graph to a string-encoded bytes.
    """
    img_bytes = base64.b64encode(fig.to_image())
    img_string = img_bytes.decode("utf-8")
    return img_string


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
