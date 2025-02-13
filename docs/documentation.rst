.. _documentation:

*************
Documentation
*************

This is the documentation of the Grasshopper components in **ARA**. 

The documentation of **AIXD: AI-eXtended Design** tookit can be found `here <https://aixd.ethz.ch/docs/api.html>`_. 

DataBool
--------
.. image:: _images/icons/ara_DataBool.png
	:align: left
	:height: 24
	:width: 24

Defines a boolean variable.


**Inputs**

- **name** *(str)* -- Name of the variable.
- **dim** *(int)* -- Dimension of the variable.

**Outputs**

- **dataobject** -- Data object.

DataCategorical
---------------
.. image:: _images/icons/ara_DataCat.png
	:align: left
	:height: 24
	:width: 24

Defines a categorical variable.


**Inputs**

- **name** *(str)* -- Name of the variable.
- **dim** *(int)* -- Dimension of the variable.
- **options** *[List of (str)]* -- Options: list of possible categories, as strings.

**Outputs**

- **dataobject** -- Data object.

DataInt
-------
.. image:: _images/icons/ara_DataInt.png
	:align: left
	:height: 24
	:width: 24

Defines an integer-valued variable.


**Inputs**

- **name** *(str)* -- Name of the variable.
- **dim** *(int)* -- Dimension of the variable.
- **domain** *(interval)* -- Domain of the variable as an interval.

**Outputs**

- **dataobject** -- Data object.

DataObjectsNames
----------------
.. image:: _images/icons/ara_DataObjectsNames.png
	:align: left
	:height: 24
	:width: 24

Generates panels with list of names of data objects for all existing data blocks.


**Inputs**

- **get_names** *(bool)* -- Set to True to run.

DataReal
--------
.. image:: _images/icons/ara_DataReal.png
	:align: left
	:height: 24
	:width: 24

Defines a real-valued variable.


**Inputs**

- **name** *(str)* -- Name of the variable.
- **dim** *(int)* -- Dimension of the variable.
- **domain** *(interval)* -- Domain of the variable as an interval.

**Outputs**

- **dataobject** -- Data object.

DatasetCreate
-------------
.. image:: _images/icons/ara_DatasetCreate.png
	:align: left
	:height: 24
	:width: 24

Creates a dataset object. This defines the structure of the dataset. It does not cointain any data.


**Inputs**

- **design_parameters** *[List of (none)]* -- Design parameters: list of data objects.
- **performance_attributes** *[List of (none)]* -- Performance attributes: list of data objects.
- **create** *(bool)* -- Set to True to create a dataset object. If a dataset already exists in the project path, nothing will happen. To create a new dataset, change the project path or dataset name or delete the existing dataset.

**Outputs**

- **msg** -- Message or error.

DatasetGenerator
----------------
.. image:: _images/icons/ara_DatasetGenerator.png
	:align: left
	:height: 24
	:width: 24

Provides instructions on how to generate random samples for the dataset.


**Outputs**

- **instructions** -- Information on how to run the `dataset_generator` script.

DatasetLoad
-----------
.. image:: _images/icons/ara_DatasetLoad.png
	:align: left
	:height: 24
	:width: 24

Loads an existing dataset from the file system, from the location specified in the project setup. It loads the dataset object and the data into the app.


**Inputs**

- **load** *(bool)* -- Set to True to load the dataset.

**Outputs**

- **msg** -- 

DatasetOneSample
----------------
.. image:: _images/icons/ara_DatasetOneSample.png
	:align: left
	:height: 24
	:width: 24

Retrieves one sample from the dataset (at a given or random index) and instantiates it in the parametric model.


**Inputs**

- **item** *(int)* -- Index of the sample in the dataset, optional. If not provided, a random index will be selected.
- **get** *(bool)* -- Set to True to retrieve a sample.

**Outputs**

- **sample_summary** -- Summary of the retrieved sample.

