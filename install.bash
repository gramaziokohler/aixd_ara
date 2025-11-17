#!/usr/bin/env bash

if [[ $- != *i* ]]; then
    RHINO_VERSION=7
    printf "NOTE: Installation will default to Rhino 7\n"
    printf "To select a different Rhino version, run this script interactively:\n\n"
    printf "    curl -sO https://github.com/gramaziokohler/aixd_ara/raw/main/install.bash && bash -i install.bash\n\n"
else
    while true; do
        read -n 1 -p "Select Rhino version (7, 8, or Q to quit): " RHINO_VERSION
        printf "\n";
        case $RHINO_VERSION in
            7* ) break;;
            8* ) break;;
            [Qq]* ) exit;;
            * ) printf "Invalid Rhino version, please choose either 7 or 8.\n";;
        esac
    done
fi

CONDA_HOME=$HOME/miniconda
CONDA_BIN=$CONDA_HOME/condabin
CONDA_ENV_NAME=aixd_ara
ARCH=$(uname -m)

printf "[√] Starting ARA installation…\n"

printf "[ ] Checking conda…"

if ! command -V conda &> /dev/null
then
    printf "\r[x] Conda not found, we will install Miniconda\n"
	printf "[ ] Installing miniconda (Python distribution)…"
	# curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o ./miniconda.sh &> /dev/null
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-$ARCH.sh -o ./miniconda.sh &> /dev/null
	bash ./miniconda.sh -b -u -p $CONDA_HOME &> /dev/null
	printf "\r[√] Installing miniconda (Python distribution)…\n"

	printf "[ ] Configuring miniconda for first use…"
	$CONDA_BIN/conda init bash &> /dev/null
	source $HOME/.bash_profile &> /dev/null
	printf "\r[√] Configured miniconda for first use successfully\n"
else
	CONDA_HOME=$(dirname $(dirname $CONDA_EXE))
    printf "\r[√] Conda command found!\n"
fi

if { conda env list | grep $CONDA_ENV_NAME; } >/dev/null 2>&1; then
    printf "[√] Virtual environment already exists! ($CONDA_ENV_NAME)\n"
else
    printf "[√] Virtual environment not found, will create it now…\n"

    printf "[ ] Creating virtual environment…"
    conda create -c conda-forge -n $CONDA_ENV_NAME aixd aixd_ara compas flask python=3.9 -y &> /dev/null
    printf "\r[√] Created virtual environment '$CONDA_ENV_NAME' successfully\n"
fi

printf "[ ] Activating virtual environment…"
source $CONDA_HOME/bin/activate $CONDA_ENV_NAME
printf "\r[√] Activated virtual environment successfully\n"

printf "[√] Activating environment '$CONDA_ENV_NAME' for Rhino…\n"
python -m aixd_ara.rhino_install -v $RHINO_VERSION.0
printf "\r[√] Successfully installed ARA on Rhino\n"
