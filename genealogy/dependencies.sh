#!/bin/bash
dependencies=("ged4py" "matplotlib")
environment_name="plotged"

mamba create -y -n $environment_name
mamba activate $environment_name
for package in "${dependencies[@]}"
do
    mamba install -y $package -n $environment_name
done
for package in "${dependencies[@]}"
do
    if conda list -n $environment_name | grep -q $package; then
        echo "$package is already installed."
    else
        echo "$package is not installed. Trying to install with pip..."
        pip install --user $package
    fi
done
