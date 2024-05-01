.. _documentation:

*************
Documentation
*************

This is the documentation of the Grasshopper components in **ARA**. 

The documentation of **AIXD: AI-eXtended Design** tookit can be found `here <https://aixd.ethz.ch/docs/api.html>`_. 

DataBool
--------
.. image:: _images/icons/aixd_DataBool.png
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
.. image:: _images/icons/aixd_DataCat.png
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
.. image:: _images/icons/aixd_DataInt.png
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
.. image:: _images/icons/aixd_DataObjectsNames.png
	:align: left
	:height: 24
	:width: 24

Generates panels with list of names of data objects for all or selected data blocks. Data block names are: 'design_parameters','performance_attributes','inputML','outputML'. 


**Inputs**

- **datablock** *[List of (str)]* -- Name(s) of the datablock(s).
- **get_names** *(bool)* -- Set to True to run.

DataReal
--------
.. image:: _images/icons/aixd_DataReal.png
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
.. image:: _images/icons/aixd_DatasetCreate.png
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

DatasetLoad
-----------
.. image:: _images/icons/aixd_DatasetLoad.png
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
.. image:: _images/icons/aixd_DatasetOneSample.png
	:align: left
	:height: 24
	:width: 24

Retrieves one sample from the dataset (at a given or random index) and instantiates it in the parametric model.


**Inputs**

- **item** *(int)* -- Index of the sample in the dataset, optional. If not provided, a random index will be selected.
- **get** *(bool)* -- Set to True to retrieve a sample.

**Outputs**

- **sample** -- Summary of the retrieved sample.

DatasetSummary
--------------
.. image:: _images/icons/aixd_DatasetSummary.png
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
.. image:: _images/icons/aixd_Generator.png
	:align: left
	:height: 24
	:width: 24

Runs a generation campaing to create new designs using the trained model.


**Inputs**

- **requested_values** *(str)* -- List of requested values, each formatted as a string with the following format: 'variable_name:value'.
- **n_designs** *(int)* -- Number of designs to generate.
- **run** *(none)* -- Set to True to start the generation process.

**Outputs**

- **predicions** -- List of generated designs.

GenSampleEval
-------------
.. image:: _images/icons/aixd_GenSampleEval.png
	:align: left
	:height: 24
	:width: 24

Compares the requested values with the predicted and the actual values for a current design.


**Inputs**

- **request** *(none)* -- Requested values.
- **predicted** *(none)* -- Predicted values (the generated sample).
- **real** *(none)* -- Actual values (the current design).

**Outputs**

- **comparison** -- Table with the comparison of the requested, predicted and actual values.

GenSelect
---------
.. image:: _images/icons/aixd_GenSelect.png
	:align: left
	:height: 24
	:width: 24

Selects one of the designs generated from the trained model.


**Inputs**

- **predictions** *[List of (none)]* -- List of generated designs.
- **select** *(int)* -- Index of the selected design.

**Outputs**

- **sample_summary** -- Summary of the selected design.
- **generated_sample** -- Sample.

ModelDimensions
---------------
.. image:: _images/icons/aixd_ModelDims.png
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
.. image:: _images/icons/aixd_ModelLoad.png
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
.. image:: _images/icons/aixd_ModelSetup.png
	:align: left
	:height: 24
	:width: 24

Sets up an autoencoder model of the specified type with the given parameters.


**Inputs**

- **model_type** *(str)* -- Type of the autoencoder model. Options are: 'CAE' (conditional Autoencoder) and 'CVAE' (conditional Variational Autoencoder). Default: 'CAE'.
- **inputML** *[List of (str)]* -- List of variable names to be used as input to the model.
- **outputML** *[List of (str)]* -- List of variable names to be used as output from the model.
- **latent_dim** *(int)* -- Dimension of the latent space.
- **hidden_layers** *[List of (int)]* -- Width of each hidden layer (list of int).
- **batch_size** *(int)* -- Size of the training batches
- **set** *(bool)* -- Set to True to set up the model.

**Outputs**

- **quick_summary** -- Quick summary of the model.
- **model_dims** -- Input and output dimensions of the model.

ModelSummary
------------
.. image:: _images/icons/aixd_ModelSummary.png
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
.. image:: _images/icons/aixd_ModelTrain.png
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
.. image:: _images/icons/aixd_PlotContours.png
	:align: left
	:height: 24
	:width: 24

Plots the distribution contours for each pair of variables from the data in the dataset.


**Inputs**

- **variables** *[List of (str)]* -- List of names of the variables to be plotted.
- **output_type** *(str)* -- Plot type: 'static' creates a bitmap image, 'interactive' launches an interactive plot in a browser.
- **plot** *(bool)* -- Set to True to (re-)create the plot.
- **scale** *(float)* -- Resize factor for the static plot.

**Outputs**

- **img** -- Bitmap image if output_type is 'static', otherwise None.

PlotCorrelations
----------------
.. image:: _images/icons/aixd_PlotCorrelations.png
	:align: left
	:height: 24
	:width: 24

Plots correlation matrix for the given variables from the data in the dataset.


**Inputs**

- **variables** *[List of (str)]* -- List of names of the variables to be plotted.
- **output_type** *(str)* -- Plot type: 'static' creates a bitmap image, 'interactive' launches an interactive plot in a browser.
- **plot** *(bool)* -- Set to True to (re-)create the plot.
- **scale** *(float)* -- Resize factor for the static plot.

**Outputs**

- **img** -- Bitmap image if output_type is 'static', otherwise None.

PlotDistribution
----------------
.. image:: _images/icons/aixd_PlotDistributions.png
	:align: left
	:height: 24
	:width: 24

Plots the distribution of the given variables from the data in the dataset.


**Inputs**

- **variables** *[List of (str)]* -- List of names of the variables to be plotted.
- **output_type** *(str)* -- Plot type: 'static' creates a bitmap image, 'interactive' launches an interactive plot in a browser.
- **plot** *(bool)* -- Set to True to (re-)create the plot.
- **scale** *(float)* -- Resize factor for the static plot.

**Outputs**

- **img** -- Bitmap image if output_type is 'static', otherwise None.

ProjectSetup
------------
.. image:: _images/icons/aixd_ProjectSetup.png
	:align: left
	:height: 24
	:width: 24

Sets up the project in the folder given by `project_root/project_name`.


**Inputs**

- **set** *(bool)* -- 
- **project_root** *(str)* -- Path to the project root folder.
- **project_name** *(str)* -- Any name for the project. It will be used to create a folder with the same name in the project root folder. All files will be later saved here.

**Outputs**

- **msg** -- Messages and errors.
- **path** -- Effective path to the project.

Reset
-----
.. image:: _images/icons/aixd_Reset.png
	:align: left
	:height: 24
	:width: 24

Resets the current project running in this Grasshopper file.


**Inputs**

- **reset** *(bool)* -- Set to True to reset.

Server
------
.. image:: _images/icons/aixd_Server.png
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
.. image:: _images/icons/aixd_ShowFolder.png
	:align: left
	:height: 24
	:width: 24

Reveals the folder in the file explorer.


**Inputs**

- **path** *(str)* -- Path to the (local) folder.
- **open** *(bool)* -- Set to True to open the folder in the file explorer.

Weights&Biases
--------------
.. image:: _images/icons/aixd_W&B.png
	:align: left
	:height: 24
	:width: 24

Launches Weights&Biases dashboard for model training and monitoring in a browser.


**Inputs**

- **user** *(str)* -- Part of the path containing username and project name, typically in the form of 'username/projectname'
- **launch** *(bool)* -- Set to True to launch the dashboard.

