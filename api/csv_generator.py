import random
import pandas as pd
import uuid
from datetime import datetime, timedelta


# Function to generate fake data
def generate_fake_event_log(num_issues=1, num_events_per_issue=7, output_csv="generated_csv.csv", seed=42):
    """
    Generates fake event log data and saves it to a CSV file. The event log always startes with event 'assigned' and ends
    with event 'closed'. Events generated in between are randomly picked with options {'labeled', 'assigned', 'milestoned', 'closed', 'unlabeled', 'referenced', 'mentioned', 'subscribed'}.

    Args:
    - num_issues (int): Number of unique issues to generate.
    - num_events_per_issue (int): Number of events per issue
    - output_csv (str): The path where the CSV will be saved.
    - seed (int): Seed to get same results

    Returns:
    - str: The path to the saved CSV file
    """
    # Set seed given as parameter 
    random.seed(seed)
    # Set base time for all times to be based off of
    base_time = datetime(2020, 1, 1, 12, 0, 0)

    all_events = ['labeled', 'assigned', 'milestoned', 'closed', 'unlabeled', 'referenced', 'mentioned', 'subscribed']
    event_data = []

    for issue_num in range(1, num_issues + 1):
        # Always start with 'assigned' and end with 'closed'
        issue_events = ['assigned']

        # Choose (num_events_per_issue - 2) random events from the rest, excluding 'assigned' and 'closed'
        middle_candidates = [e for e in all_events if e not in ['assigned', 'closed']]
        middle_events = random.choices(middle_candidates, k=num_events_per_issue - 2)
        issue_events += middle_events
        issue_events.append('closed')

        for event_num, event in enumerate(issue_events):
            unique_id = str(uuid.uuid4())
            created_at = base_time + timedelta(minutes=event_num * 5 + issue_num * 60)
            created_at_str = created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
            event_data.append([unique_id, created_at_str, event, issue_num])

    event_log_df = pd.DataFrame(event_data, columns=['id', 'created_at', 'event', 'issue_number'])
    event_log_df.to_csv(output_csv, index=False)
    print(f"Fake event log data saved to {output_csv}")
    return output_csv

def modify_event(event_log_df, row_index, new_event):
    """
    Modify events in the given event log dataframe.

    Args:
    - event_log_df (pd.DataFrame): The event log data frame.
    - row_index (int): The index of the row to modify.
    - new_event (str): The new event value to assign.

    Returns:
    - pd.DataFrame: The modified event log dataframe.
    """
    # Ensure row_index is within the bounds of the dataframe
    if row_index < 0 or row_index >= len(event_log_df):
        raise IndexError(f"Row index {row_index} is out of bounds.")
    
    event_log_df.loc[row_index, 'event'] = new_event
    return event_log_df


