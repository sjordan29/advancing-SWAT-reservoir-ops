This folder contains reservoir files for models run with (a) coordinated release policies and (b) existing target storage reservoir operations. Each folder includes a `prep_swat.py` file that converts Borg output to the necessary format to run the SWAT model with optimized reservoir releases. 

The `ScriptsAssets` folder contains scripts used to calculate objectives. These go in the same folder as all of the SWAT files, and were used for both coordinated release policies and target storage releases.

Any code that references a folder called `SWATfiles` (e.g., as referenced by scripts in the `Optimization` or `omoScenarios` folders in the repo root direcotry) contained these assets (for the relevant resevoir policy type), along with the rest of the SWAT model files. 

For all SWAT model files, please contact Sarah Jordan at smjordan329@gmail.com. 


