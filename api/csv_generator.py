import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# Initialize faker
fake = Faker()

# Function to generate fake data
def generate_csv_file(num_issues=1, num_events_per_issue=7, output_csv="generated_csv", seed=2):
    """
    Generates fake event log data and saves it to a CSV file.

    Args:
        num_issues (int): Number of unique issues to generate.
        num_events_per_issue (int): Number of events per issue
        output_csv (str): The path where the CSV will be saved.
        seed (int): Seed to get same results

    Returns:
        str: The path to the saved CSV file
    """
    # Set seed given as parameter 
    random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    # Set base time for all times to be based off of
    base_time = datetime(2020, 1, 1, 12, 0, 0)

    all_events = ['labeled', 'assigned', 'milestoned', 'closed', 'unlabeled', 'referenced', 'mentioned', 'subscribed']
    event_data = []

    for issue_num in range(1, num_issues + 1):
        # Always start with 'assigned' and end with 'closed'
        issue_events = ['assigned']

        # Choose (num_events_per_issue - 2) random events from the rest, excluding 'assigned' and 'closed'
        middle_candidates = [e for e in all_events if e not in ['assigned', 'closed']]
        middle_events = random.sample(middle_candidates, k=num_events_per_issue - 2)
        issue_events += middle_events
        issue_events.append('closed')

        for event_num, event in enumerate(issue_events):
            unique_id = fake.uuid4()
            created_at = base_time + timedelta(minutes=event_num * 5 + issue_num * 60)
            created_at_str = created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
            event_data.append([unique_id, created_at_str, event, issue_num])

    event_log_df = pd.DataFrame(event_data, columns=['id', 'created_at', 'event', 'issue_number'])
    event_log_df.to_csv(output_csv, index=False)
    print(f"Fake event log data saved to {output_csv}")
    return output_csv

def modify_event_in_csv(csv_path, row_index, new_event, output_csv=None):
    """
    Modifies the 'event' value in a specific row of a CSV file.

    Args:
        csv_path (str): Path to the original CSV file.
        row_index (int): Zero-based index of the row to modify.
        new_event (str): The new event value to assign.
        output_csv (str, optional): Path to save the modified CSV. Otherwise overwrites the original
    """
    df = pd.read_csv(csv_path)

    if row_index < 0 or row_index >= len(df):
        raise IndexError(f"Row index {row_index} is out of bounds.")

    df.loc[row_index, 'event'] = new_event

    save_path = output_csv if output_csv else csv_path
    df.to_csv(save_path, index=False)
    print(f"Modified CSV saved to {save_path}")


