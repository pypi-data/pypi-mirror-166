# GS1 Library wrapper

[![Documentation Status](https://readthedocs.org/projects/gs1-barcode-engine-python-wrapper/badge/?version=latest)](https://gs1-barcode-engine-python-wrapper.readthedocs.io/en/latest/?badge=latest)

A Python wrapper of https://github.com/gs1/gs1-barcode-engine.

Docs: https://gs1-barcode-engine-python-wrapper.readthedocs.io/en/latest/

Pypi: https://pypi.org/project/py-gs1-barcode-engine/

Source: https://bitbucket.org/stolmen/gs1-wrapper

TODO 
- expose a thin wrapper interface.

## Installation

`pip install py-gs1-barcode-engine`

## Example usage

```
import py_gs1_barcode_engine

INCHES_PER_MM = 0.0393701
dpi = 157.35
module_x_dim_mm = 7
module_x_dim_inches = module_x_dim_mm * INCHES_PER_MM

bmp_data = py_gs1_barcode_engine.generate_gs1_datamatrix(
    "(01)94210325403182(30)2(3922)0460(93)TQ",
    dm_rows=22,
    dm_cols=22,
    x_undercut=0,
    y_undercut=0,
    scaling={"resolution": dpi, "target_x_dim": module_x_dim_inches},
)

with open("barcode.bmp", "wb") as f:
    f.write(bmp_data)
        
```

## Running tests

```
pip install -r requirements.txt
python setup.py test
pytest
```


## Packaging

To package this project, run:
```
python -m build -s
```

To package and upload a new version of this, update the version numnber in setup.py, then run
```
./build_and_publish.sh
```

Note that only an sdist distribution is built and uploaded. No wheel is uploaded.

Output is copied into the `dist/` folder.

## License

Copyright (c) 2022 Tiliter Pty Ltd
Copyright (c) 2000-2021 GS1 AISBL

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this library except in compliance with the License.

You may obtain a copy of the License at:

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
