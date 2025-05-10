from datetime import datetime
import pandas
import pm4py


def generate_timestamped_filename(prefix, extension="png"):
    """
    Generates a unique file name with a given prefix and file extension.

    Args:
    - prefix (str): The prefix to be added to the file name.
    - extension (str): The extension of the file (default is "png").

    Returns:
    - str: The generated file name with the current timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def read_event_log(csv_path):
    """
    Loads and formats an event log CSV for use with PM4Py.

    Args:
    - csv_path (str): Path to the event log CSV file.

    Returns:
    - pd.DataFrame: A formatted DataFrame ready for process mining.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing.
    """
    event_log = pandas.read_csv(csv_path)

    if not {'issue_number', 'event', 'created_at'}.issubset(event_log.columns):
        raise ValueError("CSV must contain 'issue_number', 'event', and 'created_at' columns.")

    event_log['issue_number'] = event_log['issue_number'].astype(str)
    event_log['created_at'] = pandas.to_datetime(event_log['created_at'], errors='coerce')

    # PM4PY format
    formatted_log = pm4py.format_dataframe(event_log, case_id='issue_number', activity_key='event', timestamp_key='created_at')
    
    return formatted_log