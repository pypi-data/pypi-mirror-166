from typing import Dict, Union

import dask.dataframe as dd
import pandas as pd
from dagster import Any, In, Out
from qdk.base import BaseComponent


class BaseInference(BaseComponent):
    compute_function = "predict"
    tags = {
        "kind": "inference",
    }
    input_defs = {"data": In(pd.DataFrame), "model": In(Any)}
    output_defs = {"predictions": Out(pd.DataFrame)}

    @classmethod
    def predict(
        cls,
        df: Union[pd.DataFrame, dd.DataFrame],
        model: Any,
    ):
        raise NotImplementedError(
            'Make sure you added a "predict" function to the component'
        )
