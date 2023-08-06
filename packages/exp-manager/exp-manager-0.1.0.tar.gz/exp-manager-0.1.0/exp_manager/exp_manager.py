from collections import defaultdict
from pathlib import Path

from exp_manager.run import Run

CURRENT_RUN_FILE_NAME = "current_run.txt"

def set_run_as_current(exp_dir: Path, run: Run):
    """
    Record the given run as current by writing its folder name to a file
    """
    run_dir_name = run.run_dir.stem
    current_run_file = exp_dir/CURRENT_RUN_FILE_NAME
    with open(current_run_file, "w") as f:
        f.write(run_dir_name + "\n")

def show_all(args):
    """
    Display all runs in the experiment folder grouped by group name in chronological order.
    The group with the newest run is printed at the bottom,
    and in each group, the newest run is printed at the bottom
    """
    runs = Run.find_all_runs(args.exp_dir)
    runs = sorted(runs, key=lambda run: run.run_id)

    parsed_runs = defaultdict(list)
    group_latest_runs = {}
    for run in runs:
        group = run.get_run_info()["group"]
        parsed_runs[group].append(run)
        group_latest_run = group_latest_runs.get(group)
        if group_latest_run is not None:
            group_latest_runs[group] = max(run.run_id, group_latest_run)
        else:
            group_latest_runs[group] = run.run_id

    group_order = sorted(group_latest_runs.items(), key=lambda kvp: kvp[1])
    for group, _ in group_order:
        group_runs = parsed_runs[group]
        print(f"{group}:")
        for run in group_runs:
            print(f"\t{run.run_id}: {run.get_run_info()['title']}")

def print_run(run: Run):
    """
    Print the given run's metadata
    """
    print("ID:", run.run_id)
    for key, val in run.get_run_info().items():
        print(f"{key}: {val}")

def show_current(args):
    """
    Print the current run's metadata
    """
    with open(args.exp_dir/CURRENT_RUN_FILE_NAME) as f:
        run_dir_name = f.read().strip()
    run_dir = args.exp_dir/run_dir_name
    run = Run(run_dir)
    print_run(run)

def show_run(args):
    """
    Find and print a run's metadata given its ID
    """
    run = Run.find_run(args.exp_dir, args.id)
    print_run(run)

def show(args):
    if args.all:
        show_all(args)
    elif args.current:
        show_current(args)
    elif args.id:
        show_run(args)
    else:
        print("No arguments given to 'show' command")
        exit(1)

def new(args):
    run = Run.create_run(args.exp_dir)
    set_run_as_current(args.exp_dir, run)

def edit(args):
    run = Run.find_run(args.exp_dir, args.id)
    run.edit_run()
    set_run_as_current(args.exp_dir, run)

def delete(args):
    run = Run.find_run(args.exp_dir, args.id)
    run.delete_run()

def set_current(args):
    run = Run.find_run(args.exp_dir, args.id)
    set_run_as_current(args.exp_dir, run)
