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
            _state = _xdg_state or _local_data # /<APPNAME>/State
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
            _state = _xdg_state or "~/Library/Preferences" # /<APPNAME>/State
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
            _state = _xdg_state or "~/Library/Preferences"  # Mirror macOS
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
    def data(cls, app_name: str = None, local=False):
        app_name = app_name if app_name else ""
        if local and sys.platform == "win32":
            return Path(cls._local_data, app_name).expanduser()
        else:
            return Path(cls._data, app_name).expanduser()
    
    @classmethod
    def config(cls, app_name: str = None):
        app_name = app_name if app_name else ""
        return Path(cls._config, app_name).expanduser()

    @classmethod
    def state(cls, app_name: str = None):
        app_name = app_name if app_name else ""
        if sys.platform in ["win32", "darwin", "ios"]:
            return Path(cls._state, app_name, "State").expanduser()
        else:
            return Path(cls._state, app_name).expanduser()

    @classmethod
    def app(cls):
        return Path(cls._app).expanduser()
    
    #@classmethod
    #def program_files(cls):
    #    if sys.platform == "win32":
    #        if isinstance(cls._win_program_files, str):
    #            cls._win_program_files = Path(cls._win_program_files).expanduser()
    #        return cls._win_program_files
    #    else:
    #        raise RuntimeError("Program Files exists only on Windows!")

    @classmethod
    def cache(cls, app_name: str = None):
        app_name = app_name if app_name else ""
        return Path(cls._cache, app_name).expanduser()

    @classmethod
    def runtime(cls):
        return Path(cls._runtime).expanduser()

    @classmethod
    def data_dirs(cls, app_name: str = None, include_home=False, local=False):
        app_name = app_name if app_name else ""
        # Follow XDG spec and don't include user data home unless requested
        # Would be more convenient if `include_home=True` by default though...
        dirs = [Path(p, app_name).expanduser() for p in cls._data_dirs]
        if include_home:
            return [cls.data(app_name=app_name, local=local)] + dirs
        else:
            return dirs

    @classmethod
    def config_dirs(cls, app_name: str = None, include_home=False):
        app_name = app_name if app_name else ""
        # Follow XDG spec and don't include user config home unless requested
        # Would be more convenient if `include_home=True` by default though...
        dirs = [Path(p, app_name).expanduser() for p in cls._config_dirs]
        if include_home:
            return [cls.config(app_name=app_name)] + dirs
        else:
            return dirs
        
    def __init__(self, app_name: str):
        self.data = self.data(app_name=app_name)
        self.config = self.config(app_name=app_name)
        self.state = self.state(app_name=app_name)
        self.app = self.app()
        self.cache = self.cache(app_name=app_name)
        self.runtime = self.runtime()
        self.data_dirs = self.data_dirs(app_name=app_name)
        self.config_dirs = self.config_dirs(app_name=app_name)
