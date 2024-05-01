from aixd_grasshopper.scripts import dataset_generator

path = dataset_generator.__file__

txt = "INSTRUCTIONS\n------------\n"
txt += "How to generate random samples for the dataset.\n\n"
txt += "Locate the 'dataset_generator.py' file in:\n\n"
txt += "{}\n\n".format(path)
txt += "In Rhino, open the Rhino Pythin Editor, open the file and run it.\n"
txt += "(Follow the prompts in the Rhino command line)\n\n"
txt += "Optionally, add a button to a Rhino toolbar to access the dataset generator more easily:\n"


txt += "> right-click on a toolbar > New Button... \n"
txt += "> in the pop-up window, in Command section, paste:\n\n"
txt += "'! _-RunPythonScript {}'".format(path)

instructions = txt
