********************************************************************************
Tutorial
********************************************************************************


This tutorial presents the basic workflow of **ARA** in Grasshopper.



Parametric Model
----------------
First, compose the parametric model of your design task in Grasshopper as usual.

Decide which inputs (*design parameters*) and outputs (*performance attributes*) of the model will be used by **ARA** 
and what are their names (unique, case sensitive, no white spaces).

These can be either single values or lists of values, of one of the following types: 

- ``Number`` -- for real-valued variables
- ``Integer`` -- for integer-valued variables
- ``Boolean`` -- for True/False variables
- ``Text`` -- for categorical variables


For **ARA** to access the inputs and outputs of the parametric model, replace the inputs and outputs of the parametric model 
with Grasshopper's **Param** components (``Number``, ``Integer``, ``Boolean``, ``Text``). 
Rename these components:

- for inputs, use the names of the design parameters prefixed with ``GENERATED_``
- for outputs, use the names of the performance attributes prefixed with ``REAL_``


.. hint::

   To reduce the clutter on the Grasshopper canvas, you can collapse the parametric model into a cluster, 
   or reference it using the Hops component. 
   This way, you will be able to have the same definition of your parametric design twice....


App
---
**ARA** runs cpython code in the background via an http server. Use the ``Server`` component to launch the app.


Project setup
-------------
Much of the functionalities of **ARA** use dataset files and model checkpoints stored on disk in pre-defined directories.
Set up the root project directory and the project name using the ``ProjectSetup`` component. 
The project directory ``project_root\project_name`` will be created with the necessary subdirectories.

You can quickly access the project directory with the ``ShowFolder`` component.


Data
----

Design parameters and performance attributes need to be declared in a bit more detail. 
For each variable, create a data object using on of the following components: ``DataReal``, ``DataInt``, ``DataBool``, ``DataCategorical``,
specifying the unique name and dimensionality of the variable. For real, integer and categorical design parameters, also specify their domain.
This domain will be used to generate random design samples.

Connect the data object components to the ``CreateDataset`` component accordingly and run it to set up the definition of the dataset. 



Dataset
-------
Run the ``dataset_generator.py`` script from *Rhino Python Editor* (in Rhino) to generate random design samples for the dataset 
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

You can easily generate a Grasshopper Panel with lists of variable names for the design parameters and performance attributes using the ``DataObjectsNames`` component.

Choose the model type: conditional Autoencoder (cAE) or conditional Variational Autoencoder (cVAE).

Define the number of hidden layers by providing a list of layer widths, and specify the dimension of the latent space.

Use ``ModelTrain`` component to run the training for the specified the number of epochs. 
To track the training process with `Weights&Biases <https://wandb.ai/site>`_ (optional), provide your *w&b entity* (username, team name). 

During the training, checkpoints of the two best models are saved in the ``checkpoints`` subfolder and can be later loaded using the ``ModelLoad`` component.   
The last model state is kept in memory after the training completes.



Generative design
-----------------
To generate new designs using the trained model, first formulate your *request*. 
In the request, specify the name of the variable and the requested target value(s), 
formatted as a list of strings with colon-separaterd pairs of the variable name and the target value(s), for example: 
``myrealvar:3.141``, ``myintvar:42``, ``myboolvar:True``, ``mycatvar:cat``. 
Beside single target value, it is also possible to request values within a given range or domain, for example: 
``myrealvar:[2.718-3.141]``, ``myintvar:[13-42]``, ``mycatvar:[cat,cod]``.

Only the variables earlier defined as *targets* can be requested.


