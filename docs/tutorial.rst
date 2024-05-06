********************************************************************************
Tutorial
********************************************************************************

.. rst-class:: lead

This tutorial presents the basic workflow using **ARA** in Grasshopper.



Parametric Model
----------------
First, compose the parametric design model of your design task in Grasshopper as usual.

Decide which inputs (*design parameters*) and outputs (*performance attributes*) of the parametric model will be used by **ARA**.
These variables can be either single values or lists of values, and of one of the following type: *real*, *integer*, *boolean* or *categorical*.

All variables must have unique names (case sensitive, no white spaces) for the scope of the Grasshopper file.
For **ARA** to access the inputs and outputs of the parametric model, replace the inputs and outputs of the parametric model 
with Grasshopper's **Param** components: 

- ``Number`` -- for real-valued variables
- ``Integer`` -- for integer-valued variables
- ``Boolean`` -- for True/False variables
- ``Text`` -- for categorical variables

Rename these components:

- for inputs, use the names of the design parameters prefixed with ``DP_`` (accronym for *Design Parameters*)
- for outputs, use the names of the performance attributes prefixed with ``PA_`` (accronym for *Performance Attributes*).


.. hint::

   You might want to have two copies of your parametric model definition on the canvas in the same Grasshopper file: 
   one for manually exploring the design space (for example, using sliders to change input values),
   and one for the **ARA** workflow.

   For this, you can collapse the parametric model into a cluster, 
   or reference it using a Hops component, to keep both copies in sync (and to reduce the clutter on the canvas). 


App
---
**ARA** runs cpython code in the background via an http server. Use the ``Server`` component to launch the app.


Project setup
-------------
Much of the functionalities of **ARA** use dataset files and model checkpoints stored on disk in pre-defined directories.
Set up the root project directory and the project name using the ``ProjectSetup`` component. 
The project directory ``project_root\project_name`` will be created with the necessary subdirectories.

For convenience, you can quickly open the project directory in File Explorer with the ``ShowFolder`` component.


Data
----

Design parameters and performance attributes need to be declared in a bit more detail. 
For each variable, create a data object using one of the following components: ``DataReal``, ``DataInt``, ``DataBool``, ``DataCategorical``,
matching the unique variable name, type and dimensionality used in the parametric model. 
For design parameters of type real, integer and categorical, also specify their domain.
This domain will be used to generate random design samples for the dataset.

Connect the data object components to the ``CreateDataset`` component accordingly and run it to set up the definition of the dataset. 



Dataset
-------
Run the ``dataset_generator.py`` script in *Rhino Python Editor* (in Rhino) to generate random design samples for the dataset 
(for this, make sure that only one Grasshopper file is open in Rhino).
The script will prompt you to specify the number of samples to generate and the number of samples to save per batch file.
The generated samples will be saved in the folders ``design_parameters`` and ``performance_attributes`` in the project directory.


Load the dataset using the ``LoadDataset`` component. 

Inspect the summary of the dataset with the ``DatasetSummary`` component.

You can also instantiate a specific or a random design from the dataset with ``Get1Sample`` component. 


Autoencoder models
------------------
To set up the machine learning model, first decide which variables will be used as *features*  and which as *targets*. 
In many cases the features will be the design parameters and the targets the performance attributes, 
but it is also possible to add some of the design parameters to the targets. 
This depends on the design task and the intended used of the generative model.

You can easily generate a Grasshopper Panel with lists of variable names for the design parameters and performance attributes 
defined in the project using the ``DataObjectsNames`` component.

Choose the model type: conditional Autoencoder (cAE) or conditional Variational Autoencoder (cVAE).

Define the number of hidden layers by providing a list of layer widths, and specify the dimension of the latent space.

Use ``ModelTrain`` component to run the training for the specified the number of epochs. 
To track the training process with `Weights&Biases <https://wandb.ai/site>`_ (optional), provide your *w&b entity* (username or team name). 

During the training, checkpoints of the two best models are saved in the ``checkpoints`` subfolder and can be later loaded using the ``ModelLoad`` component.   
The last model state is kept in memory after the training completes.



Generative design
-----------------
To generate new designs using the trained model, first formulate your *request*. 
Only the variables earlier defined as *targets* can be requested.

In the request, specify the name of the variable and the requested target value(s), 
formatted as a list of strings with colon-separaterd pairs of the variable name and the target value(s).
Beside single target value, it is also possible to request values within a given range or a list of options.

Examples:
``myrealvar:3.141``, ``myintvar:42``, ``mycatvar:[cat,cod]``. 

Triggering the  ``Generator`` component will run the generative model to produce new designs based on the request. 
Once generated, the designs can be instantiated in the parametric model one by one 
(use ``pick_next`` and  ``pick_previous`` to browse through the list).


Plotters
--------

Visual analysis of the dataset can give some additional insights on the design space. 
**ARA** provides a selection of plot methods, which can output either a *static* bitmap image 
(using ``PrevImg`` component from the `Bitmap+ <https://www.food4rhino.com/en/app/bitmap>`_ plugin) 
or an *interactive* plot (opening in browser).

- ``Plot Correlations`` -- produces a correlation matrix of the selected variables
- ``Plot Distribution`` -- plots distribution of each selected variable
- ``Plot Contours`` -- plots pair-wise joint distributions of the selected variables as contours


