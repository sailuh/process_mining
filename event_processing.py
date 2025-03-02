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

import argparse
import pandas
import os
from datetime import datetime
import pm4py
import subprocess
import yaml

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
    print("Tree generated and saved")

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
    print("Graph generated and saved")

# Load config file from given path
def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main(config_file, action):
    # Load config file
    conf = load_config(config_file)
    csv_file = conf.get('process_mining', {}).get('csv_file_path')
    output_dir = conf.get('process_mining', {}).get('image_output_dir')

    # If-else for action choosen
    if action == 'start_end':
        start_activities, end_activities = start_end_activities(csv_file)
        print("Start Activities:", start_activities)
        print("End Activities:", end_activities)
    elif action == 'generate_tree':
        generate_tree(csv_file, output_dir)
    elif action == 'generate_graph':
        generate_graph(csv_file, output_dir)
    else:
        print(f"Unknown action choose: start_end, generate_tree, generate_graph.")

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Process mining script with pm4py")
    parser.add_argument('config_file', help='Path to the configuration file (.yml)')
    parser.add_argument('action', help='Action to perform (start_end, generate_tree, generate_graph)')
    args = parser.parse_args()
    # Call main
    main(args.config_file, args.action)