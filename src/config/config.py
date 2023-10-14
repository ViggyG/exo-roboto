import os
import yaml


__config_path = os.getenv("CONFIG_FILE_PATH")
__config_dict: dict = {}

with open(__config_path, "r", encoding="utf8") as file:
    __config_dict = yaml.safe_load(file)


class Config:
    def __init__(self, params: dict) -> None:
        self.data_manager_params: dict = {}

        for k, value in params.items():
            if hasattr(self, k):
                setattr(self, k, value)
            else:
                print(f"WARNING, config given unknown param {k}")


app_config = Config(__config_dict)
