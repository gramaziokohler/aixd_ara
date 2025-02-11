"""
This module contains methods that are intended to run in cpython in a server app.
Do not call it from Rhino/Grasshopper (imports will fail in IronPython).
"""

import base64
import os
import random
import shutil
import pandas as pd

import pytorch_lightning as pl
import torch
from aixd.data.data_blocks import DesignParameters
from aixd.data.data_blocks import PerformanceAttributes
from aixd.data.data_objects import DataInt, DataBool, DataCategorical, DataReal
from aixd.data.dataset import Dataset
from aixd.data.utils_data import reformat_dataframe_to_dataframeflat
from aixd.data.utils_data import reformat_dataframeflat_to_dict
from aixd.data.utils_data import reformat_dict_to_dataframe
from aixd.data.utils_data import reformat_dict_to_dictlist
from aixd.data.utils_data import reformat_dictlist_to_dict
from aixd.mlmodel.architecture.cond_ae_model import CondAEModel
from aixd.mlmodel.architecture.cond_vae_model import CondVAEModel
from aixd.mlmodel.data.data_loader import DataModule
from aixd.mlmodel.generation.generator import Generator
from aixd.utils.utils import flatten_dict
from aixd.visualisation.plotter import Plotter

from aixd_ara.shallow_objects import dataobjects_from_shallow


