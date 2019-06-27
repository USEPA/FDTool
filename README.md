#### README: Algorithm to mine for functional dependencies, equivalences and candidate keys

##### Description: 
FDTool is a Python command-line application that mines functional dependencies, equivalences and
candidate keys from datasets read in from .csv, .txt, and .pkl files.

##### Dependencies:

  1. [Python3](https://www.python.org/)

  2. [Pandas](https://pandas.pydata.org/); pip install pandas

##### Configuration:

Edit ```REPO\fdtool\config.py``` prior to building setup to
change preset time limit or max k-level. Include (optional) custom outfile
name after command to run application.

##### Build setup:
```
$ git clone https://github.com/USEPA/FDTool.git
$ cd FDTool
$ python setup.py install
```

##### Run Application:
```	
$ fdtool /path/to/file
```

##### Output:
![output](images/sampleOutput.PNG)

##### DOI Badge:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3245414.svg)](https://doi.org/10.5281/zenodo.3245414)

##### Notes:
Module ```REPO/fdtool/modules/dbschema``` released under C-FSL license 
and copyright held by Elmar Stellnberger.





