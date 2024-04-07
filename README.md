# AI-eXtended Design (AIXD): Grasshopper plugin

Grasshopper plugin for the AIXD toolkit.

## Installation

#### Requirements:

- Python >= 3.9
- compas > 2.0
- flask

#### Latest stable version
Install `aixd_grasshopper` using `pip`
```
pip install aixd_grasshopper
```

Install `aixd_grasshopper` using `conda`:
```
conda install -c conda-forge aixd_grasshopper
```

**Note**: It is recommended to use virtual environments to manage the dependencies of your projects. If you are using 
`conda`, you can create a new environment with `conda create -n myproject python=3.9` and then activate it with
`conda activate myproject` before installing `aixd_grasshopper`.

#### Latest unstable version

Install the latest version using `pip` from the git repository:
```
pip install --upgrade git+https://github.com/gramaziokohler/aixd_grasshopper.git
```

## Development

If you are going to develop on this repository, perform an installation from source:

```
git clone https://github.com/gramaziokohler/aixd_grasshopper.git
cd aixd_grasshopper
```

Then, install using conda, to install all the dependencies into a new environment called `aixd_gh`:
```
conda env create -f environment.yml
```

Or using pip:
```
pip install -e ".[dev]"
```

Finally, build Grasshopper components and install on Rhino/GH:

```
invoke build-ghuser-components
python -m compas_rhino.install -v 7.0
```

For more details on how the process of building components work, refer to [this docs](https://github.com/compas-dev/compas-actions.ghpython_components).

Check the [contribution guidelines](CONTRIBUTING.md) for more details.

## Folders and structure

The structure we follow on the current repo is as follows:

* `src` : for all source code.
    * `src/aixd_grasshopper` : source code of `aixd_grasshopper` plugin.
    * `src/aixd_grasshopper/components` : source code of the GH components.
    * `src/aixd_grasshopper/ghuser_manual` : binary components, pre-built.
    * `src/compas_aixd` : source code of the connector to COMPAS infrastructure.
