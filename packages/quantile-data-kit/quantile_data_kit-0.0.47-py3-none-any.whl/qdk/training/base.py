from typing import Optional, Tuple, Union

import dask.dataframe as dd
import pandas as pd
from dagster import In, Nothing
from dagster import Optional as DagsterOptional
from dagster import Out
from qdk.base import BaseComponent
from qdk.dagster_types import DataFrameType, ModelType, SeriesType

from sklearn.base import BaseEstimator


class BaseTrainer(BaseComponent):
    compute_function = "train"
    tags = {
        "kind": "training",
    }
    input_defs = {
        "X": In(DataFrameType),
        "y": In(DataFrameType),
        "model": In(DagsterOptional[SeriesType]),
    }
    output_defs = {
        "model": Out(ModelType),
        "data": Out(DataFrameType, is_required=False),
    }

    @classmethod
    def train(
        cls,
        X: Union[pd.DataFrame, dd.DataFrame],
        model: Optional[BaseEstimator] = None,
        y: Optional[Union[pd.Series, dd.Series]] = None,
    ) -> Tuple[BaseEstimator, Optional[Union[pd.DataFrame, dd.DataFrame]]]:
        raise NotImplementedError(
            'Make sure you added a "train" function to the component'
        )
