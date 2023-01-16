#!/bin/bash
dependencies=("ged4py" "matplotlib")
environment_name="plotged"

mamba create -y -n $environment_name
mamba activate $environment_name
for package in "${dependencies[@]}"
do
    mamba install -y $package -n $environment_name
done
