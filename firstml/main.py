import getpass
import os
import sys

import pandas as pd

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firstml.graph.graph_resolver import GraphResolver
from firstml.runner.sequential_runner import SequentialRunner

seq = SequentialRunner()
gres = GraphResolver()

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

dev_usr = getpass.getuser()
