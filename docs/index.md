# Pillar: Building Blocks for Python Applications

[![PyPi](https://img.shields.io/pypi/v/pillar.svg)](https://pypi.python.org/pypi/pillar/)
[![PyPI - Status](https://img.shields.io/pypi/status/pillar)](https://pypi.python.org/pypi/pillar/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pillar.svg)](https://github.com/nhairs/pillar)
[![License](https://img.shields.io/github/license/nhairs/pillar.svg)](https://github.com/nhairs/pillar)

## Introduction
Pillar provides resusable components for building command-line applications. No more copy-pasting boilerplate for `logging` or `argparse` just to get bare-bone features.

In particular Pillar focusses on providing components for applications that are run as services, background tasks, or scheduled jobs (e.g. cron jobs).

!!! warning "Pillar is currently Alpha software and does not have complete documentation, testing, or implementation of certain features."


### Features

- **Config Loading:** Automatically collect, parse, and merge config files provided as arguments.
- **Logging:** Preconfigured console and file logging.
  - Includes bare-bones logger for when applications are initialising.
- **Modular:** Many components are modular so you can re-use them in your applications without being forced to used all of Pillar.
- **Development:** fully typed for your static analysis / linting needs

### Why use Pillar over [Click](https://github.com/pallets/click), [Fire](https://github.com/google/python-fire), [Typer](https://github.com/tiangolo/typer-cli), or [Cement](https://github.com/datafolklabs/cement)?
Tools like Click, Fire, and Typer are focussed on CLI interfaces and how to get the command-line arguments to the code that runs them. Whilst Pillar can be used for extensive CLIs, it is better suited to single purpose applications like cron jobs. That's not to say that it doesn't support command-line arguments, as it still uses and exposes `argparse` for you to add your own.

Frameworks like Cement are powerful, but leads to a lot of boilerplate when creating lots of small applications. In contrast Pillar provides most of it's core functionality through a single class that your application subclasses from. You are able to customise and plug-and-play many components, but components are also fairly opinioated so that you don't have to remeber to customise them every time.

## Quick Start

Follow our [Quickstart Guide](quickstart.md).

```python title="tldr.py"
from pillar.application import Application

class MyApplication(Application):
    "Hello World application that prints basic info then exits"

    def main(self):
        self.info(f"hello world! My name is {self.name}")
        self.debug(f"My config is: {self.config}")
        return

if __name__ == "__main__":
    app = MyApplication()
    app.run()
```


## Bugs, Feature Requests etc
Please [submit an issue on github](https://github.com/nhairs/pillar/issues).

In the case of bug reports, please help us help you by following best practices [^1^](https://marker.io/blog/write-bug-report/) [^2^](https://www.chiark.greenend.org.uk/~sgtatham/bugs.html).

In the case of feature requests, please provide background to the problem you are trying to solve so to help find a solution that makes the most sense for the library as well as your usecase.

## Contributing
I am still working through open source licencing and contributing, so not taking PRs at this point in time. Instead raise and issue and I'll try get to it as soon a feasible.

## Licence
This project is licenced under the MIT Licence - see [`LICENCE`](https://github.com/nhairs/pillar/blob/main/LICENCE).

This project includes other open source licenced software - see [`NOTICE`](https://github.com/nhairs/pillar/blob/main/NOTICE).

## Authors
A project by Nicholas Hairs - [www.nicholashairs.com](https://www.nicholashairs.com).
