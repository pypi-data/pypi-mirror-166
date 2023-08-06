# Quantile Data Kit 🔍

## Publish to pypi
How to deploy a new version of the QDK?
1) Update the package version in `setup.py`.
2) Run the Makefile `make publish`

## Components
There are four types of base components in the QDK. 
1) `LoadComponent`. Takes nothing as input and outputs a DataFrame.
2) `TransformComponent`. Takes a DataFrame as input and outputs a DataFrame.
3) `TrainingComponent`. Takes data and a model as input and outputs a trained model.
4) `InferenceComponent`. Takes data and a model as input and ouputs prediction data.

## Adding a new component?
Adding a new component to the QDK requires the following steps:
1) **Type of component:** Decide which type of the four components above you are adding. 
2) **Add component:** Once you decide which type of component you are adding, add in the corresponding folder (e.g. `qdk/loader`) a new Python file that inherits from the parent component. In this file you can optionally overwrite `input_defs`, `output_defs` and `config_schema`. When adding a new component, you are required to add a classmethod with the same name as the `compute_function` attribute on the parent class. The keys in the `config_schema` are injected into the parameters of the compute function. Lastly, you need to import the new component to `qdk/__init__.py`. This allows you to import it from top-level.
4) **Write tests**: To continuously check the robustness of the components, we highly encourage you to add tests using `pytest`. The tests can be added at `qdk/tests`. Reminder to prefix the folder, files and functions with `test_`. One is able to test the components using either VScode testing or the terminal (e.g. with `pytest -s qdk/tests/test_loaders`).