class SessionController(object):
    instances = {}

    def __init__(self):
        self.project_root = None
        self.project_name = None
        self.dataset = None
        self.model = None
        self.datamodule = None
        self.samples_per_file = None
        self.model_is_trained = False
        self.requested_designs = None, None, None

    def reset(self):
        self.project_root = None
        self.project_name = None
        self.dataset = None
        self.model = None
        self.datamodule = None
        self.samples_per_file = None
        self.model_is_trained = False
        self.requested_designs = None, None, None

    @property
    def dataset_path(self):
        if not self.project_root or not self.project_name:
            return None
        return os.path.join(self.project_root, self.project_name)

    @classmethod
    def create(cls, session_id):
        if session_id not in cls.instances:
            cls.instances[session_id] = cls()
        return cls.instances[session_id]

    def project_setup(self, project_root, project_name):
        if not os.path.exists(project_root):
            return {"msg": "Project path {project_root} does not exist!"}
        self.project_root = project_root
        self.project_name = project_name
        return {
            "msg": f"Project has been set up in: {os.path.join(self.project_root, self.project_name)}",
            "path": os.path.join(self.project_root, self.project_name),
        }

    def project_setup_info(self):
        return {"project_root": self.project_root, "project_name": self.project_name}

    def create_dataset_object(self, design_parameters, performance_attributes):
        """
        Creates a dataset object based on given definitions of dataobjects in shallow formatting.
        """

        if not self.project_root or not self.project_name:
            raise ValueError("You need to first set the project root path and the dataset name.")

        dataset_path= os.path.join(self.project_root, self.project_name)
        if len(os.listdir(dataset_path)) > 0:
            msg =f"The folder {self.project_root}\{self.project_name} is not empty!"
            msg+="\nProbably it already contains a Dataset. \nIf yes, if does not need to be defined again."
            msg+="\nIf you want to define a new Dataset, change the project name or the project path, or delete the existing Dataset."
            return {"msg": msg, "status":"warning"}
            
        dp = DesignParameters(name="DP", dobj_list=dataobjects_from_shallow(design_parameters))
        pa = PerformanceAttributes(name="PA", dobj_list=dataobjects_from_shallow(performance_attributes))

        #INFO: we need to use overwrite=True here because of AIXD syntax which only checks for the existence of the folder. 
        #INFO: In ARA this folder is always created before. We prevent overwriting data by checking above if the folder is empty.
        dataset = Dataset(name=self.project_name, design_par=dp, perf_attributes=pa, root_path=self.project_root, overwrite=True) 
        dataset.save_dataset_obj()

        self.dataset = dataset

        return {"msg": f"Dataset object and default subfolders have been created in {dataset_path}.","status":"ok"}

    def generate_dp_samples(self, n_samples):
        if not self.dataset:
            raise ValueError("Dataset is not defined. Load or create a Dataset object first.")

        samples_dictlist = self.dataset.get_samples(n_samples=n_samples, format_out="dict_list")
        return samples_dictlist

    def save_samples(self, samples, samples_per_file):
        """
        Adds samples to dataset, saves them to files and saves the dataset object.
        Samples can be in any of the formats used in the project.
        """
        if not self.dataset:
            raise ValueError("Dataset is not defined. Load or create a Dataset object first.")
        if not samples_per_file:
            samples_per_file = None

        self.dataset.write_data_dp_pa(data_combined=samples, samples_perfile=samples_per_file)
        return True

    def getdata_design_parameters(self):
        if not self.dataset:
            raise ValueError("Dataset is not defined. Load or create a Dataset object first.")

        self.dataset.load()
        data = self.dataset.design_par.data
        dp_dict = reformat_dataframeflat_to_dict(data, self.dataset.design_par.dobj_list + [DataInt(name="uid", dim=1)])
        dp_dictlist = reformat_dict_to_dictlist(dp_dict)
        return dp_dictlist

    def datablocks_dataobjects(self):
        if not self.dataset:
            raise ValueError("Dataset is not defined. Load or create a Dataset object first.")
        blocks = {}
        blocks["design_parameters"] = self.dataset.design_par.names_list
        blocks["performance_attributes"] = self.dataset.perf_attributes.names_list
        return blocks

    @property
    def design_parameters_names(self):
        if not self.dataset:
            raise ValueError("Dataset is not defined. Load or create a Dataset object first.")
        return self.dataset.design_par.names_list

    def load_dataset(self):
        error = ""
        if not self.project_root or not self.project_name:
            error = "You need to first set the project root path and the dataset name."
            raise ValueError(error)
        try:
            dataset = Dataset(root_path=self.project_root, name=self.project_name, overwrite=False)
            dataset.load_dataset_obj()
            dataset.load()
            dataset.update_obj_domains(flag_only_perfatt=True)
        except:  # noqa: E722
            dataset = None
            error = "Loading dataset failed."
            raise ValueError(error)

        if not dataset:
            return {"msg": error}

        self.dataset = dataset

        id_to_open = self.dataset.data_gen_dp["fileid_vector"]
        report = "Loaded a total of {} samples from {} files".format(len(self.dataset.design_par.data), len(id_to_open))

        return {"msg": report}

    def import_data_from_dict(self, datadict, samples_per_file=None):
        """
        Imports data created elsewhere (e.g. performance attributes calculated in Grasshopper) and
        formated as a dictionary, to the dataset and saves to files.
        datadict: dictionary containing keys equal to object names and values are lists of data values.
                  format: list of n dictionaries datadict[nth_sample][object_name_as_key][ith_dimension]
                  TODO: must also contain an 'uid' key?
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")
        if not samples_per_file:
            samples_per_file = self.samples_per_file
        if not samples_per_file:
            raise ValueError(
                "Argument 'samples per file' is not specified (neither in the project nor given as argument here)."
            )

        datadict = reformat_dictlist_to_dict(datadict)
        dataobjects = [d for d in self.dataset.data_objects if d.name in datadict.keys()]
        df = reformat_dict_to_dataframe(datadict)
        df = reformat_dataframe_to_dataframeflat(df, dataobjects)
        self.dataset.import_data_from_df(data=df, samples_perfile=samples_per_file)

        return True  # confirm it went well

    def dataset_summary(self):
        error = ""
        if not self.dataset:
            error = "Dataset is not loaded."
            raise ValueError(error)

        # flag_only_names = False
        txt = "-------------------------------------\n"
        txt += "Data blocks and elements in dataset\n\n"

        txt += "* Design parameters\n"
        for x in [
            f"{dobj.name} dim={str(dobj.dim)} domain: {dobj.domain}" for dobj in self.dataset.design_par.dobj_list
        ]:
            txt += f"    {x}\n"

        txt += "\n"
        txt += "* Performance attributes\n"
        for x in [
            f"{dobj.name} dim={str(dobj.dim)} domain: {dobj.domain}" for dobj in self.dataset.perf_attributes.dobj_list
        ]:
            txt += f"    {x}\n"

        txt += "-------------------------------------"
        return {"msg": error, "summary": txt}

    def get_dataobject_names_from_block(self, datablock_nickname):
        if datablock_nickname in ["design_parameters", "performance_attributes"] and not self.dataset:
            return {"msg": "Dataset is not loaded.", "names": []}
        if datablock_nickname in ["inputML", "outputML"] and not self.datamodule:
            return {"msg": "Model is not loaded.", "names": []}

        if datablock_nickname == "design_parameters":
            return {"msg": "", "names": self.dataset.design_par.names_list}
        if datablock_nickname == "performance_attributes":
            return {"msg": "", "names": self.dataset.perf_attributes.names_list}
        if datablock_nickname == "inputML":
            return {"msg": "", "names": self.datamodule.input_ml_dblock.names_list}
        if datablock_nickname == "outputML":
            return {"msg": "", "names": self.datamodule.output_ml_dblock.names_list}
        return {"msg": f"Wrong block nickname: {datablock_nickname}.", "names": []}

    def cast_to_python_type(self, dataobject_name, value):
        """
        Cast the values (usually coming from a dataframe) to the correct python type.
        Value can be a single value or a list.
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        dobj = self.dataset.get_data_objects_by_name([dataobject_name])[0]

        if not isinstance(value, list):
            value = [value]
            single = True
        else:
            single = False

        if isinstance(dobj, DataInt):
            castvalue = [int(v) for v in value]
        elif isinstance(dobj, DataReal):
            castvalue = [float(v) for v in value]
        elif isinstance(dobj, DataBool):
            castvalue = []
            for v in value:
                if isinstance(v, bool):
                    castvalue.append(v)
                elif isinstance(v, int):
                    castvalue.append(bool(v))
                elif isinstance(v, str):
                    castvalue.append({"True": True, "False": False}[v])
                else:
                    raise ValueError(f"Dataobject type not recognized: {dobj.type}")
        elif isinstance(dobj, DataCategorical):
            castvalue = [str(v) for v in value]
        else:
            raise ValueError(f"Dataobject type not recognized: {dobj.type}")

        if single:
            castvalue = castvalue[0]
        return castvalue

    def get_dataobject_types(self):
        """
        Returns names of the data types of the dataobjects in the dataset.
        """
        if not self.dataset:
            error = "Dataset is not loaded."
            raise ValueError(error)

        all_dataobjects = self.dataset.data_objects
        # cannot use this because boolean are declared as categorical
        # dataobject_types = {d.name: d.type for d in all_dataobjects}

        dataobject_types = {}
        for d in all_dataobjects:
            if isinstance(d, DataInt):
                dataobject_types[d.name] = "integer"
            elif isinstance(d, DataReal):
                dataobject_types[d.name] = "real"
            elif isinstance(d, DataCategorical):
                dataobject_types[d.name] = "categorical"
            elif isinstance(d, DataBool):
                dataobject_types[d.name] = "boolean"
            else:
                dataobject_types[d.name] = "unsupported"

        return {"msg": "", "dataobject_types": dataobject_types}

    def get_design_parameters(self):
        # TODO: rename
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")
        print(self.dataset.design_par)
        dp = self.dataset.design_par.names_list
        return dp

    def plot_distrib_attributes(self, dataobjects, output_type):
        """
        dataobjects: list of dataobject names
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        if not dataobjects:
            block = self.dataset.perf_attributes.name  # by default, we're interested in performance attributes here
        else:
            block = self.blocknames_from_dataobjects(dataobjects)
            if len(block) > 1:
                raise ValueError("Dataobjects are not from the same block.")
            if len(block) == 0:
                raise ValueError("Dataobjects are not from any block.")

        plotter = Plotter(self.dataset, output=None)
        fig = plotter.distrib_attributes(
            block=block[0], attributes=dataobjects, per_column=True, bottom_top=(0.1, 0.9), downsamp=1, sub_figs=True
        )
        return _fig_output(fig, output_type)

    def plot_correlations(self, dataobjects, output_type):
        """
        blocks and dataobjects: lists of names
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        if not dataobjects:
            dataobjects = [d.name for d in self.dataset.data_objects]

        blocks = self.blocknames_from_dataobjects(dataobjects)

        plotter = Plotter(self.dataset, output=None)
        fig = plotter.correlation(blocks=blocks, attributes=dataobjects)
        return _fig_output(fig, output_type)

    def plot_contours(self, dataobjects, output_type):
        """
        dataobjects: list of dataobject names
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")
        blocks = self.blocknames_from_dataobjects(dataobjects)

        plotter = Plotter(self.dataset, output=None)
        fig = plotter.contours2d(blocks=blocks, attributes=dataobjects)
        return _fig_output(fig, output_type)

    def plot_contours_request(self, output_type):
        """
        request:
            dictionary where keys are the names of dataobjects (usually performance attributes),
            and values the requested target value(s).
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")
        if not self.model:
            raise ValueError("Model is not loaded.")
        if self.requested_designs == (None, None, None):
            raise ValueError("No designs have been requested yet.")

        plotter = Plotter(datamodule=self.datamodule, output=None)
        detailed_results = self.requested_designs[2]
        n_samples = len(self.requested_designs[1])

        fig = plotter.generation_scatter([detailed_results], n_samples=n_samples)
        return _fig_output(fig, output_type)

    def model_setup(self, model_type, inputML, outputML, latent_dim, layer_widths, batch_size):
        # TODO: set defaults here if missing?
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        # TODO: move this check to the resp. datablocks so that
        # they recognize "design_parameters" and "performance_attributes" as argument?
        if inputML == ["design_parameters"]:
            inputML = self.dataset.design_par.names_list
        if outputML == ["design_parameters"]:
            outputML = self.dataset.design_par.names_list
        if inputML == ["performance_attributes"]:
            inputML = self.dataset.perf_attributes.names_list
        if outputML == ["performance_attributes"]:
            outputML = self.dataset.perf_attributes.names_list

        datamodule = DataModule.from_dataset(
            self.dataset, input_ml_names=inputML, output_ml_names=outputML, batch_size=batch_size
        )
        self.datamodule = datamodule

        save_dir = self.dataset_path

        if model_type == "CAE":
            model = CondAEModel.from_datamodule(
                datamodule, layer_widths=layer_widths, latent_dim=latent_dim, save_dir=save_dir
            )
        elif model_type == "CVAE":
            model = CondVAEModel.from_datamodule(
                datamodule, layer_widths=layer_widths, latent_dim=latent_dim, save_dir=save_dir
            )
        else:
            raise ValueError("Model type not recognized. Choose 'CAE' or 'CVAE'.")

        self.model = model
        self.model_is_trained = False

        quick_summary = self.model_summary(self.model, max_depth=2)
        model_dims = self.model_input_output_dimensions()
        return {"msg": "Model has been set up.", "quick_summary": quick_summary, "model_dims": model_dims}

    def model_train(self, epochs, wb):
        if not self.model:
            raise ValueError("Model is not set up. Try setting up a model first.")
        self.model_is_trained = False

        if not wb:
            log_wb = False
        else:
            log_wb = True

        self.model.fit(
            self.datamodule,
            name_run="",
            max_epochs=epochs,
            callbacks=[],
            accelerator="cpu",
            flag_wandb=log_wb,
            wandb_entity=wb,
        )
        self.model_is_trained = True
        # TODO: store the best model in controller instead?
        checkpoint_path = os.path.join(self.model.save_dir, self.model.CHECKPOINT_DIR)

        # TODO: add some callback so that we can have a progress preview in Grasshopper
        # TODO: still saving the checkpoints in strange locations!!! return path to best checkpoint
        # TODO: add retrieve and return the name/path of the best checkpoint

        return {"msg": "Training completed!", "path": checkpoint_path, "best_ckpt": None}

    def model_load(self, model_type, checkpoint_path, checkpoint_name):
        error = None
        if checkpoint_path not in [None, ""]:
            if not os.path.exists(checkpoint_path):
                error = f"The given checkpoint path does not exist: {checkpoint_path}"
                raise ValueError(error)
        else:
            # default to the project path
            checkpoint_path = os.path.join(self.dataset_path, "checkpoints")

        checkpoint_filepath = os.path.join(checkpoint_path, checkpoint_name + ".ckpt")
        if not os.path.exists(checkpoint_path):
            error = f"The given checkpoint path does not exist: {checkpoint_filepath}"
            raise ValueError(error)

        if model_type == "CAE":
            model = CondAEModel.load_model_from_checkpoint(checkpoint_filepath)
        elif model_type == "CVAE":
            model = CondVAEModel.load_model_from_checkpoint(checkpoint_filepath)
        else:
            raise ValueError("Model type not recognized. Choose 'CAE' or 'CVAE'.")

        self.model = model
        self.model_is_trained = True
        self.datamodule = self._datamodule_from_dataset()
        return {"msg": error or f"Model loaded from checkpoint: {checkpoint_filepath}"}

    def _datamodule_from_dataset(self):
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        datamodule = DataModule.from_dataset(
            self.dataset,
            input_ml_names=self.model.datamodule_parameters["input_ml_dblock"].names_list,
            output_ml_names=self.model.datamodule_parameters["output_ml_dblock"].names_list,
            batch_size=self.model.datamodule_parameters["batch_size"],
        )
        return datamodule

    def get_one_sample(self, item):
        """
        Returns a single sample from the dataset as a dictionary.

        Parameters
        ----------
        item : int >=-1 or None
            Index of the sample. If None or -1, a random sample will be drawn.

        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        if item is None or item < 0:
            n = len(self.dataset.design_par.data)
            item = random.randint(0, n)

        dp_df = self.dataset.design_par.data.iloc[item]  # pd.series
        pa_df = self.dataset.perf_attributes.data.iloc[item]  # pd.series

        def _reduce_list(x):
            # if the list has only one element, return the element instead of a list
            if isinstance(x, list):
                if len(x) == 1:
                    return x[0]
            return x

        sample = {"design_parameters": {}, "performance_attributes": {}}
        for name, values in dp_df.items():
            if name == "uid":
                continue
            typed_values = self.cast_to_python_type(name, values)
            sample["design_parameters"][name] = _reduce_list(typed_values)

        for name, values in pa_df.items():
            if name in ["uid", "error"]:
                continue
            typed_values = self.cast_to_python_type(name, values)
            sample["performance_attributes"][name] = _reduce_list(typed_values)

        return sample

    def request_designs(self, request, n_samples=1):
        """
        Parameters
        ----------
        n: int
            number of designs to return
        request: [Dict]
            dictionary where keys are the names of dataobjects (usually performance attributes),
            and values are the requested target values to fulfil
            Example:
            request = {"attribute1": 123,"attribute2":[45.0,67.0] }

        Returns
        -------
        List[Dict]
            List containing generated samples. Each sample is represented by a dictionary containing
            dataobject names as keys and values (requested, generated or predicted)

        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")
        if not self.model:
            raise ValueError("Model is not loaded.")

        gen = Generator(model=self.model, datamodule=self.datamodule, over_sample=100)
        new_designs, detailed_results = gen.generate(request=request, n_samples=n_samples, format_out="dict_list")
        self.requested_designs = request, new_designs, detailed_results
        # split the result into separate dictionaries for design parameters and performance attributes
        # assert len(new_designs) == n_samples
        samples = []
        for d in new_designs:
            s = {"design_parameters": {}, "performance_attributes": {}}
            for k, v in d.items():
                if k in self.dataset.design_par.names_list:
                    s["design_parameters"][k] = v
                if k in self.dataset.perf_attributes.names_list:
                    s["performance_attributes"][k] = v
            samples.append(s)

        return {"msg": "", "generated": samples}

    def model_summary(self, model=None, max_depth=-1):

        if not model:
            model = self.model
        if not model:
            raise ValueError("No NN model given or loaded.")

        model.example_input_array = (
            (
                torch.zeros(
                    1,
                    max([x_dobj.position_index + x_dobj.dim for x_dobj in model.input_ml_dblock.dobj_list_transf]),
                ),
                torch.zeros(
                    1,
                    max([y_dobj.position_index + y_dobj.dim for y_dobj in model.input_ml_dblock.dobj_list_transf]),
                ),
            ),
        )
        summary = str(pl.utilities.model_summary.ModelSummary(model, max_depth=max_depth))
        return {"summary": summary}

    def model_input_output_dimensions(self):
        if not self.datamodule:
            raise ValueError("DataModule is not loaded. Try loading a model first.")

        inputdim, outputdim, summary = self.datamodule.summary_input_output_dimensions()
        return {"msg": "", "summary": summary}

    def all_block_names(self):
        """
        Returns all block names in the dataset.
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        datablocks = flatten_dict(self.dataset.data_blocks)
        names = [db.name for db in datablocks]
        return names

    def blocknames_from_dataobjects(self, dataobjects):
        """
        Returns the name of the block that contains the given dataobjects (given by their name).
        """
        datablocks = flatten_dict(self.dataset.data_blocks)  # list of all blocks

        blocknames = []
        for block in datablocks:
            for dobjname in dataobjects:
                if dobjname in block.names_list:
                    blocknames.append(block.name)

        return list(set(blocknames))

    @staticmethod
    def merge_datasets(root_folder: str, new_dataset_name: str, samples_per_file: int):
        """
        This function merges all datasets in the root_folder into a new dataset with the name new_dataset_name.
        Prerequisites:
        - All datasets are stored in subfolders of the root_folder
        - Each dataset has the same design_parameters and performance_attributes (variable names, types, dimensions)

        Parameters:
        -----------
        root_folder: str
            Path to the root folder containing the datasets.
        new_dataset_name: str
            Name of the new dataset. The new dataset will be created in a subfolder with this name. \
                Default is "merged_dataset".
            If such a folder already exists, it will be overwritten.

        Returns:
        --------
        status : str
            Status of the process: "warning", "error" or None
        msg : str
            A message containing information about the process.
        """
        # TODO: check what happens with the domains, may need to get a union explicitly.

        status = None
        msg = ""

        if not os.path.exists(root_folder):
            txt = f"Folder {root_folder} does not exist.\n"
            status = "error"
            return status, txt

        if not new_dataset_name:
            new_dataset_name = "merged_dataset"

        if os.path.exists(os.path.join(root_folder, new_dataset_name)):
            txt = f"[WARNING] Folder {new_dataset_name} already exists. It will be overwritten.\n\n"
            status = "warning"
            print(txt)
            msg += txt
            shutil.rmtree(os.path.join(root_folder, new_dataset_name))

        dataset_names = [
            name
            for name in os.listdir(root_folder)
            if os.path.isdir(os.path.join(root_folder, name)) and name != new_dataset_name
        ]
        txt = f"Found following subfolders: {dataset_names}.\n\n"
        print(txt)
        msg += txt

        def _load_df(root_folder, dataset_name):
            # Load old sharded data from pickled dataframes

            # DPs
            directory = os.path.join(root_folder, dataset_name, "design_parameters")
            df_dp_all = []

            for filename in os.listdir(directory):
                if filename.endswith(".pkl"):
                    filepath = os.path.join(directory, filename)
                    df = pd.read_pickle(filepath)
                    df_dp_all.append(df)

            df_dp_all = pd.concat(df_dp_all, axis=0)

            # PAs
            directory = os.path.join(root_folder, dataset_name, "performance_attributes")
            df_pa_all = []

            for filename in os.listdir(directory):
                if filename.endswith(".pkl"):
                    filepath = os.path.join(directory, filename)
                    df = pd.read_pickle(filepath)
                    df_pa_all.append(df)

            df_pa_all = pd.concat(df_pa_all, axis=0)
            df_all = pd.merge(df_dp_all, df_pa_all, how="inner", on=["uid"])
            df_all = df_all.drop(columns=["uid"])
            return df_all

        # load all datasets into a single dataframe
        dfs = []
        for dataset_name in dataset_names:
            df = _load_df(root_folder, dataset_name)
            dfs.append(df)
        df_all = pd.concat(dfs)

        # create new Dataset, take one of the old datasets as a template
        dataset_temp = Dataset.from_dataset_folder(os.path.join(root_folder, dataset_names[0]))

        dataset_new = Dataset(
            name=new_dataset_name,
            root_path=root_folder,
            file_format="json",
            design_par=dataset_temp.design_par,
            perf_attributes=dataset_temp.perf_attributes,
            overwrite=True,
        )

        # load data
        dataset_new.import_data_from_df(df_all, samples_perfile=samples_per_file, flag_fromscratch=True)
        msg += f"New dataset with {len(df_all)} samples has been created in \
            {os.path.join(root_folder, new_dataset_name)}.\n"
        return {"status": status, "msg": msg}


# --------------------------------------------------------------
# helper methods
# --------------------------------------------------------------


def _fig_output(fig, output_type):
    if not fig:
        return {"msg": "Plot failed."}

    if output_type == "static":
        imgstr = _fig_to_str(fig)
        return {"msg": "Static plot has been created.", "imgstr": imgstr}

    elif output_type == "interactive":
        fig.show()
        return {"msg": "Interactive plot has been launched in a new browser window."}


def _fig_to_str(fig):
    """
    Convert a plotly figure graph to a string-encoded bytes.
    """
    img_bytes = base64.b64encode(fig.to_image())
    img_string = img_bytes.decode("utf-8")
    return img_string
