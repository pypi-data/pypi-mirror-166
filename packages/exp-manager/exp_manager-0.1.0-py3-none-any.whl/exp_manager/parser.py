import argparse
from pathlib import Path

from exp_manager.exp_manager import delete, edit, new, set_current, show

def add_id_arg(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--id",
        help="run ID",
    )

parser = argparse.ArgumentParser()
parser.add_argument(
    "--exp_dir",
    default=Path("outputs"),
    help="parent directory containing all runs"
)
subparsers = parser.add_subparsers()

show_parser = subparsers.add_parser("show", help="show run(s)")
show_parser_mutex_grp = show_parser.add_mutually_exclusive_group()
show_parser_mutex_grp.add_argument(
    "--all", "-a",
    help="show all runs",
    action="store_true",
)
show_parser_mutex_grp.add_argument(
    "--current", "-c",
    help="show current run",
    action="store_true",
)
add_id_arg(show_parser_mutex_grp)
show_parser.set_defaults(func=show)

new_parser = subparsers.add_parser("new", help="create new run")
new_parser.set_defaults(func=new)

edit_parser = subparsers.add_parser("edit", help="edit existing run")
add_id_arg(edit_parser)
edit_parser.set_defaults(func=edit)

delete_parser = subparsers.add_parser("delete", help="delete a run")
add_id_arg(delete_parser)
delete_parser.set_defaults(func=delete)

set_parser = subparsers.add_parser("set", help="set a run as the current run")
add_id_arg(set_parser)
set_parser.set_defaults(func=set_current)