DatasetsMerge
-------------
.. image:: _images/icons/ara_DatasetsMerge.png
	:align: left
	:height: 24
	:width: 24

Merges multiple datasets into a single dataset. Requires that the datasets have the same schema (variable names, types, dimensions).


**Inputs**

- **root_folder** *(str)* -- Path to the folder containing the datasets to merge.
- **new_dataset_name** *(str)* -- Name of the merged dataset. (Optional, default: 'merged_dataset'.)
- **samples_per_file** *(int)* -- Number of samples to be saved in each file of the new dataset. (Optional, default: 1000.)
- **merge** *(bool)* -- Triggers the merge process.

**Outputs**

- **msg** -- Message logs.

DatasetSummary
--------------
.. image:: _images/icons/ara_DatasetSummary.png
	:align: left
	:height: 24
	:width: 24

Provides a summary of the dataset.


**Inputs**

- **get** *(bool)* -- Set to True to get the summary of the dataset.

**Outputs**

- **summary** -- Summary of the dataset.

Generator
---------
.. image:: _images/icons/ara_Generator.png
	:align: left
	:height: 24
	:width: 24

Runs a generation campaing to create new designs using the trained model.


**Inputs**

- **requested_values** *[List of (str)]* -- List of requested values, each formatted as a string with the following format: 'variable_name:value'.
- **n_designs** *(int)* -- Number of designs to generate.
- **generate** *(bool)* -- Set to True to start the generation process.
- **clear** *(bool)* -- Forget the previously generated designs.
- **pick_previous** *(bool)* -- Iterate backward through the list of generated designs, instantiate the previous sample.
- **pick_next** *(bool)* -- Iterate forward through the list of generated designs, instantiate the next sample.

**Outputs**

- **sample_summary** -- Selected sample.

ModelDimensions
---------------
.. image:: _images/icons/ara_ModelDims.png
	:align: left
	:height: 24
	:width: 24

Retrieves dimensions of the model's input and output layers.


**Inputs**

- **get** *(bool)* -- Set to True to retrieve input and output dimensions of the model.

**Outputs**

- **summary** -- Summary of the model's input and output dimensions.

ModelLoad
---------
.. image:: _images/icons/ara_ModelLoad.png
	:align: left
	:height: 24
	:width: 24

Loads an existing, pre-traind neural network model from a checkpoint.


**Inputs**

- **model_type** *(str)* -- Type of the autoencoder model. Options are: 'CAE' (conditional Autoencoder) and 'CVAE' (conditional Variational Autoencoder). Default: 'CAE'.
- **checkpoint_name** *(str)* -- Name of the checkpoint file to load the model from, without the file extension. The file's extension must be .ckpt
- **checkpoint_path** *(str)* -- Path to the directory containing the checkpoint file.
- **load** *(bool)* -- Set to True to load the model.

**Outputs**

- **msg** -- Confirmation of the model loading, or an error message.

ModelSetup
----------
.. image:: _images/icons/ara_ModelSetup.png
	:align: left
	:height: 24
	:width: 24

Sets up an autoencoder model of the specified type with the given parameters.


**Inputs**

- **model_type** *(str)* -- Type of the autoencoder model. Options are: 'CAE' (conditional Autoencoder) and 'CVAE' (conditional Variational Autoencoder). Default: 'CAE'.
- **features** *[List of (str)]* -- List of variable names to be used as input to the model.
- **targets** *[List of (str)]* -- List of variable names to be used as output from the model.
- **latent_dim** *(int)* -- Dimension of the latent space.
- **hidden_layers** *[List of (int)]* -- Width of each hidden layer (list of int).
- **batch_size** *(int)* -- Size of the training batches
- **set** *(bool)* -- Set to True to set up the model.

**Outputs**

- **quick_summary** -- Quick summary of the model.
- **model_dims** -- Input and output dimensions of the model.

