from before_shutdown.main import main
import os
import pathlib
import configparser

base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, 'config.txt')
config = configparser.ConfigParser()
config.read_file(open(config_path))

FOLDERS = [
 os.path.expandvars(config['DEFAULT']['RECALLFOLDER']),
]

def initialize_files_and_folders():
    for path in FOLDERS:
        path_obj = pathlib.Path(path)
        if not os.path.exists(path=path_obj):
            path_obj.mkdir(parents=True, exist_ok=True)


initialize_files_and_folders()

__all__ = [
    "main",
]