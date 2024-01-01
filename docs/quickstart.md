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
### Writing our application
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

### Running our application
```console
% python pillar_sample_app.py
[23:54:32][ERROR]: Is anyone there? TT_TT

% python pillar_sample_app.py Nick
[23:56:44][INFO]: Hello Nick. It's quite lonely in here isn't it?

% python pillar_sample_app.py Nick Fred
[23:57:10][INFO]: Hello Nick and Fred.

% python pillar_sample_app.py Nick Fred James
[23:57:37][INFO]: Hello Nick, Fred, and James

% python pillar_sample_app.py Nick Fred James Alice Bob Malory
[23:58:18][CRITICAL]: Sorry but there are too many of you 0_0
```

### Viewing help / usage and version information
```console
% python pillar_sample_app.py --help
usage: pillar_sample_app.py [-h] [-c CONFIG_PATH] [-v] [--log-dir PATH] [--version] [NAME ...]

This is a sample application to show off Pillar.

The class docstring will be used as the description of the program it it is set.

positional arguments:
  NAME                  Name(s) to say hello to.

options:
  -h, --help            show this help message and exit
  -c CONFIG_PATH, --config CONFIG_PATH
                        Add a config file to parse. Config files are parsed in the order they are
                        added with values being merged into the previously parsed config.
  -v, --verbose         Increase logging verbosity
  --log-dir PATH        Set where log files should be stored. Defaults to /var/tmp
  --version             show program's version number and exit

Copyright (c) The Pillar Authors

% python pillar_sample_app.py --version
1.2.3
```

### Increasing logging verbosity
To view the logs we can use the `--verbose` argument multiple times, or use the shortened form `-v`.

```console
% python pillar_sample_app.py -v Nick Fred James Alice Bob Malory
[23:59:36][DEBUG]: There are 6
[23:59:36][CRITICAL]: Sorry but there are too many of you 0_0

% python pillar_sample_app.py -vvv Nick Fred James Alice Bob Malory
[23:59:57][DEBUG]: There are 6
[23:59:57][VDEBUG]: Our config is {'too_many_names': 5}
[23:59:57][CRITICAL]: Sorry but there are too many of you 0_0
```

### Using a config file
We know that we have a default config with a `too_many_names` set to `5`. Let's write our own config file to increase. By default Pillar supports JSON and YAML config files.

```yaml title="pillar_sample_config.yaml"
too_many_names: 10
```

Let's call our program again with the new config file.

```console
% python pillar_sample_app.py -c pillar_sample_config.yaml -vv Nick Fred James Alice Bob Malory
[00:02:36][DEBUG]: There are 6
[00:02:36][VDEBUG]: Our config is {'too_many_names': 10}
[00:02:36][INFO]: Hello Nick, Fred, James, Alice, Bob, and Malory
```

### Viewing the log files
All our output so far has been through the console. However Pillar will also have written logs to `/var/tmp`.

```console
% tail /var/tmp/pillar_sample_app.log
[20240101T235737+1100][2407242][pillar_sample_app][INFO]: Hello Nick, Fred, and James
[20240101T235818+1100][2407254][pillar_sample_app][CRITICAL]: Sorry but there are too many of you 0_0
[20240101T235936+1100][2407292][pillar_sample_app][DEBUG]: There are 6
[20240101T235936+1100][2407292][pillar_sample_app][CRITICAL]: Sorry but there are too many of you 0_0
[20240101T235957+1100][2407299][pillar_sample_app][DEBUG]: There are 6
[20240101T235957+1100][2407299][pillar_sample_app][VDEBUG]: Our config is {'too_many_names': 5}
[20240101T235957+1100][2407299][pillar_sample_app][CRITICAL]: Sorry but there are too many of you 0_0
[20240102T000236+1100][2407433][pillar_sample_app][DEBUG]: There are 6
[20240102T000236+1100][2407433][pillar_sample_app][VDEBUG]: Our config is {'too_many_names': 10}
[20240102T000236+1100][2407433][pillar_sample_app][INFO]: Hello Nick, Fred, James, Alice, Bob, and Malory
```

Pillar will also create a basic log file early during the setup process to capture any errors that occur before full logging is available. Let's check it too:

```console
% tail /var/tmp/pillar_sample_app.init.log
<should be empty>
```