ModelSummary
------------
.. image:: _images/icons/ara_ModelSummary.png
	:align: left
	:height: 24
	:width: 24

Provides a summary of the autoencoder model's architecture.


**Inputs**

- **max_depth** *(int)* -- Sets the depth of the summary. The larger the depth, the more detailed the summary.
- **get** *(bool)* -- Retrieves the model information.

**Outputs**

- **summary** -- Model summary.

ModelTrain
----------
.. image:: _images/icons/ara_ModelTrain.png
	:align: left
	:height: 24
	:width: 24

Runs a training campaign.


**Inputs**

- **epochs** *(int)* -- Number of training epochs.
- **wb** *(str)* -- Weights&Biases: username or team name. If not set, W&B will not be used.
- **run** *(bool)* -- Set to True to start training.

**Outputs**

- **best_ckpt** -- Filename of the best performing checkpoint.
- **path** -- Path to all checkpoints.

PlotContours
------------
.. image:: _images/icons/ara_PlotContours.png
	:align: left
	:height: 24
	:width: 24

Plots the distribution contours for each pair of variables from the data in the dataset.


**Inputs**

- **variables** *[List of (str)]* -- List of names of the variables to be plotted.
- **plot** *(bool)* -- Set to True to (re-)create the plot.

PlotContoursRequest
-------------------
.. image:: _images/icons/ara_PlotContoursRequest.png
	:align: left
	:height: 24
	:width: 24

Plots the predicted values of the requested designs against the distribution contours for each pair of the corresponding variables.


**Inputs**

- **plot** *(bool)* -- Set to True to (re-)create the plot.

PlotCorrelations
----------------
.. image:: _images/icons/ara_PlotCorrelations.png
	:align: left
	:height: 24
	:width: 24

Plots correlation matrix for the given variables from the data in the dataset.


**Inputs**

- **variables** *[List of (str)]* -- List of names of the variables to be plotted.
- **plot** *(bool)* -- Set to True to (re-)create the plot.

PlotDistribution
----------------
.. image:: _images/icons/ara_PlotDistributions.png
	:align: left
	:height: 24
	:width: 24

Plots the distribution of the given variables from the data in the dataset.


**Inputs**

- **variables** *[List of (str)]* -- List of names of the variables to be plotted.
- **plot** *(bool)* -- Set to True to (re-)create the plot.

ProjectSetup
------------
.. image:: _images/icons/ara_ProjectSetup.png
	:align: left
	:height: 24
	:width: 24

Sets up the project in the folder given by `project_root/project_name`.


**Inputs**

- **set** *(bool)* -- 
- **project_root** *(str)* -- Path to the project root folder. If none is given, the default is the parent folder of this Grasshopper file.
- **project_name** *(str)* -- Any name for the project. It will be used to create a folder with the same name in the project root folder. All files will be later saved here.

**Outputs**

- **msg** -- Messages and errors.
- **path** -- Effective path to the project.

Reset
-----
.. image:: _images/icons/ara_Reset.png
	:align: left
	:height: 24
	:width: 24

Resets the current project running in this Grasshopper file.


**Inputs**

- **reset** *(bool)* -- Set to True to reset.

Server
------
.. image:: _images/icons/ara_Server.png
	:align: left
	:height: 24
	:width: 24

Starts and stops the app server.


**Inputs**

- **start** *(bool)* -- Starts the server.
- **stop** *(bool)* -- Stops the server.
- **show_window** *(bool)* -- If True, the server window will be shown. If False, the server window will be hidden. Default: True.

**Outputs**

- **msg** -- Messages or errors.

ShowFolder
----------
.. image:: _images/icons/ara_ShowFolder.png
	:align: left
	:height: 24
	:width: 24

Reveals the folder in the file explorer.


**Inputs**

- **path** *(str)* -- Path to the (local) folder.
- **open** *(bool)* -- Set to True to open the folder in the file explorer.

