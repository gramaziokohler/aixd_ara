# ARA: Grasshopper plugin for AIXD toolbox for AI-eXtended Design

[![License](https://img.shields.io/github/license/gramaziokohler/aixd_ara.svg)](https://pypi.python.org/pypi/aixd_ara)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/aixd_ara)](https://anaconda.org/conda-forge/aixd_ara)
[![pip downloads](https://img.shields.io/pypi/dm/aixd_ara)](https://pypi.python.org/project/aixd_ara)
[![PyPI Package latest release](https://img.shields.io/pypi/v/aixd_ara.svg)](https://pypi.python.org/pypi/aixd_ara)
[![Anaconda](https://img.shields.io/conda/vn/conda-forge/aixd_ara.svg)](https://anaconda.org/conda-forge/aixd_ara)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14007759.svg)](https://doi.org/10.5281/zenodo.14007758)


**Grasshopper plugin for data-driven and inverse design methods with generative AI.**


**ARA** is a Grasshopper plugin that augments the design process with data-driven and inverse design approach by combining parametric models built in Grasshopper with generative AI models. It enables designers, architects and engineers to efficiently generate design solutions with the assistance of generative neural networks. The inverse design paradigm accelerates design exploration by providing many different design variants that match project objectives.

With **ARA**, you can easily generate a project-specific the dataset from an existing parametric model definition in Grasshopper, and then train and deploy a custom autoencoder model to generate designs that satisfy the requested target values, such as performance metrics or design constraints.

**ARA** also comes with various visualization tools for data analysis and performance evaluation.

**ARA** is open-source and builds on top of the [AIXD: AI-eXtended Design toolkit](https://gitlab.renkulab.io/ai-augmented-design/aixd).

## Getting started

To get started, please have a look at the 
[Easy Installation](https://gramaziokohler.github.io/aixd_ara/latest/installation.html), 
[Tutorial](https://gramaziokohler.github.io/aixd_ara/latest/tutorial.html), 
[Documentation](https://gramaziokohler.github.io/aixd_ara/latest/documentation.html) and 
[Examples](https://gramaziokohler.github.io/aixd_ara/latest/examples.html),
as well as our [paper](https://link.springer.com/chapter/10.1007/978-3-031-68275-9_19).



## Installation

#### Requirements:
- Python >= 3.9
- axid == 0.13.0
- compas > 2.0
- flask

#### Latest stable version

Install `aixd_ara` using `pip`
```bash
pip install aixd_ara
```

Install `aixd_ara` using `conda`:
```bash
conda install -c conda-forge aixd_ara
```

Install the plugin in Rhino/Grasshopper using the following command:
```bash
python -m compas_rhino.install -v 7.0
```

**Note**: It is recommended to use virtual environments to manage the dependencies of your projects. If you are using 
`conda`, you can create a new environment with `conda create -n myproject python=3.9` and then activate it with
`conda activate myproject` before installing `aixd_ara`.

#### Latest unstable version

Install the latest version using `pip` from the git repository:
```bash
pip install --upgrade git+https://github.com/gramaziokohler/aixd_ara.git
```

## Development

If you are going to develop on this repository, perform an installation from source:

```bash
git clone https://github.com/gramaziokohler/aixd_ara.git
cd aixd_ara
```

Then, use conda to install all the dependencies into a new environment called `aixd_ara`:
```bash
conda env create -f environment.yml
```

Or using pip:
```bash
pip install -e ".[dev]"
```

Finally, build Grasshopper components and install on Rhino/GH:

```bash
invoke build-ghuser-components
python -m compas_rhino.install -v 7.0
```

For more details on how the process of building components work, refer to [this docs](https://github.com/compas-dev/compas-actions.ghpython_components).

Check the [contribution guidelines](CONTRIBUTING.md) for more details.

## Folders and structure

The structure we follow on the current repo is as follows:

* `src` : for all source code.
    * `src/aixd_ara` : source code of the ARA plugin.
    * `src/aixd_ara/components` : source code of ARA's Grasshopper components.
    * `src/aixd_ara/scripts` : ARA scripts to run in Rhino's Python Editor.
    * `src/compas_aixd` : source code of the connector to COMPAS infrastructure.
* `examples` : example files.
* `scripts` : additional scipts.
* `docs` : documentation's source code.
