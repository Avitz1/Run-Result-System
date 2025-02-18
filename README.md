### Set-Up
1. Create a virtual environment
2. Install the requirements
3. Install sub-packages with `pip install -e .`
### CLI Usage
```bash
python cli/store_run_results.py --tool TOOL [ -f RESULT_FILE | --data DATA_JSON ]
```
* "innovus" run-results look like
```json
{
  "user": "obiwan",
  "project": "sped_00",
  "tag": "ff_kslow_2025_02_02_nostop_ready",
  "t_deviate": 0.3392,
  "path_type": "timing_seq0",
}
```
* "prime" run-results look like:
```json
{
	"user": "kenobi",
	"project": "falcon",
	"tag": "cred_opens-2.2-signal0872-",
	"aberrant_cells": ["/hier0/hier1/cell0", "/hier0/hier3/cell2"],
	"avg_aberration": 1.4892732007,
	"edge_focus": [0, 0, 1, 0]
}
```
### GUI Usage
```bash
python gui/app.py
```
In the GUI, click on a column header to sort the table by that column.

