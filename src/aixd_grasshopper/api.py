import base64

from flask import Flask, request


from controller import SessionController
import json
from compas.data import DataEncoder, DataDecoder


from aixd_grasshopper.constants import default_port
app = Flask(__name__)


@app.route("/project_setup", methods=["POST"])
def project_setup():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    root = data["root"]
    dataset_name = data["dataset_name"]
    result = sc.project_setup(root, dataset_name)
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


@app.route("/plot_contours", methods=["POST"])
def plot_contours():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    output_type = data["output_type"]
    attributes = data["attributes"]
    fig = sc.plot_contours(dataobjects=attributes)
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
    data = json.loads(data)
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


@app.route("/load_model", methods=["POST"])
def load_model():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    checkpoint_path = data["checkpoint_path"]
    checkpoint_name = data["checkpoint_name"]
    inputML = data["inputML"].split(",")
    outputML = data["outputML"].split(",")

    result = "False"
    result = sc.load_cae_model(
        checkpoint_path=checkpoint_path,
        checkpoint_name=checkpoint_name,
        inputML=inputML,
        outputML=outputML,
    )
    response = json.dumps(result, cls=DataEncoder)
    return response 


@app.route("/nn_summary", methods=["POST"])
def nn_summary():
    data = request.data
    data = json.loads(data)
    session_id = data["session_id"]
    sc = SessionController.create(session_id)

    max_depth = data["max_depth"]
    result = sc._model_summary(max_depth=int(max_depth))
    response = json.dumps(result, cls=DataEncoder)  
    return response

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
    import sys

    if len(sys.argv) ==1:
        port = default_port
    else: 
        try:
            port = int(sys.argv[1])
        except ValueError: 
            print("Invalid port number: ",sys.argv[1], "Setting a default port number {}".format(default_port))
            port = default_port

    app.run(host="127.0.0.1", port=port, debug=False)
