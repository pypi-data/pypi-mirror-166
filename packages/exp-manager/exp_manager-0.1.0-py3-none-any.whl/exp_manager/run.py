from typing import Any, Dict, List, Union

from datetime import datetime
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile

from exp_manager.utils import read_yaml

EMPTY_RUN_INFO_FILE = Path(__file__).parent/"empty_run_info.yaml"
RUN_INFO_FILE_NAME = "run_info.yaml"
RUN_DIR_SEPARATOR = "__"

def open_editor(file: Union[Path, str]):
    """
    Open vim to edit a file
    """
    system = platform.system()
    if system == "Linux":
        editor_process_results = subprocess.run(["vim", str(file)])
    elif system == "Windows":
        editor_process_results = subprocess.run(["notepad.exe", str(file)])
    else:
        raise ValueError("Platform", system, "is not supported yet.")
    editor_process_results.check_returncode()


class Run(object):
    """Class representing a training run"""

    @staticmethod
    def create_run_dir_name(run_id: str, run_title: str) -> str:
        return f"{run_id}{RUN_DIR_SEPARATOR}{run_title}"

    def __init__(self, run_dir: Path):
        self.run_dir = run_dir
        self._run_info = None
        self._run_info_open_time = None

    @classmethod
    def create_run(cls, exp_dir: Path) -> 'Run':
        """
        Create a new training run folder and get run metadata from the user
        """
        now = datetime.now()
        now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
        run_dir_name = Run.create_run_dir_name(now_str, "")
        run_dir = exp_dir/run_dir_name
        run_dir.mkdir(parents=True)
        run = cls(run_dir)
        shutil.copy(EMPTY_RUN_INFO_FILE, run.run_file)
        run.edit_run()
        return run

    @classmethod
    def find_run(cls, exp_dir: Path, run_id: str) -> 'Run':
        """
        Find an existing training run given its ID
        """
        run_dirs = list(exp_dir.glob(f"{run_id}*"))
        assert len(run_dirs) == 1, f"Invalid ID {run_id} given, found multiple runs with same ID"
        return cls(run_dirs[0])
    
    @classmethod
    def find_all_runs(cls, exp_dir: Path) -> List['Run']:
        """
        Return all training runs whose folders are direct children in a parent directory
        """
        run_dirs = exp_dir.glob("*")
        runs = []
        for run_dir in run_dirs:
            run = cls(run_dir)
            if run.run_file.is_file():
                runs.append(run)
        return runs

    @property
    def run_id(self) -> str:
        return self.run_dir.stem.split(RUN_DIR_SEPARATOR, 1)[0]
    
    @property
    def run_file(self) -> Path:
        return self.run_dir/RUN_INFO_FILE_NAME
    
    def get_run_info(self) -> Dict[str, Any]:
        """
        Get metadata about the training run
        """
        if (
            self._run_info_open_time is None or
            self._run_info_open_time < self.run_file.stat().st_mtime
        ):
            self._run_info = read_yaml(self.run_file)
            self._run_info_open_time = datetime.now().timestamp()
        return self._run_info
    
    def edit_run(self):
        """
        Let the user edit the training run's metadata
        """
        run_file = self.run_file
        run_file_tmp = Path(tempfile.gettempdir(), "hyperion_exp_manager.yaml")
        shutil.copy(run_file, run_file_tmp)

        is_valid_edit = False
        while not is_valid_edit:
            open_editor(run_file_tmp)
            new_run_info = read_yaml(run_file_tmp)
            is_valid_edit = {"title", "description", "group"}.issubset(new_run_info.keys())

        shutil.move(run_file_tmp, run_file)
        new_run_dir_name = Run.create_run_dir_name(self.run_id, self.get_run_info()["title"])
        new_run_dir = self.run_dir.parent/new_run_dir_name
        shutil.move(self.run_dir, new_run_dir)
        self.run_dir = new_run_dir
    
    def delete_run(self):
        shutil.rmtree(self.run_dir)
