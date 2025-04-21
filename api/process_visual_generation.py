"""
# 📊 Process Visualization Module

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

---

## Dependencies

- `pandas`
- `pm4py`

---

## Example

```python
from process_visual_generation import start_end_activities, generate_tree_inductive

start_acts, end_acts = start_end_activities("data/log.csv")
generate_tree_inductive("data/log.csv", "~/Downloads")
```
"""

import os
from api.io_helpers import generate_filename, load_event_log
import pandas
import pm4py


def start_end_activities(csv_path):
    """
    Reads an event log from a CSV file and returns its start and end activities.

    Assumes the CSV has the following columns:
        - id': Unique case identifier.
        - 'event': Activity name or label.
        - 'created_at': Timestamp of the event.

    Args:
        csv_path (str): Path to the event log CSV file.

    Returns:
        tuple[dict, dict]: A tuple containing:
            - dict: Start activities and their counts.
            - dict: End activities and their counts.

    Raises:
        FileNotFoundError: If the CSV path is invalid
        ValueError: If required columns are missing.
    """
    event_log = load_event_log(csv_path)

    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    return start_activities, end_activities


def generate_tree_inductive(csv_path, output_dir):
    """
    Generates and saves a process tree visualization from an event log. Uses the Inductive Miner algorithm.

    Assumes the CSV has the following columns:
        - 'issue_number': Unique case identifier.
        - 'event': Activity name or label.
        - 'created_at': Timestamp of the event.

    Args:
        csv_path (str): Path to the event log CSV file.
        output_dir (str): Directory where the PNG image will be saved.

    Returns:
        None

    Side Effects:
        Saves a PNG file of the process tree to the specified output directory.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing.
    """
    event_log = load_event_log(csv_path)

    file_name = generate_filename("process_tree")
    output_path = os.path.join(output_dir, file_name)
    
    # Run Inductive Miner to generate tree.
    process_tree = pm4py.discover_process_tree_inductive(event_log)
    pm4py.save_vis_process_tree(process_tree, output_path)
    print(f"Tree generated and saved to {output_path}")


def generate_graph_inductive(csv_path, output_dir, noise_threshold=0.0):
    """
    Generates and saves a filtered process graph visualization from an event log,
    using a noise threshold to remove less relevant activities. Uses the Inductive Miner algorithm. 

    Assumes the CSV has the following columns:
        - 'issue_number': Unique case identifier.
        - 'event': Activity name or label.
        - 'created_at': Timestamp of the event.

    Args:
        csv_path (str): Path to the event log CSV file.
        output_dir (str): Directory where the PNG image will be saved.
        noise_threshold (float): Threshold for filtering noise in the process graph (default is 0.0).

    Returns:
        None

    Side Effects:
        Saves a PNG file of the filtered process graph to the specified output directory.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing or the noise threshold is invalid.
    """
    event_log = load_event_log(csv_path)

    file_name = generate_filename("process_graph_filtered")
    output_path = os.path.join(output_dir, file_name)

    # Run the BPMN model with a noise threshold.
    bpmn_filtered = pm4py.discover_bpmn_inductive(event_log, noise_threshold)
    pm4py.save_vis_bpmn(bpmn_filtered, output_path, format="png")
    print(f"Graph generated and saved to {output_path}")


def generate_performance_graph_dfg(csv_path, output_dir):
    """
    Generates and saves a performance-related Directed Flow Graph (DFG) visualization.

    Assumes the CSV has the following columns:
        - 'issue_number': Unique case identifier.
        - 'event': Activity name or label.
        - 'created_at': Timestamp of the event.

    Args:
        csv_path (str): Path to the event log CSV file.
        output_dir (str): Directory where the PNG image will be saved.

    Returns:
        None

    Side Effects:
        Saves a PNG file of the performance DFG to the specified output directory.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing.
    """
    event_log = load_event_log(csv_path)


    file_name = generate_filename("performance_dfg")
    output_path = os.path.join(output_dir, file_name)
    
    # Run DFG and generate performance graph.
    performance_dfg, start_activities, end_activities = pm4py.discover_performance_dfg(event_log, case_id_key='issue_number', activity_key='event', timestamp_key='created_at')
    pm4py.save_vis_performance_dfg(performance_dfg, start_activities, end_activities, output_path)
    print(f"Graph generated and saved to {output_path}")


def generate_count_graph_dfg(csv_path, output_dir):
    """
    Generates and saves an occurrence-based Directed Flow Graph (DFG) visualization,
    which shows the frequency of activity transitions.

    Assumes the CSV has the following columns:
        - 'issue_number': Unique case identifier.
        - 'event': Activity name or label.
        - 'created_at': Timestamp of the event.

    Args:
        csv_path (str): Path to the event log CSV file.
        output_dir (str): Directory where the PNG image will be saved.

    Returns:
        None

    Side Effects:
        Saves a PNG file of the occurrence DFG to the specified output directory.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing.
    """
    event_log = load_event_log(csv_path)

    file_name = generate_filename("occurrence_dfg")
    output_path = os.path.join(output_dir, file_name)
    
    # Run DFG and generate graph.
    performance_dfg, start_activities, end_activities = pm4py.discover_performance_dfg(event_log, case_id_key='issue_number', activity_key='event', timestamp_key='created_at')
    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log, case_id_key='issue_number', activity_key='event', timestamp_key='created_at')
    pm4py.save_vis_dfg(dfg, start_activities, end_activities, output_path)
    print(f"Graph generated and saved to {output_path}")


def generate_petri_net_inductive(csv_path, output_dir):
    """
    Generates and saves a Petri net visualization from an event log using the Inductive Miner.

    Assumes the CSV has the following columns:
        - 'issue_number': Unique case identifier.
        - 'event': Activity name or label.
        - 'created_at': Timestamp of the event.

    Args:
        csv_path (str): Path to the event log CSV file.
        output_dir (str): Directory where the PNG image will be saved.

    Returns:
        None

    Side Effects:
        Saves a PNG file of the Petri net to the specified output directory.

    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If required columns are missing.
    """
    event_log = load_event_log(csv_path)

    file_name = generate_filename("petri_net")
    output_path = os.path.join(output_dir, file_name)

    # Run Inductive Miner and generate Petri Net.
    net, im, fm = pm4py.discover_petri_net_inductive(event_log, case_id_key='issue_number', activity_key='event', timestamp_key='created_at')
    pm4py.save_vis_petri_net(net, im, fm, output_path, format="png")
    print(f"Graph generated and saved to {output_path}")
