from typing import Any

from dagster import In, Nothing, Out
from qdk.base import BaseComponent


class BaseLoader(BaseComponent):
    compute_function = "load"
    tags = {
        "kind": "loader",
    }
    input_defs = {"after": In(Nothing)}
    output_defs = {"out": Out(Any)}

    @classmethod
    def load(cls) -> Any:
        """
        Overwrite this function to load the required object.
        """
        raise NotImplementedError(
            'Make sure you added a "load" function to the component'
        )
