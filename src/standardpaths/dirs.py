import os
import sys
from pathlib import Path


class StandardPaths:

    # Look for XDG env vars on all platforms - if someone has gone to the
    # trouble to set them even on Windows or macOS, presumably they would like
    # them respected
    _xdg_data = os.getenv("XDG_DATA_HOME")
    _xdg_config = os.getenv("XDG_CONFIG_HOME")
    _xdg_state = os.getenv("XDG_STATE_HOME")
    _xdg_cache = os.getenv("XDG_CACHE_HOME")
    _xdg_runtime = os.getenv("XDG_RUNTIME_HOME")
    _xdg_data_dirs = os.getenv("XDG_DATA_DIRS")
    _xdg_config_dirs = os.getenv("XDG_CONFIG_DIRS")
    
    # Following https://specifications.freedesktop.org/basedir-spec/latest/
    _xdg_default_data = "~/.local/share"
    _xdg_default_config = "~/.config"
    _xdg_default_state = "~/.local/state"
    _xdg_default_app = "~/.local/bin"
    _xdg_default_cache = "~/.cache"
    _xdg_default_runtime = f"/run/user/{os.getuid()}"
    _xdg_default_data_dirs = ["/usr/local/share/", "/usr/share/"]
    _xdg_default_config_dirs = ["/etc/xdg"]

    match sys.platform:
        case "win32":
            # Windows environment variables
            # See https://learn.microsoft.com/en-us/windows/deployment/usmt/usmt-recognized-environment-variables
            _win_app_data = os.getenv("CSIDL_APPDATA")
            _win_local_app_data = os.getenv("CSIDL_LOCAL_APPDATA")
            #_win_program_files = os.getenv("CSIDL_PROGRAM_FILES")
            _win_programs = os.getenv("CSIDL_PROGRAMS")
            _win_tmp = os.getenv("TEMP")

            _data = _xdg_data or _win_app_data or "~/AppData/Roaming"
            _local_data = _win_local_app_data or "~/AppData/Local"
            _config = _xdg_config or _local_data
            _state = _xdg_state or _local_data + "/State"
            _app = _win_programs or "~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
            _cache = _xdg_cache or  _local_data + "/cache"
            _runtime = _xdg_runtime or _win_tmp or _local_data + "/Temp"
            _data_dirs = (
                _xdg_data_dirs.split(";") if _xdg_data_dirs
                else ["C:/ProgramData"]
            )
            _config_dirs = (
                _xdg_config_dirs.split(";") if _xdg_config_dirs
                else ["C:/ProgramData"]
            )

        case "darwin":
            _data = _xdg_data or "~/Library/Application Support"
            _config = _xdg_config or "~/Library/Preferences"
            _state = _xdg_state or "~/Library/Preferences/State" # Should really be ~/Library/Preferences/<APPNAME>/State
            _app = "/Applications"
            _cache = _xdg_cache or "~/Library/Caches"
            _runtime = _xdg_runtime or "~/Library/Application Support"
            _data_dirs = (
                _xdg_data_dirs.split(":") if _xdg_data_dirs
                else ["/Library/Application Support"]
            )
            _config_dirs = (
                _xdg_config_dirs.split(":") if _xdg_config_dirs
                else []
            )

        case "ios":
            # On iOS, ~ (presumably) evaluates to within the app's sandbox
            # This is fine as it aligns with QStandardPaths and platformdirs
            _data = _xdg_data or "~/Library/Application Support"
            _config = _xdg_config or "~/Library/Preferences"
            _state = _xdg_state or "~/Library/Preferences/State"  # Mirror macOS
            _app = _xdg_default_app  # This should maybe be unsupported on mobile
            _cache = _xdg_cache or "~/Library/Caches"
            _runtime = _xdg_runtime or "~/Library/Caches"  # With QStandardPaths this is unsupported
            _data_dirs = (
                _xdg_data_dirs.split(":") if _xdg_data_dirs
                else []
            )
            _config_dirs = (
                _xdg_config_dirs.split(":") if _xdg_config_dirs
                else []
            )

        case "android":
            # On Android, ~ evaluates to within the app's sandbox
            # This is fine as it aligns with QStandardPaths and platformdirs
            _data = _xdg_data or "~/files"
            _config = _xdg_config or "~/files/settings"
            _state = _xdg_state or "~/files/state"
            _app = _xdg_default_app  # This should maybe be unsupported on mobile
            _cache = _xdg_cache or "~/cache"
            _runtime = _xdg_runtime or "~/cache"
            _data_dirs = (
                _xdg_data_dirs.split(":") if _xdg_data_dirs
                else []
            )
            _config_dirs = (
                _xdg_config_dirs.split(":") if _xdg_config_dirs
                else []
            )

        case "linux":
            _data = _xdg_data or _xdg_default_data
            _config = _xdg_config or _xdg_default_config
            _state = _xdg_state or _xdg_default_state
            _app = _xdg_default_app
            _cache = _xdg_cache or _xdg_default_cache
            _runtime = _xdg_runtime or _xdg_default_runtime
            _data_dirs = (
                _xdg_data_dirs.split(":") if _xdg_data_dirs
                else _xdg_default_data_dirs
            )
            _config_dirs = (
                _xdg_config_dirs.split(":") if _xdg_config_dirs
                else _xdg_config_dirs
            )

        case _:
            # Same as Linux for now
            _data = _xdg_data or _xdg_default_data
            _config = _xdg_config or _xdg_default_config
            _state = _xdg_state or _xdg_default_state
            _app = _xdg_default_app
            _cache = _xdg_cache or _xdg_default_cache
            _runtime = _xdg_runtime or _xdg_default_runtime
            _data_dirs = (
                _xdg_data_dirs.split(":") if _xdg_data_dirs
                else _xdg_default_data_dirs
            )
            _config_dirs = (
                _xdg_config_dirs.split(":") if _xdg_config_dirs
                else _xdg_config_dirs
            )

    @classmethod
    def home(cls):
        return Path.home()
    
    @classmethod
    def data(cls, local=False):
        if local and sys.platform == "win32":
            if isinstance(cls._local_data, str):
                cls._local_data = Path(cls._local_data).expanduser()
            return cls._local_data
        else:
            if isinstance(cls._data, str):
                cls._data = Path(cls._data).expanduser()
            return cls._data
    
    @classmethod
    def config(cls):
        if isinstance(cls._config, str):
            cls._config = Path(cls._config).expanduser()
        return cls._config

    @classmethod
    def state(cls):
        if isinstance(cls._state, str):
            cls._state = Path(cls._state).expanduser()
        return cls._state

    @classmethod
    def app(cls):
        if isinstance(cls._app, str):
            cls._app = Path(cls._app).expanduser()
        return cls._app
    
    #@classmethod
    #def program_files(cls):
    #    if sys.platform == "win32":
    #        if isinstance(cls._win_program_files, str):
    #            cls._win_program_files = Path(cls._win_program_files).expanduser()
    #        return cls._win_program_files
    #    else:
    #        raise RuntimeError("Program Files exists only on Windows!")

    @classmethod
    def cache(cls):
        if isinstance(cls._cache, str):
            cls._cache = Path(cls._cache).expanduser()
        return cls._cache

    @classmethod
    def runtime(cls):
        if isinstance(cls._runtime, str):
            cls._runtime = Path(cls._runtime).expanduser()
        return cls._runtime

    @classmethod
    def data_dirs(cls, include_home=False, local=False):
        # Follow XDG spec and don't include user data home unless requested
        # Would be more convenient if `include_home=True` by default though...
        if cls._data_dirs and isinstance(cls._data_dirs[0], str):
            cls._data_dirs = [Path(p).expanduser() for p in cls._data_dirs]
        if include_home:
            return [cls.data(local=local)] + cls._data_dirs
        else:
            return cls._data_dirs

    @classmethod
    def config_dirs(cls, include_home=False):
        # Follow XDG spec and don't include user config home unless requested
        # Would be more convenient if `include_home=True` by default though...
        if cls._config_dirs and isinstance(cls._config_dirs[0], str):
            cls._config_dirs = [Path(p).expanduser() for p in cls._config_dirs]
        if include_home:
            return [cls.config()] + cls._config_dirs
        else:
            return cls._config_dirs

