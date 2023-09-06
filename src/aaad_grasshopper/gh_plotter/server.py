from flask import Flask, request
import time
from aaad.data_objects.data_structures import Dataset
from aaad.visualisation.plotter import Plotter
import base64
import plotly

app = Flask(__name__)

# global variables ("memory storage")
global_root = None
global_dataset_name = None
global_dataset = None


def fig_to_str(fig):
    """
    Convert a plotly figure graph to a string-encoded bytes.
    """
    img_bytes = base64.b64encode(fig.to_image())
    img_string = img_bytes.decode("utf-8")
    return img_string


@app.route("/project_setup", methods=["POST"])
def project_setup():
    data = request.form

    global global_root
    global_root = str(data["root"])

    global global_dataset_name
    global_dataset_name = str(data["dataset_name"])

    return "Project settings set!"


@app.route("/load_dataset", methods=["POST"])
def load_dataset():
    data = request.form
    root = str(data["root"])
    dataset_name = str(data["dataset_name"])

    dataset = Dataset(root_path=root, name=dataset_name)
    dataset.load_dataset_obj()
    dataset.load()

    global global_dataset
    global_dataset = dataset

    return "Dataset loaded!"


@app.route("/plot_browser", methods=["POST"])
def plot_browser():
    data = request.form
    plot_type = data["plot_type"]

    global global_dataset
    dataset = global_dataset

    if not dataset:
        return "Dataset not loaded!"

    plotter = Plotter(dataset, output="plot")

    if plot_type == "distrib_attributes":
        fig = plotter.distrib_attributes(blocks=["performance_attributes"], per_column=True, bottom_top=(0.1, 0.9), downsamp=1)
    elif plot_type == "distrib_attributes2d":
        fig = plotter.distrib_attributes2d(blocks=["performance_attributes"])
    else:
        return "Wrong plot type argument"

    if fig:
        return "Your image is in the browser."
    else:
        return "Plot failed for unknown reason."


@app.route("/plot", methods=["POST"])
def plot():
    data = request.form
    plot_type = data["plot_type"]

    global global_dataset
    dataset = global_dataset

    if not dataset:
        return "Dataset not loaded!"

    plotter = Plotter(dataset, output="txt")

    if plot_type == "distrib_attributes":
        fig = plotter.distrib_attributes(blocks=["performance_attributes"], per_column=True, bottom_top=(0.1, 0.9), downsamp=1)
    elif plot_type == "distrib_attributes2d":
        fig = plotter.distrib_attributes2d(blocks=["performance_attributes"])
    else:
        return "Wrong plot type argument"

    if fig:
        return fig_to_str(fig)
    else:
        return "Plot failed for unknown reason."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
