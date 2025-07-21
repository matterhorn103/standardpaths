# standardpaths
Platform-appropriate paths with a simple API.

When working in Python it is commonly useful to store and later retrieve configuration files and miscellaneous user data.
Where such data should be stored, however, varies by operating system.

`standardpaths` provides an easy way to make sure your code is using best-practice locations appropriate for the operating system of the user.

The [`pathlib`](https://docs.python.org/3/library/pathlib.html) module of the Python standard library provides `Path` classes that use the semantics appropriate for the operating system, which also makes it a lot easier to write cross-platform Python code.
`standardpaths` and `pathlib` work hand-in-hand.

`standardpaths` is kept small and focused, with a view to potential Python stdlib integration.

## Why use standardpaths?

Key differentiators from the also excellent `platformdirs`:

- Uses `pathlib.Path` objects exclusively
- Simpler API
- Only a small core set of the most useful paths
- Only one way to do things
- Focuses on user data
- Cross-platform compatibility with the XDG specification

## Usage

### Basics

Basic usage is simple and mirrors the pattern of `Path.home()`:

```python
>>> from standardpaths import StandardPaths
>>> # On Linux
>>> StandardPaths.config()
PosixPath('/home/monty/.config')
>>> # On Windows
>>> StandardPaths.config()
WindowsPath('c:/Users/Monty/AppData/Local')
>>> # On macOS
>>> StandardPaths.config()
PosixPath('/home/monty/Library/Preferences')
```

Sometimes it is useful to access the general locations in this way, but applications should save user data pertaining to the application within application subdirectories rather than at the top level.
This is also done slightly differently between platforms though, so for convenience `standardpaths` also handles this for you:

```python
>>> # On Linux
>>> StandardPaths.state(app_name="my_app")
PosixPath('/home/monty/.local/state/my_app')
>>> # Alternatively
>>> StandardPaths.state("my_app")
PosixPath('/home/monty/.local/state/my_app')
>>> # On Windows
>>> StandardPaths.state("my_app")
WindowsPath('c:/Users/Monty/AppData/Local/my_app/State')
>>> # On macOS
>>> StandardPaths.state("my_app")
PosixPath('/home/monty/Library/Preferences/my_app/State')
```

If a nested structure is desired -- for author and name, for example -- simply pass a forward-slash-delineated string as you would to `Path` e.g.:

```python
>>> StandardPaths.config("spam/alot")
WindowsPath('c:/Users/Monty/AppData/Local/spam/alot')
```

The `StandardPaths` class provides platform-specific equivalents to all the paths specified in the [XDG base directory specification](https://specifications.freedesktop.org/basedir-spec/latest/):

```python
>>> StandardPaths.data()
PosixPath('/home/monty/.local/share')
>>> StandardPaths.config()
PosixPath('/home/monty/.config')
>>> StandardPaths.state()
PosixPath('/home/monty/.local/state')
>>> StandardPaths.app()
PosixPath('/home/monty/.local/bin')
>>> StandardPaths.cache()
PosixPath('/home/monty/.cache')
>>> StandardPaths.runtime()
PosixPath('/run/user/1000')
```

as well as the user's home directory for convenience:

```python
>>> StandardPaths.home()  # Alias for pathlib.Path.home()
PosixPath('/home/monty')
```

### Caching paths

While paths are always returned as `pathlib.Path` objects, they are stored within the class as strings initialized on import.
As a result, there is naturally a small overhead associated with the creation of a new `Path` object upon each class method call.

It may also be tedious to pass the same arguments over and over again, and consistently, in many different places.

The set of paths can be generated and cached for a given platform and app name by creating an instance of the `StandardPaths` class.
Any options for the class methods can be passed at the same time and will apply to all paths.

The generated paths are then accessed as instance attributes rather than via methods.

```python
>>> paths = StandardPaths("my_app", force_xdg=["darwin"], local=True)
>>> # On Linux
>>> paths.config
PosixPath('/home/monty/.config/my_app')
>>> paths.cache
PosixPath('/home/monty/.cache/my_app')
>>> paths.app
PosixPath('/home/monty/.local/bin')
```

Note that the paths are only evaluated and instantiated once -- at the time the `StandardPaths` instance is created -- and are never re-evaluated.

### Directory sets

Sets of additional directories that should be searched for data or config files, but that may not be writeable, are also provided as lists of `Path` objects ordered by priority; as an example of the output:

```python
>>> StandardPaths.data_dirs()
[PosixPath('/usr/local/share'), PosixPath('/usr/share')]
>>> StandardPaths.config_dirs()
[PosixPath('/home/monty/.config/kdedefaults'), PosixPath('/etc/xdg'), PosixPath('/usr/local/etc/xdg'), PosixPath('/usr/etc/xdg')]
```

The behaviour conforms to the XDG specification, meaning that they do *not* necessarily include the normal data or config directories.
To include them in the list with the highest priority, set the `include_home` flag to `True`:

```python
>>> StandardPaths.data()
PosixPath('/home/monty/.local/share')
>>> StandardPaths.data_dirs()
[PosixPath('/usr/local/share'), PosixPath('/usr/share')]
>>> StandardPaths.data_dirs(include_home=True)
[PosixPath('/home/monty/.local/share'), PosixPath('/usr/local/share'), PosixPath('/usr/share')]
```

### Handling of environment variables

Sensible default paths are used for each platform and can be found in the section below.

Where platform-specific environment variables are found, these take priority over the defaults e.g. `StandardPaths.data()` returns the value of `CSIDL_APPDATA` on Windows.

If the respective XDG environment variables (e.g. `$XDG_DATA_HOME`) are defined, these take priority over all other possibilities.
This is the case on all platforms -- even Windows -- with the philosophy that if they have been defined by a user, it is likely the user wants them used.

### Forcing the XDG standard

By default, `standardpaths` follows the native conventions for each platform.

For some users, this may not actually be preferable.
On macOS in particular, users often wish to store their user data according to the XDG standard rather than Apple's guidelines.

The use of the XDG default locations rather than the platform-specific ones can be enforced using the `force_xdg` argument; a `True` value causes them to be used for all systems, while passing a list of platform identifiers restricts the effect to those platforms:

```python
>>> # On Linux
>>> StandardPaths.config("my_app")
PosixPath('/home/monty/.config/my_app')
>>> # On Windows
>>> StandardPaths.config("my_app")
WindowsPath('c:/Users/Monty/AppData/Local/my_app')
>>> # On macOS
>>> StandardPaths.config("my_app")
PosixPath('/home/monty/Library/Preferences/my_app')
>>> # On Windows with XDG defaults forced for all platforms
>>> StandardPaths.config("my_app", force_xdg=True)
WindowsPath('c:/Users/Monty/.config/my_app')
>>> # On macOS with XDG defaults forced for macOS only
>>> StandardPaths.config("my_app", force_xdg=["darwin"])
PosixPath('/home/monty/.config/my_app')
```

Note however that `standardpaths` *always* follows the XDG specification in that, as discussed above, any set XDG environment variables are always deferred to in preference to anything else.

### "Local" vs "Roaming" profiles on Windows

Under Windows the `APPDATA` directory is separated into Local and Roaming profiles, depending on whether that data should be synchronized between machines or not when working in a domain environment.

For many of the locations, `StandardPaths` returns a path under the Local directory according to the Microsoft guidelines and/or by following the example of [`QStandardPaths`](https://doc.qt.io/qt-6/qstandardpaths.html):

```python
>>> StandardPaths.config("my_app")
WindowsPath('c:/Users/Monty/AppData/Local/my_app')
```

The default location for the data directory, on the other hand, is under the Roaming profile.
In this case, however, the location for local data can be requested using the appropriate flag:

```python
>>> StandardPaths.data("my_app")
WindowsPath('c:/Users/Monty/AppData/Roaming/my_app')
>>> StandardPaths.data("my_app", local=True)
WindowsPath('c:/Users/Monty/AppData/Local/my_app')
```

This parameter has no effect on other platforms.

## Paths

The default values for the paths (in the absence of defined XDG environment variables) are shown below:


| standardpaths              | Purpose                                                                                      | XDG variable      | Windows (`win32`)                                                                    | macOS (`darwin`)                     | Linux (`linux`)                        | iOS (`ios`)             | Android (`android`)     |
| -------------------------- | -------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------ | ------------------------------------ | -------------------------------------- | ----------------------- | ----------------------- |
| `data("spam")`             | user-specific data                                                                           | `XDG_DATA_HOME`   | `$CSIDL_APPDATA/spam`<br>or<br>`~/AppData/Roaming/spam`                              | `~/Library/Application Support/spam` | `~/.local/share/spam`                  | as macOS                | `~/files/spam`          |
| `data("spam", local=True)` | user-specific data (non-roaming)                                                             | N/A               | `$CSIDL_LOCAL_APPDATA/spam`<br>or<br>`~/AppData/Local/spam`                          | as above                             | as above                               | as macOS                | as above                |
| `config("spam")`           | user-specific configuration                                                                  | `XDG_CONFIG_HOME` | `$CSIDL_LOCAL_APPDATA/spam`<br>or<br>`~/AppData/Local/spam`                          | `~/Library/Preferences/spam`         | `~/.config/spam`                       | as macOS                | `~/files/settings/spam` |
| `state("spam")`            | user-specific state data                                                                     | `XDG_STATE_HOME`  | `$CSIDL_LOCAL_APPDATA/spam/State`<br>or<br>`~/AppData/Local/spam/State`              | `~/Library/Preferences/spam/State`   | `~/.local/state/spam`                  | as macOS                | `~/files/state/spam`    |
| `app()`                    | user-specific executable files                                                               |                   | `$CSIDL_PROGRAMS`<br>or<br>`~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs` | `/Applications`                      | `~/.local/bin`                         | `~/.local/bin`          | `~/.local/bin`c         |
| `cache("spam")`            | user-specific non-essential (cached) data                                                    | `XDG_CACHE_HOME`  | `$CSIDL_LOCAL_APPDATA/cache/spam`                                                    | `~/Library/Caches/spam`              | `~/.cache/spam`                        | as macOS                | `~/cache/spam`          |
| `runtime("spam")`          | user-specific runtime files and other file objects                                           | `XDG_RUNTIME_DIR` | `$TEMP`<br>or<br>`$CSIDL_LOCAL_APPDATA/Temp/spam`                                    | `~/Library/Application Support/spam` | `f"/run/user/{os.getuid()}/spam"`      | `~/Library/Caches/spam` | `~/cache/spam`          |
| `data_dirs()`              | preference ordered base directories relative to which data files should be searched          | `XDG_DATA_DIRS`   | `["C:/ProgramData"]`                                                                 | `["/Library/Application Support"]`   | `["/usr/local/share/", "/usr/share/"]` | `[]`                    | `[]`                    |
| `config_dirs()`            | preference ordered base directories relative to which configuration files should be searched | `XDG_CONFIG_DIRS` | `["C:/ProgramData"]`                                                                 | `[]`                                 | `["/etc/xdg"]`                         | `[]`                    | `[]`                    |

Other platforms default to the same as Linux.

## Comparison with other libraries

Approximate equivalents from other libraries are shown below.

| standardpaths | XDG env var       | platformdirs         | QStandardPaths        |
| ------------- | ----------------- | -------------------- | --------------------- |
| `home`        | (`HOME`)          |                      | HomeLocation          |
| `data`        | `XDG_DATA_HOME`   | `user_data_dir`*     | GenericDataLocation   |
| `config`      | `XDG_CONFIG_HOME` | `user_config_dir`*   | GenericConfigLocation |
| `state`       | `XDG_STATE_HOME`  |                      | StateLocation         |
| `app`         |                   |                      | ApplicationsLocation  |
| `cache`       | `XDG_CACHE_HOME`  | `user_cache_dir`*    | GenericCacheLocation  |
| `runtime`     | `XDG_RUNTIME_DIR` | `user_runtime_dir`   | RuntimeLocation       |
| `data_dirs`   | `XDG_DATA_DIRS`   | `site_data_dir`*     | GenericDataLocation   |
| `config_dirs` | `XDG_CONFIG_DIRS` | `site_config_dir`*   | GenericConfigLocation |
