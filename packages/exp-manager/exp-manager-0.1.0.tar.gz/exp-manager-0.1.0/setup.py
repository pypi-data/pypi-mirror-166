# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exp_manager']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

setup_kwargs = {
    'name': 'exp-manager',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Usage instructions for experiment manager\nThis document describes to how use the experiment manager.\n\n## Overview\nThe experiment manager is a CLI tool that helps keep track of and annotate training runs. It works by maintaining the following directory structure:\n```\nout/\n|_____current_run.txt\n|_____run1/\n|_____run2/\n|_____run3/\n.\n.\n.\n```\nwhere `runN` contains the results and logs for a single training run. The folder names are sortable timestamps to aid navigation and are suffixed by the training run's title. The timestamp for each folder is also the run's ID. The folder name for the current/active run is stored in `current_run.txt`.\n\nEach training run folder contains a YAML file with name, description and experiment group name. The experiment manager can:\n- Show run metadata\n- Create a new run\n- Edit/delete an existing run\n- Pick an existing run to be the active run\n\nEach run can be annotated with a title, description and group name. The group name is used to group together runs when displaying a list of all runs.\n\nRun `python3 scripts/experiment_manager/exp_manager.py -h` to see a list of commands:\n```\nusage: exp_manager.py [-h] [--exp_dir EXP_DIR] {show,new,edit,delete,set} ...\n\npositional arguments:\n  {show,new,edit,delete,set}\n    show                show run(s)\n    new                 create new run\n    edit                edit existing run\n    delete              delete a run\n    set                 set a run as the current run\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --exp_dir EXP_DIR     parent directory containing all runs\n```\n\nEach command has a help option as well. e.g. run `python3 scripts/experiment_manager/exp_manager.py -h`\n```\nusage: exp_manager.py show [-h] [--all | --current | --id ID]\n\noptional arguments:\n  -h, --help     show this help message and exit\n  --all, -a      show all runs\n  --current, -c  show current run\n  --id ID        run ID\n```\n",
    'author': 'Arun Ramachandran',
    'author_email': 'arun.jhurricane@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
