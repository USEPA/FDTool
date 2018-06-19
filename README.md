#### README: Algorithm to mine for functional dependencies and keys

##### Description: 
FDTool is a Python command-line application that mines functional dependencies and
candidate keys from datasets read in from .csv, .txt, and .pkl files.

##### Dependencies:

  1. [Python2](https://www.python.org/) (version 2.7.8 or later recommended)

  2. [Pandas](https://pandas.pydata.org/)

##### Build setup:
```
$ git clone https://github.com/USEPA/FDTool.git
$ cd FDTool
$ python setup.py install
```

##### Run Application:
```	
$ python fdtool /path/to/file
```

##### Output:
![output](images/sampleOutput.PNG)

##### Notes:
Module ```REPO/fdtool/modules/dbschema``` released under C-FSL license 
and copyright held by Elmar Stellnberger.





