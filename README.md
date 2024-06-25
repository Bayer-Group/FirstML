# FirstML

Transform your Jupyter notebooks into a pipeline of nodebooks.

## Content

- [Installation](#installation)
- [Usage](#usage)


## Installation

### From GitHub (directly)

Run the following command:

```shell
pip install git+https://{token}@github.com/bayer-int/firstml.git
```

### From Local File System

Clone this GitHub repository:

```shell
git clone https://github.com/bayer-int/firstml.git
```

Move into the project directory:

```shell
cd firstml
```

Run the following command:

```shell
pip install .
```

### Trouble Shooting

The package `pygraphviz` (a requirement for `networkx`) can cause problems.
The following action(s) should solve these problems:

**On Windows:**

- use `conda` to install `pygraphviz` and then run the `pip install` again,
- install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  and make sure that the `C++ build tools` are added to path.

**On Linux (Ubuntu):**

Install `graphviz` using the following command:

```shell
sudo apt-get install graphviz
```

**On macOS:**

Install `graphviz` using the following command:

```shell
brew install graphviz
```


### Extra Requirements

You can install extra requirements by writing them in square brackets
(e.g., `pip install ".[io]"`).

Possible options:

- `io`: install connectors for `presto` and `snowflake`
- `dev`: install developer libraries to, e.g., execute unit tests

## Usage

Using this package, you can easily set up a pipeline consisting of Jupyter Notebooks
that can be executed using `SequentialRunner` and visualized using `GraphResolver`.

To do so, you first have to configure some parameters and define your pipeline.

### Global Parameters

You need to specify the following parameters
so that the script will run properly in your environment.

| name          | key             | description                                                                                         | example                                                                  |
|---------------|-----------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| BASE_URL      | "base_url"      | url to open notebooks                                                                               | "http://localhost:8888/lab/tree/"" |
| BASE_PATH     | "base_path"     | full path to home folder of jupyterlab                                                              | "/home/dev_usr_folder/"                                                  |
| DATA_HOME     | "data_home"     | relative path to the folder where to store data outputs, nodebook runs, etc.                        | "workspace/test/firstml-example/data"                                    |
| NODEBOOK_PATH | "nodebook_path" | relative path to the folder where the nodebooks are stored (nodebooks can be up to one level lower) | "workspace/test/firstml-example/nodebooks"                               |
| DEV_USR       | "dev_usr"       | name of current user, is retrieved automatically, you can force the named here                      | "YOUR_ID"                                                              |

You can easily set them by running the following code in python:

```python
from firstml.parameters import create_parameters
PARAMETERS = create_parameters(
  "{BASE_URL}", "{BASE_PATH}", "{DATA_HOME}", "{NODEBOOK_PATH}"
)
```

### Catalog

The catalog contains the mapping between easy to read/write identifiers
and their full / correct values (mostly paths to certain input and output files).

The catalog is constructed as dictionary using the identifier as key
and the correct value as value (see the following example):

```python
CATALOG = {
    "example_id": {
        "endpoint": "example_value"
    },
    "another_id": {
        "endpoint": "another_value"
    }
}
```

### Pipeline

As last preparation, you need to define the pipeline.
To do so, you create another dictionary as shown and explained in the following:

```python
PIPELINE = {
    "layer": "layer",
    "nodebooks": [
        {
            "nodebook_id": "nodebook_id",
            "nodebook_id_suffix": "nodebook_id_suffix",
            "type": "custom",
            "inputs": ["example_id"],
            "outputs": ["another_id"],
            "params": {
                "some_param": "a_value"
            },
        }
    ]
}
```

| key/value          | description                                                                                                                         |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| layer              | the type of the nodebook that is loaded; is reflected in the nodebook path (see below)                                              |
| notebook_id        | the name of the nodebook that is loaded; is reflected in the nodebook path (see below)                                              |
| notebook_id_suffix | the suffix assigned to the nodebook after processing (useful if you run the same nodebook with different input/output/param values) |
| inputs             | a list of input parameters for the nodebook; here you use the identifiers defined in the catalog                                    |
| outputs            | a list of output parameters for the nodebook; here you use the identifiers defined in the catalog                                   |
| params             | additional parameters you want to pass to the nodebook as key-value-arguments                                                       |

The path of the nodebook loaded for each step results from
`{BASE_PATH/{NODEBOOK_PATH}/{layer}/{nodebook_id}.ipynb`.

A pipeline can consist of multiple layers with each multiple nodebooks.

- To add a nodebook to a layer, you can another nodebook description under `nodebooks`.
- To add another layer to the pipeline, you can create a second pipeline as shown above
and then merge them as shown below:

```python
PIPELINE = {"pipelines": [LAYER_1, LAYER_2]}
```

**Important**: Always define an input and output parameter,
even if you just use a dummy value (which you have defined in the catalog).
The script is resolving the execution by looking at these values
and will ignore steps which do not have them.

### Sequential Runner

You can now execute the pipeline by running the following code:

```python
from firstml.runner.sequential_runner import SequentialRunner

PROJECT_NAME = "firstml-example"
seq = SequentialRunner()
seq.run(PROJECT_NAME, PIPELINE, PARAMETERS, CATALOG)
```

It will create an execution plan and then executes the nodebooks using the parameters.

The executed nodebooks can be found at
`{BASE_PATH}/{DATA_HOME}/nodebook_runs/{DEV_USR}/{TIME_STAMP}/{PROJECT_NAME}/`.

**Important**: You have to install all dependencies required for you nodebooks
before executing them using this script.

### GraphResolver

You can also visualize the execution plan by running the following code:

```python
from firstml.graph.graph_resolver import GraphResolver

gr_res = GraphResolver()
gr_res.viz_graph(PIPELINE)
```

### Testing a pipeline

Once you setup the parameters in test_firstml_pipeline.py you can run and visualise the test pipeline with the following command:

```shell
cd test
python -m unittest test_firstml_pipeline.py
```
