# pylint: disable=missing-function-docstring
### IMPORTS
### ============================================================================
## Standard Library
import sys

## Installed

## Application
from pillar.dataclass import dataclass_slots_kwargs


### TESTS
### ============================================================================
def test_dataclass_slots_kwargs():
    kwargs = dataclass_slots_kwargs()
    if sys.version_info >= (3, 10):
        assert kwargs == {"slots": True}
    else:
        assert kwargs == {}  # pylint: disable=use-implicit-booleaness-not-comparison
    return
