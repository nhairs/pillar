### IMPORTS
### ============================================================================
## Installed
from pillar.application import Application


### CLASSES
### ============================================================================
class LogApplication(Application):
    """A sample application showcasing Pillar's logging functionality."""

    def main(self):
        self.vvdebug("This is a very verbose debug message")
        self.vdebug("This is a verbose debug message")
        self.debug("This is a debug message")
        self.info("This is an info message")
        self.warning("This is a warning message")
        self.error("This is an error message")
        self.critical("This is a critical message")
        try:
            raise ValueError("Whoops!")
        except ValueError:
            self.info("This is a message with a stack trace", exc_info=True)
        return 0


### MAIN
### ============================================================================
if __name__ == "__main__":
    app = LogApplication()
    app.run()
