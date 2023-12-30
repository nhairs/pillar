# pylint: disable=missing-function-docstring
### IMPORTS
### ============================================================================
## Standard Library
import sys

## Installed

## Application
from pillar.logging import logging_file_handler_errors_kwargs


### TESTS
### ============================================================================
def test_logging_file_handler_errors_kwargs():
    kwargs = logging_file_handler_errors_kwargs("TEST")
    if sys.version_info >= (3, 9):
        assert kwargs == {"errors": "TEST"}
    else:
        assert kwargs == {}  # pylint: disable=use-implicit-booleaness-not-comparison
    return
