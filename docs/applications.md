# Writing Applications

The Pillar [`Application`][pillar.application.Application] class encapsulates common boilerplate when writing applications. Although they are configured to have many "sane" defaults or "automagic" detection of settings, they are fairly configurable.

Specifically Pillar applications handle the following tasks:

- Argument parsing and help info
- Configuration loading and parsing
- Standard logging outputs
  - Console logging
  - File logging
- Graceful handling of uncaught exceptions.

This makes Pillar applications a good base when writing services, background taks, scheduled (cron) jobs, or other similar programs. That said, Pillar applications are in no way limited to these types of programs, but if you are writing a heavily CLI driven program (like `git`) there are better alternatives.

## Writing your application

You write applications by subclassing `Application` and overriding class variables and methods as needed. For an example see [the quickstart sample application](quickstart.md#sample-application).

The only method that you must override is the [`main`][pillar.application.Application.main] method. This is where you should put the bulk of your program. You can set the exit/return code of your application by simply returning an `int` (note: it must be in the range of `0-255` inclusive). If your main method returns `None` this will be converted to a `0` (no error) return code.

Sometimes you may wish to modify the [`setup`][pillar.application.Application.setup] method to add your own setup steps. Whilst you can completely replace it, it is recommended that you that you call `super().setup()` first so that the default behaviour can run first.

A common reason for overriding `setup` rather than doing custom setup at the start of `main` is when you have multiple applications that should do the same basic setup. For example you might attach a custom logger that sends messages to the work chat. By using a shared based class you don't need to worry about subclasses remembering to call your custom setup in `main`.

```python
# Could be in the same package, or you might have your own
# organisation base package you import into all projects
class BaseApplication(Application):
    name = "my-app"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        # Custom setup
        return

class ProcessStuff(BaseApplication):
    application_name = "my-app"
    # ...

class ReportStuff(BaseApplication):
    application_name = "my-app-report"
    # ...
```

## Argument Parsing

Argument parsing is handled through the standard library [`argparse`](https://docs.python.org/3/library/argparse.html). Whilst there are more advanced packages available they are generally aimed at CLI heavy applications. For applications that are primarily customised through their config `argparse` should provide enough functionality.

To add your own arguments you will need to override the [`get_argument_parser`][pillar.application.Application.get_argument_parser] method. This should provide a ready to use `ArgumentParser`. In general you'll want to modify the default parser rather than creating one from scratch. To access it you should call the `super().get_argument_parser()` method first:

```python
class MyApplication(Application):
    def get_argument_parser(self):
        parser = super().get_argument_parser()
        # modify the parser
        return parser
```

When running you can access the parsed arguments through `self.args`.

### The Default Parser

Generation of the default `ArgumentParser` can be customised through certain class attributes on your application.

**Program Name** - This is used when generating the `usage: <application_name> <args>` displayed in the help text. By default Pillar will attempt to guess what this name is based on how the application has been called (e.g. `python yourscript.py`, `python -m your.package.app`). However this detection is pretty limited so is recommended that you set it via the `application_name` class attribute.

**Description** - This is used when generating the help text. It is collected and used verbatim from the docstring of your application class.

**Epilog** - This is displayed at end of the generated help text. It can be set through the `epilog` class attribute.

**Version** - Version information can be provided through the `version` class attribute. If set it will register a `--version` argument that will print the version and exit.

The default parser may also generate arguments for the following:

**Configuration Files** - [If enabled](#configuration-files) uses `-c`/`--config` and populates `self.args.config_paths`.

**Log directory** - If [file logging is enabled](#file-logging) uses `--log-dir` and populates `self.args.log_dir`.

```python
class MyApplication(Application):
    "This is my super awesome cli"

    application_name = "some-cli"
    epilog = "NO WARRANTY IS PROVIDED"
    version = "0.0.0@a97ef09"
```

## Configuration Files

In general Pillar applications are designed to be customised more through config files than they are commandline arguments. Configuration is loaded from two locations:

**Default Config** - The default config is set via the `default_config` class attribute. It is expected to be of type `Dict[str, Any]`.

If you are instantiating the application multiple times it is safe to use basic types including `dict` and `list` as these will be deep copied by the [config loader](#the-config-loader). It is **unsafe** to use custom classes as by default these are not copied (and thus will be shared by all instances of your application).

**Arguments** - Config files can be passed as individual files via `--config` or as a directory of files using `--config-dir` to the be loaded using the `ConfigLoader`. Config is first loaded from config directories with individual files being loaded in alphabetical/lexical order. Config is then loaded from individual files in the order they were provided.

This can be disabled by setting the `config_args_enabled` class attribute to `False`. Note: even if the config args are disabled the config loader will still be created (with the default config passed through).

By default providing config via the `--config` or `--config-dir` arguments is optional, however it can be made mandatory by setting the `config_required` attributes to `True`.

```python
class MyApplication(Application):
    config_required = True
    default_config = {
        "foo": 1,
        "bar": True,
    }
```

When running, the config is available via `self.config`.

### The Config Loader

The [`ConfigLoader`][pillar.config.ConfigLoader] class handles the loading, parsing, and merging of configuration files into a single config object.

Merging of configuration is will merge any dictionaries with any existing values from earlier calls being overriden by values set by later calls.

The config loader is available at `self.config_loader`. Strictly speaking `self.config` is just a reference to `dict` located at `self.config_loader.config`.

The config loader is exposed in case you want to customise how config files are loaded. For example you may wish to disable config files from arguments and instead load the config from a predetermined location.

```python
class MyDnsService(Application):
    "Custom DNS service"
    name = "super-dns"
    application_name = "dnsd"

    config_args_enabled = False
    default_config = {
        # ...
    }

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.config_loader.load_config("/etc/dnsd/config.yaml")
        return
```

The actual config loader used can be customised by setting the `config_loader_class` class attribute on your application.

## Logging

By default your application will log on it's name (`self.name`). Like `application_name` Pillar will attempt to guess this name if it is not provided. You can control this by setting the `name` class attribute.

Pillar applications use the [`LoggingMixin`][pillar.logging.LoggingMixin] which provides the following methods to log at the given level:

- `self.vvdebug` (very verbose debug)
- `self.vdebug` (verbose debug)
- `self.debug`
- `self.info`
- `self.warning`
- `self.error`
- `self.critical`

You'll notice two extra debug levels. These are defined in `pillar.logging` to allow for finer grained control over your debug messages.

### Customising Logging

Much of the default logging behaviour can be customised by setting the `logging_manifest` class attribute to your own instance of [`LoggingManifest`][pillar.application.LoggingManifest].

**Default level** - The default log level is `INFO` however this can be changed by setting the `default_level`. This default level will affect the logging level calculated from increasing the logging verbosity in the arguments. For example if the default level is `DEBUG` increasing the verbosity by one will increase it to `VDEBUG`. This is calculated using [`get_log_level`][pillar.logging.get_log_level].

**Logging additional names** - If you wish to log additional names (for example from another library) you can provide them through `additional_namespaces` on the logging manifest. These loggers will be attached to the console and file handler.

```python
class MyApplication(Application):
    logging_manifest = LoggingManifest(default_level=logging.WARNING)
```

### Console Logging

By default logs to `sys.stderr`.

For further options see the [`LoggingManifest`][pillar.application.LoggingManifest].

### File Logging

Log files will be generated at `/var/tmp/{name}.log`. This can be disabled by setting `file_enabled` to `False`.

To prevent accidentally filling of diskspace these logs are limited in size (`file_max_size`) and only a limited number are stored (`file_backup_count`).

For further options see the [`LoggingManifest`][pillar.application.LoggingManifest].

### Initial Logging

The initial logging is created as the first step during [`setup`][pillar.application.Application.setup]. This enables logging of errors encountered during argument parsing, config loading, and later logging setup.

In addition to logging to the console it also logs to a dedicated file located at `/var/tmp/{name}.init.log`.

For further options see the [`LoggingManifest`][pillar.application.LoggingManifest].

## Testing and Debugging Applications
!!! warning "Under Construction 🏗️"
