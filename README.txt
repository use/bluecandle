The data being analyzed here is a subset of ~1.2M runs from the datadump provided by Megacrit in I think 2019 or 2020.

It was loaded into mongodb for analysis.

Screenshots show some of the charts generated, and the data being viewed with mongodb Compass.

To get this up and running:

# Probably want to setup a local python env:
python3 -m venv .venv
source .venv/bin/activate

# install python modules
pip install -r requirements.txt

# launch jupyter
jupyter-lab

# now go to the link it shows you
# you should see the jupyter notebooks in your browser
