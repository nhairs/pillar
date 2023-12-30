# Quickstart

## Installation

### Install via pip

**Recommended**

The recommended install target will include libraries to support common usecases of Pillar. This includes a number of libraries that are **not** pure Python, and thus may have install requirements outside of `pip` - they are typically included as they provide more performant versions of standard libraries.

To install Pillar with recommended packages use:

```bash
pip3 install pillar[recommended]
```

**Minimal**

A minimal installation will only include libraries to perform core functionality. This can be useful if you are intending to only use parts of Pillar in another program without using the Pillar `Application`.

To perform a minimal install use:

```bash
pip3 install pillar
```

## Sample Application

```python title="pillar_sample_app.py"
import pillar.application

class MyApplication(pillar.application.Application):
    """This is a sample application to show off Pillar.

    The class docstring will be used as the description of the program it it is set.
    """

    # We can add an argparse epilog
    epilog = "Copyright (c) The Pillar Authors"

    # We can also add an argparse version
    version = "1.2.3"

    # Set a default config
    default_config = {"too_many_names": 5}

    # Customise the ArgumentParsrer
    def get_argument_parser(self):
        # First we generate the default one
        parser = super().get_argument_parser()

        # Now lets customise it
        parser.add_argument(
            "names",
            metavar="NAME",
            nargs="*",
            default=[],
            help="Name(s) to say hello to."
        )
        return parser

    def main(self):
        # We can access the parsed arguments with self.args
        self.debug(f"There are {len(self.args.names)}")

        # We can access the loaded config using self.config
        self.vdebug(f"Our config is {self.config}")

        # Let's write a silly little program

        if len(self.args.names) >= self.config["too_many_names"]:
            self.critical("Sorry but there are too many of you 0_0")
            # if main returns an integer it will be used for the
            # exit code of the program.
            return 1

        if len(self.args.names) == 0:
            self.error("Is anyone there? TT_TT")
            return 0

        if len(self.args.names) == 1:
            self.info(f"Hello {self.args.names[0]}. It's quite lonely in here isn't it?")
        elif len(self.args.names) == 2:
            self.info(f"Hello {self.args.names[0]} and {self.args.names[1]}.")
        else:
            self.info(f"Hello {', '.join(self.args.names[:-1])}, and {self.args.names[-1]}")

        return 0

if __name__ == "__main__":
    app = MyApplication()
    app.run()
```
