import os
import sys
from pathlib import Path


class StandardPaths:

    # Look for XDG env vars on all platforms - if someone has gone to the
    # trouble to set them on e.g. Windows, presumably they would like them
    # respected
    _xdg_data = os.getenv("XDG_DATA_HOME")
    _xdg_config = os.getenv("XDG_CONFIG_HOME")
    _xdg_state = os.getenv("XDG_STATE_HOME")
    _xdg_cache = os.getenv("XDG_CACHE_HOME")
    _xdg_runtime = os.getenv("XDG_RUNTIME_HOME")
    _xdg_data_dirs = os.getenv("XDG_DATA_DIRS")
    _xdg_config_dirs = os.getenv("XDG_CONFIG_DIRS")

    match sys.platform:
        case "win32":
            # Windows environment variables
            # See https://learn.microsoft.com/en-us/windows/deployment/usmt/usmt-recognized-environment-variables
            _win_app_data = os.getenv("CSIDL_APPDATA")
            _win_local_app_data = os.getenv("CSIDL_LOCAL_APPDATA")
            _win_program_files = os.getenv("CSIDL_PROGRAM_FILES")
            _win_programs = os.getenv("CSIDL_PROGRAMS")
            _win_tmp = os.getenv("TEMP")

            _data = _xdg_data or _win_app_data or _win_local_app_data or "~/AppData/Local"
            _config = _xdg_config or _win_local_app_data or _data
            _state = _xdg_state or _win_local_app_data + "/State" or _data + "/State"
            _app = _win_programs or "~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
            _cache = _xdg_cache or "~/AppData/Local/cache"
            _runtime = _xdg_runtime or 
            _data_dirs = _xdg_data_dirs.split(":") if _xdg_data_dirs else []
            _config_dirs = _xdg_config_dirs.split(":") if _xdg_config_dirs else []

        case "darwin":
            pass

        case "ios":
            pass

        case "android":
            pass

        case "linux":
            _data = _xdg_data or "~/.local/share"
            _config = _xdg_config or "~/.config"
            _state = _xdg_state or "~/.local/state"
            _app = "~/.local/bin"
            _cache = _xdg_cache or "~/.cache"
            _runtime = _xdg_runtime or f"/run/user/{os.getuid()}"
            _data_dirs = _xdg_data_dirs.split(":") if _xdg_data_dirs else ["/usr/local/share/", "/usr/share/"]
            _config_dirs = _xdg_config_dirs.split(":") if _xdg_config_dirs else ["/etc/xdg"]

        case _:
            pass
    
    @classmethod
    def home(cls):
        return Path.home()
    
    @classmethod
    def data(cls):
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
    def data_dirs(cls):
        if isinstance(cls._data_dirs[0], str):
            cls._data_dirs = [Path(p).expanduser() for p in cls._data_dirs]
        return cls._data_dirs

    @classmethod
    def config_dirs(cls):
        if isinstance(cls._config_dirs[0], str):
            cls._config_dirs = [Path(p).expanduser() for p in cls._config_dirs]
        return cls._config_dirs

