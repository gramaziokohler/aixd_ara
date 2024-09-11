from aixd_ara.scripts import dataset_generator

path = dataset_generator.__file__

txt = "INSTRUCTIONS\n------------\n"
txt += "How to generate random samples for a dataset, "
txt += "by harnessing the parametric model defined in this Grasshopper file?\n\n"
txt += "Prepare the inputs and outputs to/from your parametric model as shown in the online documentation>tutorial at "
txt += "https://gramaziokohler.github.io/aixd_ara/latest/tutorial.html\n\n"
txt += "Close all other Grasshopper files in this Rhino app.\n\n"
txt += "Locate the 'dataset_generator.py' file in:\n\n"
txt += "{}\n\n".format(path)
txt += "In Rhino, open the Rhino Python Editor, open 'dataset_generator.py' and run it.\n"
txt += "(Follow the prompts in the Rhino command line)\n\n"

txt += "\n------------\n\n"
txt += "Optionally, add a button to a Rhino toolbar to access the dataset generator more easily:\n"
txt += "> right-click on a toolbar > New Button... \n"
txt += "> in the pop-up window, in Command section, paste:\n\n"
txt += "'! _-RunPythonScript {}'".format(path)

instructions = txt
