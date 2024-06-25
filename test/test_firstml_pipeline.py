from unittest import TestCase

from firstml.parameters import create_parameters
from firstml.graph.graph_resolver import GraphResolver
from firstml.runner.sequential_runner import SequentialRunner


PROJECT_NAME = "firstml_test"

BASE_URL = "http://localhost:8888/lab/tree/"
BASE_PATH = "/full/path/to/workspace/"
DATA_HOME = "data"
NODEBOOK_PATH = "nodebooks"

PARAMETERS = create_parameters(BASE_URL, BASE_PATH, DATA_HOME, NODEBOOK_PATH)
DEV_USR = PARAMETERS["dev_usr"]

DATA_PATH = BASE_PATH + DATA_HOME

CATALOG = {
    "iris_raw": {
        "endpoint": f"{DATA_PATH}/data_source.csv",
    },
    "iris_cleaned": {
        "endpoint": f"{DATA_PATH}/cleaned_data.csv",
    },
    "model_petals": {
        "endpoint": f"{DATA_PATH}/model_petals.txt",
    },
    "model_sepals": {
        "endpoint": f"{DATA_PATH}/model_sepals.txt",
    }
}

# TODO: rename pipelines to pipeline
PIPE_LOAD = {
    "layer": "base",
    "nodebooks": [
        {
            "nodebook_id": "load",
            "nodebook_id_suffix": "iris_dataset",
            "type": "custom",
            "inputs": ["iris_raw"],
            "outputs": ["iris_cleaned"],
            "params": {},
        }
    ],
}

PIPE_MODEL = {
    "layer": "base",
    "nodebooks": [
        {
            "nodebook_id": "model",
            "nodebook_id_suffix": "iris_dataset_petals",
            "type": "custom",
            "inputs": ["iris_cleaned"],
            "outputs": ["model_petals"],
            "params": {"select_cols": ["PetalLengthCm", "PetalWidthCm", "Species"]},
        },
        {
            "nodebook_id": "model",
            "nodebook_id_suffix": "iris_dataset_sepals",
            "type": "custom",
            "inputs": ["iris_cleaned"],
            "outputs": ["model_sepals"],
            "params": {"select_cols": ["SepalLengthCm", "SepalWidthCm", "Species"]},
        }
    ],
}

PIPELINE = {"pipelines": [PIPE_LOAD, PIPE_MODEL]}


class TestFirstMLPipeline(TestCase):
    def test_run(self):
        seq = SequentialRunner()
        seq.run(PROJECT_NAME, PIPELINE, PARAMETERS, CATALOG)

    def test_vis_graph(self):
        gr_res = GraphResolver()
        gr_res.viz_graph(PIPELINE)
