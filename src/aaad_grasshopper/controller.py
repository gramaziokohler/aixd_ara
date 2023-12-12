"""
This module contains methods that are intended to run in cpython in a server app. 
Do not call it from Rhino/Grasshopper (imports will fail in IronPython).
"""

from aaad.data.dataset import Dataset
from aaad.data.data_objects import DataInt
from aaad.data.data_blocks import DesignParameters, PerformanceAttributes, InputML, OutputML
from aaad.visualisation.plotter import Plotter
from aaad.mlmodel.data.data_loader import DataModule
from aaad.mlmodel.architecture.nn_master_ae import CondAEModel
import os
import pytorch_lightning as pl
import torch
from aaad.mlmodel.generation.generator import Generator
import random
from aaad.data.data_objects import DataBool
from aaad.data.utils_data import (
    reformat_dataframeflat_to_dict,
    reformat_list_to_dict,
    reformat_dict_to_dictlist,
    reformat_dict_to_dataframe,
    reformat_dataframe_to_dataframeflat,
    reformat_dictlist_to_dict,
)
from aaad_grasshopper.shallow_objects import dataobjects_from_shallow
from typing import List, Dict
from aaad_grasshopper.wrappers import WrapperSample
from aaad.utils.utils import flatten_dict


class SessionController(object):
    instances = {}

    def __init__(self):
        self.root_path = None
        self.dataset_name = None
        self.dataset = None
        self.model = None
        self.datamodule = None
        self.samples_per_file = None

    @classmethod
    def create(cls, session_id):
        if session_id not in cls.instances:
            cls.instances[session_id] = cls()
        return cls.instances[session_id]

    def project_setup(self, root_path, dataset_name):
        self.root_path = root_path
        self.dataset_name = dataset_name

    def create_dataset_object(self, design_parameters, performance_attributes):
        """
        Creates a dataset object based on given definitions of dataobjects in shallow formatting.
        """

        if not self.root_path or not self.dataset_name:
            raise ValueError("You need to first set the project root path and the dataset name.")

        dp = DesignParameters(name="DP", dobj_list=dataobjects_from_shallow(design_parameters))
        pa = PerformanceAttributes(name="PA", dobj_list=dataobjects_from_shallow(performance_attributes))

        dataset = Dataset(name=self.dataset_name, design_par=dp, perf_attributes=pa, root_path=self.root_path)

        # TODO: overrides an already assigned dataset - what about the datafiles if they exist?
        self.dataset = dataset

        return True

    def generate_dp_samples(self, n_samples, samples_per_file):
        if not self.dataset:
            raise ValueError("Dataset is not defined. Load or create a Dataset object first.")

        self.samples_per_file = samples_per_file  # keep it for other methods to be able to retrieve it
        self.dataset.sampling(n_samples=n_samples, samples_perfile=samples_per_file, callbacks_class=None, engine="random", flag_sample_distrib=False)

        self.dataset.load()
        data = self.dataset.design_par.data
        samples_dict = reformat_dataframeflat_to_dict(data, self.dataset.design_par.dobj_list)
        samples_dictlist = reformat_dict_to_dictlist(samples_dict)
        return samples_dictlist

    def getdata_design_parameters(self):
        if not self.dataset:
            raise ValueError("Dataset is not defined. Load or create a Dataset object first.")

        self.dataset.load()
        data = self.dataset.design_par.data
        dp_dict = reformat_dataframeflat_to_dict(data, self.dataset.design_par.dobj_list + [DataInt(name="uid", dim=1)])
        dp_dictlist = reformat_dict_to_dictlist(dp_dict)
        return dp_dictlist

    @property
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
        if not self.root_path or not self.dataset_name:
            raise ValueError("You need to first set the project root path and the dataset name.")
        try:
            dataset = Dataset(root_path=self.root_path, name=self.dataset_name)
            dataset.load_dataset_obj()
            dataset.load()
        except:
            dataset = None
            raise ValueError("Loading dataset failed.")

        if not dataset:
            return False

        self.dataset = dataset

        id_to_open = self.dataset.data_gen_dp["fileid_vector"]
        report = "* Loaded a total of {} samples from {} files".format(len(self.dataset.design_par.data), len(id_to_open))

        return report

    def import_data_from_dict(self, datadict, samples_per_file=None):
        """
        Imports data created elsewhere (e.g. performance attributes calculated in Grasshopper) and formated as a dictionary, to the dataset and saves to files.
        datadict: dictionary containing keys equal to object names and values are lists of data values.
                  format: list of n dictionaries datadict[nth_sample][object_name_as_key][ith_dimension]
                  TODO: must also contain an 'uid' key?
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")
        if not samples_per_file:
            samples_per_file = self.samples_per_file
        if not samples_per_file:
            raise ValueError("Argument 'samples per file' is not specified (neither in the project nor given as argument here).")

        datadict = reformat_dictlist_to_dict(datadict)
        dataobjects = [d for d in self.dataset.data_objects if d.name in datadict.keys()]
        df = reformat_dict_to_dataframe(datadict)
        df = reformat_dataframe_to_dataframeflat(df, dataobjects)
        self.dataset.import_data_from_df(data=df, samples_perfile=samples_per_file)

        return True  # confirm it went well

    def dataset_summary(self):
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        flag_only_names = False
        txt = "-------------------------------------\n"
        txt += "Data blocks and elements in dataset\n\n"

        txt += "* Design parameters\n"
        for x in [f"{dobj.name} dim={str(dobj.dim)} domain: {dobj.domain}" for dobj in self.dataset.design_par.dobj_list]:
            txt += f"    {x}\n"

        txt += "\n"
        txt += "* Performance attributes\n"
        for x in [f"{dobj.name} dim={str(dobj.dim)} domain: {dobj.domain}" for dobj in self.dataset.perf_attributes.dobj_list]:
            txt += f"    {x}\n"

        txt += "-------------------------------------"
        return txt

    def get_design_parameters(self):
        # TODO: rename
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")
        print(self.dataset.design_par)
        dp = self.dataset.design_par.names_list
        return dp

    def plot_distrib_attributes(self, dataobjects):
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
        fig = plotter.distrib_attributes(block=block[0], attributes=dataobjects, per_column=True, bottom_top=(0.1, 0.9), downsamp=1, sub_figs=True)
        return fig

    def plot_correlations(self, dataobjects=[]):
        """
        blocks and dataobjects: lists of names
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        if not dataobjects:
            dataobjects = [d.name for d in self.dataset.data_objects]

        blocks = self.blocknames_from_dataobjects(dataobjects)

        plotter = Plotter(self.dataset, output=None)
        fig = plotter.correlation(block=blocks, attributes=dataobjects)
        return fig

    def plot_distrib_attributes2d(self, dataobjects):
        """
        dataobjects: list of dataobject names
        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")
        blocks = self.blocknames_from_dataobjects(dataobjects)

        plotter = Plotter(self.dataset, output=None)
        fig = plotter.distrib_attributes2d(block=blocks, attributes=dataobjects)
        return fig

    def train_cae(self, inputML, outputML, latent_dim, layer_widths, batch_size, epochs):
        # TODO: set defaults here if missing?
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")

        # TODO: move this check to the resp. datablocks so that they recognize "design_parameters" and "performance_attributes" as argument?
        if inputML == ["design_parameters"]:
            inputML = self.dataset.design_par.names_list
        if outputML == ["design_parameters"]:
            outputML = self.dataset.design_par.names_list
        if inputML == ["performance_attributes"]:
            inputML = self.dataset.perf_attributes.names_list
        if outputML == ["performance_attributes"]:
            outputML = self.dataset.perf_attributes.names_list

        datamodule = DataModule.from_dataset(self.dataset, input_ml_names=inputML, output_ml_names=outputML, batch_size=batch_size)
        self.datamodule = datamodule

        cae = CondAEModel.from_datamodule(datamodule, layer_widths=layer_widths, latent_dim=latent_dim)
        cae.fit(
            datamodule,
            name_run="",
            max_epochs=epochs,
            callbacks=[],
            accelerator="cpu",
            flag_wandb=False,
        )
        # TODO: add some callback so that we can have a progress preview in Grasshopper

        # TODO: store the best model in controller?
        self.model = cae

        # TODO: return path to best checkpoint?

        return True

    def load_cae_model(self, checkpoint_path, checkpoint_name, inputML, outputML):
        if checkpoint_path not in [None, ""]:
            if not os.path.exists(checkpoint_path):
                raise ValueError(f"The given checkpoint path does not exist: {checkpoint_path}")
        else:
            if checkpoint_name in [None, ""]:
                checkpoint_name = "last"
            checkpoint_path = os.path.join(
                self.root_path,
                self.dataset_name,
                "checkpoints",
                checkpoint_name + ".ckpt",
            )
            if not os.path.exists(checkpoint_path):
                raise ValueError(f"The given checkpoint name or path does not exist: {checkpoint_path}")

        cae = CondAEModel.load_model_from_checkpoint(checkpoint_path)
        self.model = cae
        self.datamodule = DataModule.from_dataset(
            self.dataset,
            input_ml_names=self.model.datamodule_parameters["input_ml_dblock"].names_list,
            output_ml_names=self.model.datamodule_parameters["output_ml_dblock"].names_list,
            batch_size=self.model.datamodule_parameters["batch_size"],
        )
        return True

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

        if item == None or item < 0:
            n = len(self.dataset.design_par.data)
            item = random.randint(0, n)

        sample = {"design_parameters": {}, "performance_attributes": {}}

        dct = reformat_dataframeflat_to_dict(self.dataset.design_par.data, self.dataset.design_par.dobj_list)
        for key, values in dct.items():
            dct[key] = values[item]
        sample["design_parameters"] = dct

        dct = reformat_dataframeflat_to_dict(self.dataset.perf_attributes.data, self.dataset.design_par.dobj_list)
        for key, values in dct.items():
            dct[key] = values[item]
        sample["performance_attributes"] = dct

        # for single-value entries, unpack them from a list [123] -> 123
        for x in sample.keys():
            for k, v in sample[x].items():
                if len(v) == 1:
                    sample[x][k] = v[0]
        return sample

    def request_designs(self, n, request):
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
            List containing generated samples. Each sample is represented by a dictionary containing dataobject names as keys and values (requested, generated or predicted)

        """
        if not self.dataset:
            raise ValueError("Dataset is not loaded.")
        if not self.model:
            raise ValueError("NN model is not loaded.")

        def fake_generator(n):
            new_designs = []
            for i in range(n):
                one_design = {"design_parameters": {}, "performance_attributes": {}}
                for dp in self.dataset.data_blocks["design_parameters"].dobj_list_orig:
                    name = dp.name
                    vals = list(dp.random_samples(dp.dim))
                    if "int" in dp.dtype:
                        vals = [int(x) for x in vals]
                    if "float" in dp.dtype:
                        vals = [float(x) for x in vals]
                    if name not in one_design["design_parameters"].keys():
                        one_design["design_parameters"][name] = []
                    one_design["design_parameters"][name] = vals
                new_designs.append(one_design)

            return new_designs  # list of dictionaries

        def true_generator(n, request):
            """
            returns a list of dictionaries containing generated ("predicted designs")
            each dict contains two entries: "design_parameters" and "performance_attributes", their values are dicts again
            these dicts contain names of data objects as keys, and the values (possibly list or lists of lists)
            """

            def generate_novel_designs(dataset, model, datamodule, request, n_results, as_list=True):
                generator = Generator(dataset, model, datamodule, over_sample=100)

                attributes = list(request.keys())
                y_req = [request[k] for k in attributes]
                dict_out = generator.generation(y_req=y_req, attributes=attributes, n_samples=n_results, flag_norm=True, flag_peratt=False)

                columns_inML = []
                for do in datamodule.input_ml_dblock.dobj_list_orig:
                    columns_inML.extend(do.columns_df)

                columns_outML = []
                for do in datamodule.output_ml_dblock.dobj_list_orig:
                    columns_outML.extend(do.columns_df)

                x_pred = dict_out["all"]["unnormalize"]["x_gen_best"]  # n_samplesx60 -> 5 constellations + 5x11 radii
                inML_dict = reformat_list_to_dict(x_pred, datamodule.input_ml_dblock.dobj_list_orig, as_list)

                ind_best = dict_out["all"]["ind_sort"][: len(x_pred)]
                y_pred = dict_out["all"]["unnormalize"]["y_est_all"][ind_best]
                # y_pred = list(np.array(y_pred, dtype=float))  # converts to np.float64
                outML_dict = reformat_list_to_dict(y_pred, datamodule.output_ml_dblock.dobj_list_orig, as_list)

                if as_list:
                    all = []
                    for di, do in zip(inML_dict, outML_dict):
                        di.update(do)
                        all.append(di)
                else:
                    inML_dict.update(outML_dict)
                    all = inML_dict

                return all

            all_pred = generate_novel_designs(self.dataset, self.model, self.datamodule, request, n)

            assert len(all_pred) == n
            samples = []

            for d in all_pred:
                s = {"design_parameters": {}, "performance_attributes": {}}
                for k, v in d.items():
                    if k in self.dataset.design_par.names_list:
                        s["design_parameters"][k] = v
                    if k in self.dataset.perf_attributes.names_list:
                        s["performance_attributes"][k] = v
                        print(type(v))
                samples.append(s)
            return samples

        # generated = fake_generator(n)
        generated = true_generator(n, request)
        return generated

    def _model_summary(self, model=None, max_depth=-1):
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
        return str(pl.utilities.model_summary.ModelSummary(model, max_depth=max_depth))

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
