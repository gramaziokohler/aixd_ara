from aixd_grasshopper.gh_ui_helper import http_post_request


def reset_session(session_id):
    data = {"session_id": session_id}
    return http_post_request(action="reset_session", data=data)


def project_setup(session_id, project_root, project_name):
    data = {"session_id": session_id, "project_root": project_root, "project_name": project_name}
    return http_post_request(action="project_setup", data=data)


def project_setup_info(session_id):
    data = {"session_id": session_id}
    return http_post_request(action="project_setup_info", data=data)


def create_dataset_object(session_id, design_parameters, performance_attributes):
    data = {
        "session_id": session_id,
        "design_parameters": design_parameters,
        "performance_attributes": performance_attributes,
    }
    return http_post_request(action="create_dataset_object", data=data)


def load_dataset(session_id):
    data = {"session_id": session_id}
    return http_post_request(action="load_dataset", data=data)


def dataset_summary(session_id):
    data = {"session_id": session_id}
    return http_post_request(action="dataset_summary", data=data)


def get_dataobject_names_from_block(session_id, datablock_nickname):
    data = {"session_id": session_id, "datablock_nickname": datablock_nickname}
    return http_post_request(action="get_dataobject_names_from_block", data=data)


def get_dataobject_types(session_id):
    data = {"session_id": session_id}
    return http_post_request(action="get_dataobject_types", data=data)


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


def model_setup(session_id, settings):
    data = {"session_id": session_id, "settings": settings}
    return http_post_request(action="model_setup", data=data)


def model_train(session_id, epochs, wb):
    data = {"session_id": session_id, "epochs": epochs, "wb": wb}
    return http_post_request(action="model_train", data=data)


def model_load(session_id, model_type, checkpoint_name, checkpoint_path):
    data = {"session_id": session_id, "model_type": model_type, "checkpoint_name": checkpoint_name, "checkpoint_path": checkpoint_path}
    return http_post_request(action="model_load", data=data)


def nn_summary(session_id, max_depth):
    data = {"session_id": session_id, "max_depth": max_depth}
    return http_post_request(action="nn_summary", data=data)


def model_input_output_dimensions(session_id):
    data = {"session_id": session_id}
    return http_post_request(action="model_input_output_dimensions", data=data)


def request_designs(session_id, request, n_designs):
    data = {"session_id": session_id, "requested_values": request, "n_designs": n_designs}
    return http_post_request(action="request_designs", data=data)
