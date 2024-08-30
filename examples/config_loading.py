### IMPORTS
### ============================================================================
## Standard Library
import json

## Installed
from pillar.application import Application


### CLASSES
### ============================================================================
class ConfigApplication(Application):
    """A sample application showcing Pillar's config loading functionality."""

    config_required = True
    default_config = {"default": "yes"}

    def main(self):
        print(json.dumps(self.config))
        return 0


### MAIN
### ============================================================================
if __name__ == "__main__":
    app = ConfigApplication()
    app.run()
