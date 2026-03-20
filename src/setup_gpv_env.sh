#!/bin/bash
# GPV Project — PyMC environment setup
# Run this once in your terminal, then use the 'gpv' kernel in Jupyter

conda create -n gpv python=3.12 -y

conda activate gpv

# Install numpy 1.x first — this is the key fix
conda install -c conda-forge "numpy<2" -y

# Install PyMC and dependencies via conda-forge (handles binary compatibility)
conda install -c conda-forge pymc arviz -y

# Install remaining project dependencies
conda install -c conda-forge pandas matplotlib jupyter ipykernel -y

# Register the kernel so it appears in Jupyter
python -m ipykernel install --user --name gpv --display-name "Python (gpv)"

echo "Done. Select 'Python (gpv)' as your kernel in Jupyter."
