# pylint: disable=missing-function-docstring
### IMPORTS
### ============================================================================
## Standard Library
import json
from pathlib import Path
from typing import Type

## Installed
import pytest
import yaml

## Application
from pillar.config import ConfigLoader

### SETUP
### ============================================================================
CONFIG_DIR = Path(__file__).parent / "configs"


### TESTS
### ============================================================================
def test_config_loader_deepcopy_default():
    default_config = {"a": "a", "b": [1, 2, 3]}
    loader = ConfigLoader(default_config=default_config)

    assert loader.config is not default_config
    assert loader.config == default_config

    # Check list is also copied
    assert loader.config["b"] is not default_config["b"]
    assert loader.config["b"] == default_config["b"]

    # Be paranoid and check updated values
    loader.config["a"] = "foo"
    assert loader.config["a"] == "foo"
    assert default_config["a"] == "a"

    loader.config["c"] = "c"
    assert loader.config["c"] == "c"
    assert "c" not in default_config
    return


@pytest.mark.parametrize("extension", ["json", "yaml", "yml"])
def test_config_loader(extension: str):
    loader = ConfigLoader()
    config = loader.config

    # Load A
    loader.load_config(CONFIG_DIR / f"a.{extension}")
    assert config["a"] == "a"
    assert config["test"] == "a"

    # Load B
    loader.load_config(CONFIG_DIR / f"b.{extension}")
    assert config["a"] == "a"
    assert config["b"] == "b"
    assert config["test"] == ["b"]

    # Load C
    loader.load_config(CONFIG_DIR / f"c.{extension}")
    assert config["a"] == "a"
    assert config["b"] == "b"
    assert config["c"] == "c"
    assert config["test"] == [1, 2, 3]

    return


@pytest.mark.parametrize(
    "extension,error",
    [
        ("json", json.JSONDecodeError),
        ("yaml", yaml.parser.ParserError),
        ("yml", yaml.parser.ParserError),
    ],
)
def test_config_loader_malformed(extension: str, error: Type[Exception]):
    path = str(CONFIG_DIR / f"malformed.{extension}")
    default_config = {"a": "a"}

    loader = ConfigLoader(default_config=default_config)
    with pytest.raises(error):
        loader.load_config(path)

    assert loader.config == default_config
    assert isinstance(loader.load_errors[path]["exception"], error)

    ## Reset and test with supression
    loader = ConfigLoader(default_config=default_config)
    loader.load_config(path, suppress_errors=True)

    assert loader.config == default_config
    assert isinstance(loader.load_errors[path]["exception"], error)

    return
