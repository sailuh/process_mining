"""
# 📊 Process Discovery Module

Module for visualizing process event logs using **PM4Py**.

---

## Features

This module provides functions to:

- Extract **start** and **end** activities from a CSV log.
- Generate and save various visualizations:
  - **Process tree**
  - **Process graph (with filtering)**
  - **Performance-based DFG** (Directed Flow Graph)
  - **Occurrence-based DFG** (Directed Flow Graph)
  - **Petri net**

All functions assume the CSV argument has the following columns [`io.read_event_log`](io.html#read_event_log):
- 'issue_number': Unique case identifier.
- 'event': Activity name or label.
- 'created_at': Timestamp of the event.

---

## Dependencies

- `pandas`
- `pm4py`

---

## Example

```python
from process_discovery import start_end_activities, generate_tree_inductive

start_acts, end_acts = start_end_activities("data/log.csv")

generate_tree_inductive("data/log.csv")
```
"""

import os
from .io import generate_timestamped_filename, read_event_log
import pm4py


def start_end_activities(csv_path):
    """
    Reads an event log from a CSV file and returns its start and end activities.

    Assumes the CSV has required columns, see here: [`io.read_event_log`](io.html#read_event_log)


    Args:
    - csv_path (str): Path to the event log CSV file.

    Returns:
    tuple[dict, dict]: A tuple containing:
    - dict: Start activities and their counts.
    - dict: End activities and their counts.

    Raises:
    FileNotFoundError: If the CSV path is invalid
    ValueError: If required columns are missing.
    """
    event_log = read_event_log(csv_path)

    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    return start_activities, end_activities


def generate_tree_inductive(csv_path, output_dir=None, action="view"):
    """
    Generates and saves a process tree visualization from an event log. Uses the Inductive Miner algorithm.

    Assumes the CSV has required columns, see here: [`io.read_event_log`](io.html#read_event_log)

    Args:
    - csv_path (str): Path to the event log CSV file.
    - output_dir (str, optional): Directory where the PNG image will be saved. Required if action is 'save' or 'both'.
    - action (str): One of {'view', 'save', 'both'}.
        - 'view': Display the graph in the current environment. (Default action)
        - 'save': Save the graph to the specified output_dir.
        - 'both': Display and save the graph.

    Returns:
        None

    Side Effects:
        Saves a PNG file of the performance DFG to the specified output directory if action is 'save' or 'both'.
        Displays the visualization if action is 'view' or 'both'.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing, or output_dir is not provided when action is 'save' or 'both'.
    """
    event_log = read_event_log(csv_path)

    process_tree = pm4py.discover_process_tree_inductive(event_log)

    if action == "view" or action == "both":
        pm4py.view_process_tree(process_tree)

    if action == "save" or action == "both":
        if output_dir is not None:
            if not os.path.exists(output_dir):
                raise FileNotFoundError(f"The specified directory does not exist: {output_dir}")
            file_name = generate_timestamped_filename("process_tree")
            output_path = os.path.join(output_dir, file_name)
            pm4py.save_vis_process_tree(process_tree, output_path)
            print(f"Tree generated and saved to {output_path}")
        else:
            raise ValueError("Output directory must be specified for saving.")


def generate_graph_inductive(csv_path, output_dir=None, action="view", noise_threshold=0.0):
    """
    Generates and saves a filtered process graph visualization from an event log,
    using a noise threshold to remove less relevant activities. Uses the Inductive Miner algorithm. 

    Assumes the CSV has required columns, see here: [`io.read_event_log`](io.html#read_event_log)

    Args:
    - csv_path (str): Path to the event log CSV file.
    - output_dir (str, optional): Directory where the PNG image will be saved. Required if action is 'save' or 'both'.
    - noise_threshold (float): Threshold for filtering noise in the process graph (default is 0.0).
    - action (str): One of {'view', 'save', 'both'}.
        - 'view': Display the graph in the current environment. (Default action)
        - 'save': Save the graph to the specified output_dir.
        - 'both': Display and save the graph.
        
    Returns:
        None

    Side Effects:
        Saves a PNG file of the filtered process graph to the specified output directory if action is 'save' or 'both'.
        Displays the visualization if action is 'view' or 'both'.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing, output_dir is not provided when needed, or noise_threshold is invalid.
    """
    if not (0.0 <= noise_threshold <= 1.0):
        raise ValueError("Noise threshold must be between 0.0 and 1.0.")

    event_log = read_event_log(csv_path)

    bpmn_filtered = pm4py.discover_bpmn_inductive(event_log, noise_threshold)

    if action == "view" or action == "both":
        pm4py.view_bpmn(bpmn_filtered)

    if action == "save" or action == "both":
        if output_dir is not None:
            if not os.path.exists(output_dir):
                raise FileNotFoundError(f"The specified directory does not exist: {output_dir}")
            file_name = generate_timestamped_filename("process_graph_inductive")
            output_path = os.path.join(output_dir, file_name)
            pm4py.save_vis_bpmn(bpmn_filtered, output_path, format="png")
            print(f"Graph generated and saved to {output_path}")
        else:
            raise ValueError("Output directory must be specified for saving.")


