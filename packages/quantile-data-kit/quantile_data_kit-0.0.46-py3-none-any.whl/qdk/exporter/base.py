from typing import Union

import dask.dataframe as dd
import pandas as pd
from dagster import In, Nothing, Out
from qdk.base import BaseComponent
from qdk.dagster_types import DataFrameType


class BaseExporter(BaseComponent):
    compute_function = "export"
    tags = {
        "kind": "export",
    }
    input_defs = {"df": In(DataFrameType)}
    output_defs = {"after": Out(Nothing)}

    @classmethod
    def export(
        cls,
        df: Union[pd.DataFrame, dd.DataFrame],
        **config,
    ) -> None:
        raise NotImplementedError(
            'Make sure you added an "export" function to the component'
        )
