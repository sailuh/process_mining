# =============================================================================
# Title: Event Processing
# Author: Sailuh
# Description: 
# This Python script utilizes the pm4py library for process mining tasks.
#
# Requirements:
# - Python 3.x
#
# Usage:
# - Ensure the script is run in a Python environment
# - If pm4py is not installed, the script will install it
#
# License: MIT License
# =============================================================================

# Install pm4py if not already done
try: 
    import pm4py
    print("pm4py already installed")
except ImportError:
    import subprocess
    subprocess.check_call(["python", "-m", "pip", "install", "pm4py"])
    import pm4py
    print("pm4py installed!")

import pandas
import os
from datetime import datetime

# Return start & end activities
def start_end_activities(csv_path): 
    event_log = pandas.read_csv(csv_path)
    event_log = pm4py.format_dataframe(event_log, case_id='id', activity_key='event', timestamp_key='created_at')
    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    return start_activities, end_activities

# Generate tree at output_dir directory from csv_path file
def generate_tree(csv_path, output_dir):
    event_log = pandas.read_csv(csv_path)
    event_log = pm4py.format_dataframe(event_log, case_id='issue_number', activity_key='event', timestamp_key='created_at')

    # Set up path and name of .png
    output_dir = os.path.expanduser(output_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"process_tree_{timestamp}.png"
    output_path = os.path.join(output_dir, file_name)

    process_tree = pm4py.discover_process_tree_inductive(event_log)
    pm4py.save_vis_process_tree(process_tree, output_path)

# Generate graph at output_dir directory from csv_path file
def generate_graph(csv_path, output_dir):
    event_log = pandas.read_csv(csv_path)
    event_log = pm4py.format_dataframe(event_log, case_id='issue_number', activity_key='event', timestamp_key='created_at')
    
    # Set up path and name of .png
    output_dir = os.path.expanduser(output_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"process_tree_{timestamp}.png"
    output_path = os.path.join(output_dir, file_name)

    process_tree = pm4py.discover_process_tree_inductive(event_log)
    bpmn_model = pm4py.convert_to_bpmn(process_tree)
    pm4py.save_vis_bpmn(bpmn_model, output_path, format="png")

