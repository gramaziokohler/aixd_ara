from aixd_grasshopper.gh_ui_helper import http_post_request


def project_setup(session_id, root_path, dataset_name):
    data = {"session_id": session_id, "root": root_path, "dataset_name": dataset_name}
    return http_post_request(action="project_setup", data=data)


def create_dataset_object(session_id, design_parameters, performance_attributes):
    data = {"session_id": session_id, "design_parameters": design_parameters, "performance_attributes": performance_attributes}
    return http_post_request(action="create_dataset_object", data=data)


def load_dataset(session_id):
    data = {"session_id": session_id}
    return http_post_request(action="load_dataset", data=data)


def dataset_summary(session_id):
    data = {"session_id": session_id}
    return http_post_request(action="dataset_summary", data=data)


def get_one_sample(session_id, i):
    data = {"session_id": session_id, "item": i}
    return http_post_request(action="get_one_sample", data=data)


def plot_distrib_attributes(session_id, attributes, output_type):
    data = {"session_id": session_id, "attributes": attributes, "output_type": output_type}
    return http_post_request(action="plot_distrib_attributes", data=data)


def plot_contours(session_id, attributes, output_type):
    data = {"session_id": session_id, "attributes": attributes, "output_type": output_type}
    return http_post_request(action="plot_contours", data=data)


def plot_correlations(session_id, attributes, output_type):
    data = {"session_id": session_id, "attributes": attributes, "output_type": output_type}
    return http_post_request(action="plot_correlations", data=data)


def run_training(session_id, settings, epochs):
    data = {"session_id": session_id, "settings": settings, "epochs": epochs}
    return http_post_request(action="run_training", data=data)


def load_model(session_id, checkpoint_name, checkpoint_path, inputML, outputML):
    data = {"session_id": session_id, "checkpoint_name": checkpoint_name, "checkpoint_path": checkpoint_path, "inputML": ",".join(inputML), "outputML": ",".join(outputML)}
    return http_post_request(action="load_model", data=data)


def nn_summary(session_id, max_depth):
    data = {"session_id": session_id, "max_depth": max_depth}
    return http_post_request(action="nn_summary", data=data)


def request_designs(session_id, request, n_designs):
    data = {"session_id": session_id, "requested_values": request, "n_designs": n_designs}
    return http_post_request(action="request_designs", data=data)
