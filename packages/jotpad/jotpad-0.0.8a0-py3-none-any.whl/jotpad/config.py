import os
import configparser
import errno

from appdirs import user_config_dir, user_data_dir
from rich.console import Console



APP_NAME = "jotpad"
APP_AUTHOR = "jotpad"

class Config:
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read(os.path.join(f"{user_config_dir(APP_NAME)}", "config.ini"))

        if "jotpad" not in self._config:
            # init the config file
            try:
                os.makedirs(user_config_dir(APP_NAME))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise RuntimeError("Unable to create config directory")

            self._config["jotpad"] = {
                "home": user_data_dir(APP_NAME, APP_AUTHOR),
                "editor": "vim",
                "default_extension": "txt",
            }
            with open(os.path.join(f"{user_config_dir(APP_NAME)}", "config.ini"), "w") as f:
                self._config.write(f)
            
            console = Console()
            console.print(f"[DEBUG] config_dir={user_config_dir(APP_NAME)}")
            console.print(f"[DEBUG] data_dir={user_data_dir(APP_NAME, APP_AUTHOR)}")
            console.print(f"[DEBUG] config.home={self._config['jotpad']['home']}")
            console.print(f"[DEBUG] config.editor={self._config['jotpad']['editor']}")
            console.print(f"[DEBUG] config.default_extension={self._config['jotpad']['default_extension']}")
    
    def _write(self):
        with open(os.path.join(f"{user_config_dir(APP_NAME)}", "config.ini"), "w") as f:
            self._config.write(f)
    
    @property
    def home(self):
        if "home" in self._config["jotpad"]:
            return self._config["jotpad"]["home"]
        
        try:
            os.makedirs(user_data_dir(APP_NAME, APP_AUTHOR))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise RuntimeError("Unable to create data directory")
        return user_data_dir(APP_NAME, APP_AUTHOR)

    @home.setter
    def home(self, value):
        self._config["jotpad"]["home"] = value
        self._write()
    
    @property
    def editor(self):
        return self._config["jotpad"]["editor"]

    @editor.setter
    def editor(self, value):
        self._config["jotpad"]["editor"] = value
        self._write()

    @property
    def default_extension(self):
        return self._config["jotpad"]["default_extension"]
    
    @default_extension.setter
    def default_extension(self, value):
        self._config["jotpad"]["default_extension"] = value
        self._write()
