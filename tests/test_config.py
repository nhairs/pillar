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


## Test ConfigLoad.load_config
## -----------------------------------------------------------------------------
@pytest.mark.parametrize("extension", ["json", "yaml", "yml"])
def test_load_config(extension: str):
    loader = ConfigLoader()

    # Load A
    loader.load_config(CONFIG_DIR / f"a.{extension}")
    assert loader.config["a"] == "a"
    assert loader.config["test"] == "a"

    # Load B
    loader.load_config(CONFIG_DIR / f"b.{extension}")
    assert loader.config["a"] == "a"
    assert loader.config["b"] == "b"
    assert loader.config["test"] == ["b"]

    # Load C
    loader.load_config(CONFIG_DIR / f"c.{extension}")
    assert loader.config["a"] == "a"
    assert loader.config["b"] == "b"
    assert loader.config["c"] == "c"
    assert loader.config["test"] == [1, 2, 3]

    return


@pytest.mark.parametrize(
    "extension,error",
    [
        ("json", json.JSONDecodeError),
        ("yaml", yaml.parser.ParserError),
        ("yml", yaml.parser.ParserError),
    ],
)
def test_load_config_malformed(extension: str, error: Type[Exception]):
    path = str(CONFIG_DIR / f"malformed.{extension}")
    default_config = {"a": "a"}

    loader = ConfigLoader(default_config=default_config)
    with pytest.raises(error):
        loader.load_config(path)

    assert loader.config == default_config
    assert isinstance(loader.load_errors[path]["exception"], error)

    ## Reset and test with error supression
    loader = ConfigLoader(default_config=default_config)
    loader.load_config(path, suppress_errors=True)

    assert loader.config == default_config
    assert isinstance(loader.load_errors[path]["exception"], error)

    return


## Test ConfigLoader.load_config_directory
## -----------------------------------------------------------------------------
def test_load_config_directory():
    loader = ConfigLoader()
    dir_path = CONFIG_DIR / "dir-good"

    loader.load_config_directory(dir_path)

    assert loader.config["a"] == "a"
    assert loader.config["b"] == "b"
    assert loader.config["c"] == "c"
    assert loader.config["test"] == [1, 2, 3]

    for i in ["a.yml", "b.yml", "c.yml"]:
        assert str(dir_path / i) in loader.load_stack

    return


def test_load_config_directory_mixed():
    loader = ConfigLoader()
    dir_path = CONFIG_DIR / "dir-mixed"

    loader.load_config_directory(dir_path)

    assert loader.config["json"] is True
    assert loader.config["yaml"] is True
    assert loader.config["test"] == "yaml"

    for i in ["a.json", "a.yml"]:
        assert str(dir_path / i) in loader.load_stack

    for i in ["ignored", "another-dir", "another-dir/a.yml"]:
        assert str(dir_path / i) not in loader.load_stack
    return


def test_load_config_directory_malformed():
    loader = ConfigLoader()
    dir_path = CONFIG_DIR / "dir-malformed"
    malformed_path = str(dir_path / "malformed.yml")

    with pytest.raises(yaml.parser.ParserError):
        loader.load_config_directory(dir_path)

    assert loader.config["a"] == "a"
    assert loader.config["b"] == "b"
    assert loader.config["c"] == "c"
    assert loader.config["test"] == [1, 2, 3]

    for i in ["a.yml", "b.yml", "c.yml"]:
        assert str(dir_path / i) in loader.load_stack

    assert malformed_path not in loader.load_stack
    assert isinstance(loader.load_errors[malformed_path]["exception"], yaml.parser.ParserError)

    ## Reset and test with error supression
    loader = ConfigLoader()
    loader.load_config_directory(dir_path, suppress_errors=True)
    assert loader.config["a"] == "a"
    assert loader.config["b"] == "b"
    assert loader.config["c"] == "c"
    assert loader.config["test"] == [1, 2, 3]

    for i in ["a.yml", "b.yml", "c.yml"]:
        assert str(dir_path / i) in loader.load_stack

    assert malformed_path not in loader.load_stack
    assert isinstance(loader.load_errors[malformed_path]["exception"], yaml.parser.ParserError)
    return
