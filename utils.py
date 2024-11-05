import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import csv

from constants import *

# Extracts data from the .csv file and prepares for processing
def create_dataframe():
    # Crete a list for every field within the .csv
    timestamp, device_id, experiment_group, session_id, query_length, selected_id, query_id, query_outcome  = [], [], [], [], [], [], [], []
    
    # Open the .csv file and extract data
    with open(INPUT_DATA_FILE, 'r') as csvfile: 
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            try:
                timestamp.append(float(row[0]))
                device_id.append(row[1])
                
                event_data = json.loads(row[2])
                session_id.append(event_data.get('session_id'))
                experiment_group.append(int(event_data.get('experimentGroup')))
                query_length.append(int(event_data.get('searchStateFeatures', {}).get('queryLength')))
                
                if event_data.get('selectedIndexes') is not None:
                    selected_id.append(event_data.get('selectedIndexes')[0])
                else:
                    selected_id.append(None)
                    
                query_id.append(int(event_data.get('eventIndex')))
                
                query_outcome.append(row[3])
                
            except ValueError:
                continue
    
    # Combine lists into a pandas DataFrame
    df = pd.DataFrame(
        {
            "timestamp" : timestamp,
            "device_id" : device_id,
            "experiment_group" : experiment_group,
            "session_id" : session_id,
            "query_length" : query_length,
            "selected_id" : selected_id,
            "query_id" : query_id,
            "query_outcome" : query_outcome
        }
    )
    
    return df
	
def plot_data(group_0_results, group_1_results):
    metrics = list(group_0_results.keys())
    group_0_values = [group_0_results[metric] for metric in metrics]
    group_1_values = [group_1_results[metric] for metric in metrics]

    num_metrics = len(metrics)

    # Create subplots
    fig, axs = plt.subplots(num_metrics, 1, figsize=(8, 2 * num_metrics), constrained_layout=True)
    plt.title("performance_comparioson")

    # Plot each metric in a separate subplot
    for i, metric in enumerate(metrics):
        # Histogram data for the current metric
        data = [group_0_values[i], group_1_values[i]]
        labels = [metric + '_0', metric + '_1']
        colors = ['blue', 'orange']

        # Plot histogram for each dictionary's value as side-by-side bars
        axs[i].bar(labels, data, color=colors)
        
        # Set titles and labels
        axs[i].set_title(metric)
        axs[i].set_ylabel('Value')
        
        # Display value on top of bars
        for j, value in enumerate(data):
            axs[i].text(j, value + 0.1, f'{value:.2f}', ha='center', va='bottom')
    
    plt.savefig(PLOT_OUTPUT_FILE, format="pdf", dpi=300, bbox_inches='tight')
    # Show plot
    plt.show()

def write_report(group_0_results, group_1_results):
    #Open output file and save analysis data
    with open(REPORT_OUTPUT_FILE, 'w') as file:
        file.write("Group 0: \n")
        file.write("Percentage of successful sessions: " + str(group_0_results['success_percentage']) + "\n")
        file.write("Average number of querys before success: " + str(group_0_results['avg_querys_before_success']) + "\n")
        file.write("Average elapsed time in session before success: " + str(group_0_results['avg_elapsed_time_before_success']) + "\n")
        file.write("Average difference in query length between first and last query (in successful sessions): " + str(group_0_results['avg_query_length_diff']) + "\n")
        file.write("Average ranking of selected option: " + str(group_0_results['avg_choice_rank']) + "\n")
        
        file.write("Group 1: \n")
        file.write("Percentage of successful sessions: " + str(group_1_results['success_percentage']) + "\n")
        file.write("Average number of querys before success: " + str(group_1_results['avg_querys_before_success']) + "\n")
        file.write("Average elapsed time in session before success: " + str(group_1_results['avg_elapsed_time_before_success']) + "\n")
        file.write("Average difference in query length between first and last query (in successful sessions): " + str(group_1_results['avg_query_length_diff']) + "\n")
        file.write("Average ranking of selected option: " + str(group_1_results['avg_choice_rank']) + "\n")
        
# Using the pandas.read_csv() function makes the data extraction and preparation process last 17 times longer when performed on the relevant .csv with ~100 000 rows
# Additionaly, the following code requires further preparation, or changes to eval.py, in order tp 

# def create_dataframe():
    # df = pd.read_csv(INPUT_DATA_FILE)
    # df = df.rename(columns={'time_epoch' : 'timestamp', 'event_id' : 'query_outcome'})
        
    # # df[['session_id', 'experiment_group', 'search_state', 'selected_id', 'query_id']] = json.loads(str(df['event_data'])).values()
    
    # df[['session_id', 'experiment_group', 'selected_id', 'query_id', 'query_length']] = df['event_data'].apply(
        # lambda x: pd.Series({
            # 'session_id': json.loads(x).get('session_id'),
            # 'experiment_group': json.loads(x).get('experimentGroup'),
            # 'selected_id': json.loads(x).get('selectedIndexes'),
            # 'query_id' : json.loads(x).get('eventIndex'),
            # 'query_length': json.loads(x).get('searchStateFeatures', {}).get('queryLength')
        # })
    # )
    
    # df = df.drop(columns=['event_data'])
    
    # return df