def generate_performance_graph_dfg(csv_path, output_dir=None, action="view"):
    """
    Generates and saves a performance-related Directed Flow Graph (DFG) visualization.

    Assumes the CSV has required columns, see here: [`io.read_event_log`](io.html#read_event_log)

    Args:
    - csv_path (str): Path to the event log CSV file.
    - output_dir (str, optional): Directory where the PNG image will be saved. Required if action is 'save' or 'both'.
    - action (str): One of {'view', 'save', 'both'}.
        - 'view': Display the graph in the current environment. (Default action)
        - 'save': Save the graph to the specified output_dir.
        - 'both': Display and save the graph.

    Returns:
        None

    Side Effects:
        Saves a PNG file of the performance DFG to the specified output directory if action is 'save' or 'both'.
        Displays the visualization if action is 'view' or 'both'.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing, or output_dir is not provided when action is 'save' or 'both'.
    """
    event_log = read_event_log(csv_path)

    performance_dfg, start_activities, end_activities = pm4py.discover_performance_dfg(event_log, case_id_key='issue_number', activity_key='event', timestamp_key='created_at')

    if action == "view" or action == "both": 
        pm4py.view_performance_dfg(performance_dfg, start_activities, end_activities)
    if action == "save" or action == "both":
        if output_dir is not None:
            if not os.path.exists(output_dir):
                raise FileNotFoundError(f"The specified directory does not exist: {output_dir}")
            file_name = generate_timestamped_filename("performance_dfg")
            output_path = os.path.join(output_dir, file_name)
            pm4py.save_vis_performance_dfg(performance_dfg, start_activities, end_activities)
            print(f"Graph generated and saved to {output_path}")
        else: 
            raise ValueError("Output directory must be specified for saving.")


def generate_count_graph_dfg(csv_path, output_dir=None, action="view"):
    """
    Generates and saves an occurrence-based Directed Flow Graph (DFG) visualization,
    which shows the frequency of activity transitions.

    Assumes the CSV has required columns, see here: [`io.read_event_log`](io.html#read_event_log)

    Args:
    - csv_path (str): Path to the event log CSV file.
    - output_dir (str): Directory where the PNG image will be saved.
    - action (str): One of {'view', 'save', 'both}. 
        - 'view': Display the graph in the current enviroment. (Default action)
        - 'save': Save the graph to the specified output_dir.
        - 'both': Display and save the graph. 

    Returns:
        None

    Side Effects:
        Saves a PNG file of the occurrence DFG to the specified output directory if action is 'save' or 'both'.
        Displays the visualization if action is 'view' or 'both'.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing, or output_dir is not provided when action is 'save' or 'both'.
    """
    event_log = read_event_log(csv_path)
    
    # Run DFG and generate graph.
    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log, case_id_key='issue_number', activity_key='event', timestamp_key='created_at')

    if action == "view" or action == "both":
        pm4py.view_dfg(dfg, start_activities, end_activities)
    if action == "save" or action == "both":
        if output_dir is not None: 
            if not os.path.exists(output_dir):
                raise FileNotFoundError(f"The specified directory does not exist: {output_dir}")
        
            file_name = generate_timestamped_filename("occurrence_dfg")
            output_path = os.path.join(output_dir, file_name)
            pm4py.save_vis_dfg(dfg, start_activities, end_activities, output_path)
            print(f"Graph generated and saved to {output_path}")
        else: 
            raise ValueError("Output directory must be specified for saving.")


def generate_petri_net_inductive(csv_path, output_dir=None, action="view"):
    """
    Generates and saves a Petri net visualization from an event log using the Inductive Miner.

    Assumes the CSV has required columns, see here: [`io.read_event_log`](io.html#read_event_log)

    Args:
    - csv_path (str): Path to the event log CSV file.
    - output_dir (str): Directory where the PNG image will be saved.
    - action (str): One of {'view', 'save', 'both}. 
        - 'view': Display the graph in the current enviroment. (Default action)
        - 'save': Save the graph to the specified output_dir.
        - 'both': Display and save the graph. 

    Returns:
        None

    Side Effects:
        Saves a PNG file of the occurrence DFG to the specified output directory if action is 'save' or 'both'. Displays the visualization if action is 'view' or 'both'.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing, or output_dir is not provided when action is 'save' or 'both'.
    """
    event_log = read_event_log(csv_path)

    net, im, fm = pm4py.discover_petri_net_inductive(event_log, case_id_key='issue_number', activity_key='event', timestamp_key='created_at')

    if action == "view" or action == "both":
        pm4py.view_petri_net(net, im, fm)
    if action == "save" or action == "both":
        if output_dir is not None: 
            if not os.path.exists(output_dir):
                raise FileNotFoundError(f"The specified directory does not exist: {output_dir}")
        
            file_name = generate_timestamped_filename("petri_net")
            output_path = os.path.join(output_dir, file_name)
            pm4py.save_vis_petri_net(net, im, fm, output_path, format="png")
            print(f"Graph generated and saved to {output_path}")
        else: 
            raise ValueError("Output directory must be specified for saving.")