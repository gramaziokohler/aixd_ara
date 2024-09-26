import json
import os
import signal

from compas.data import DataEncoder
from flask import Flask
from flask import request

from aixd_ara.constants import DEFAULT_PORT
from aixd_ara.controller import SessionController

app = Flask(__name__)


@app.post("/reset_session")
def reset_session():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)
    sc.reset()
    result = {"msg": "Session reset"}
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/project_setup", methods=["POST"])
def project_setup():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    sc.reset()  # Reset the session
    project_root = data["project_root"]
    project_name = data["project_name"]
    result = sc.project_setup(project_root, project_name)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/project_setup_info", methods=["POST"])
def project_setup_info():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    result = sc.project_setup_info()
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/create_dataset_object", methods=["POST"])
def create_dataset_object():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    design_parameters = data["design_parameters"]
    performance_attributes = data["performance_attributes"]
    result = sc.create_dataset_object(design_parameters, performance_attributes)
    response = json.dumps(result, cls=DataEncoder)
    return str(response)


@app.route("/generate_dp_samples", methods=["POST"])
def generate_dp_samples():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    n_samples = data["n_samples"]
    result = sc.generate_dp_samples(n_samples)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/save_samples", methods=["POST"])
def save_samples():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    n_samples = data["samples"]
    samples_per_file = data["samples_per_file"]
    result = sc.save_samples(n_samples, samples_per_file)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/load_dataset", methods=["POST"])
def load_dataset():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    result = sc.load_dataset()
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/dataset_summary", methods=["POST"])
def dataset_summary():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    result = sc.dataset_summary()
    response = json.dumps(result, cls=DataEncoder)
    return response


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
    sc = SessionController.create(session_id)

    datadict = data["datadict"]
    result = sc.import_data_from_dict(datadict)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/datablocks_dataobjects", methods=["POST"])
def datablocks_dataobjects():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    result = sc.datablocks_dataobjects()
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/get_dataobject_names_from_block", methods=["POST"])
def get_dataobject_names_from_block():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    datablock_nickname = data["datablock_nickname"]
    result = sc.get_dataobject_names_from_block(datablock_nickname)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/get_dataobject_types", methods=["POST"])
def get_dataobject_types():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    result = sc.get_dataobject_types()
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
    result = sc.plot_distrib_attributes(dataobjects=attributes, output_type=output_type)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/plot_correlations", methods=["POST"])
def plot_correlations():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    output_type = data["output_type"]
    attributes = data["attributes"]
    result = sc.plot_correlations(dataobjects=attributes, output_type=output_type)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/plot_contours", methods=["POST"])
def plot_contours():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    output_type = data["output_type"]
    attributes = data["attributes"]
    result = sc.plot_contours(dataobjects=attributes, output_type=output_type)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/plot_contours_request", methods=["POST"])
def plot_contours_request():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)
    output_type = data["output_type"]

    result = sc.plot_contours_request(output_type=output_type)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/design_parameters", methods=["GET"])
def get_design_parameters():
    data = request.args
    session_id = data["session_id"]

    sc = SessionController.create(session_id)
    result = sc.get_design_parameters()
    return result


@app.post("/model_setup")
def model_setup():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    settings = data["settings"]
    model_type = settings["model_type"]
    inputML = settings["inputML"]
    outputML = settings["outputML"]
    latent_dim = settings["latent_dim"]
    hidden_layers = settings["hidden_layers"]
    batch_size = settings["batch_size"]

    result = sc.model_setup(model_type, inputML, outputML, latent_dim, hidden_layers, batch_size)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.post("/model_train")
def model_train():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    epochs = data["epochs"]
    wb = data["wb"]
    result = sc.model_train(epochs, wb)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/model_load", methods=["POST"])
def model_load():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    model_type = data["model_type"]
    checkpoint_path = data["checkpoint_path"]
    checkpoint_name = data["checkpoint_name"]
    result = sc.model_load(model_type, checkpoint_path=checkpoint_path, checkpoint_name=checkpoint_name)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/request_designs", methods=["POST"])
def request_designs():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    requested_values = data["requested_values"]
    n_designs = data["n_designs"]
    result = sc.request_designs(requested_values, n_designs)
    result = json.dumps(result, cls=DataEncoder)
    return result


@app.route("/get_one_sample", methods=["POST"])
def get_one_sample():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    item = data["item"]
    result = sc.get_one_sample(item)
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/nn_summary", methods=["POST"])
def nn_summary():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    max_depth = data["max_depth"]
    result = sc.model_summary(max_depth=int(max_depth))
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/model_input_output_dimensions", methods=["POST"])
def model_input_output_dimensions():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    result = sc.model_input_output_dimensions()
    response = json.dumps(result, cls=DataEncoder)
    return response


@app.route("/shutdown", methods=["GET"])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    print()
    print()
    print()
    print("*********************************************************")
    print("THIS APP HAS TERMINATED AND THIS WINDOW CAN BE CLOSED NOW")
    print("*********************************************************")
    print()
    print()
    print()
    return "Server shuting down"


@app.route("/ping", methods=["GET"])
def ping():
    return "Pong!"


def ara_welcome(*args):
    print()
    print()
    print()
    print("****************************")
    print("HELLO! ARA SERVER IS RUNNING")
    print("****************************")
    print()
    print()
    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        port = DEFAULT_PORT
    else:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number: ", sys.argv[1], "Setting a default port number {}".format(DEFAULT_PORT))
            port = DEFAULT_PORT

    cli = sys.modules["flask.cli"]
    cli.show_server_banner = ara_welcome

    app.run(host="127.0.0.1", port=port, debug=False)
