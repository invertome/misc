#!/bin/bash
dependencies=("ged4py" "matplotlib")
environment_name="plotged"

conda create -y -n $environment_name
conda activate $environment_name
for package in "${dependencies[@]}"
do
    conda install -y $package -n $environment_name
done
