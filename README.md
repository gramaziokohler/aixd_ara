# ARA: AIXD Grasshopper plugin

Grasshopper plugin for the AIXD toolkit.

## Installation

#### Requirements:

- Python >= 3.9
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

Install the plugin in Rhino/GH using the following command:
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
    * `src/aixd_ara` : source code of `aixd_ara` plugin.
    * `src/aixd_ara/components` : source code of the GH components.
    * `src/aixd_ara/ghuser_manual` : binary components, pre-built.
    * `src/compas_aixd` : source code of the connector to COMPAS infrastructure.
