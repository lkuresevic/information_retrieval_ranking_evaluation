import pandas as pd
import numpy as np
import json
import csv

def create_dataframe():
    timestamp, device_id, experiment_group, session_id, query_length, selected_id, query_id, query_outcome  = [], [], [], [], [], [], [], []
    
    with open('2024InternshipData.csv', 'r') as csvfile: 
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

def analyze_group(df):
    success_n = 0
    total_n = 0
    querys_before_success_list = []
    elapsed_time_before_success_list = []
    query_length_diff_list = []
    choice_rank_list = []
    
    
    # Group by session to analyze each session individually
    for session_id, session_data in df.groupby(['session_id', 'device_id']):
        total_n += 1  # Count each session
        
        is_successful = (
            (session_data['query_outcome'].iloc[-1] == 'sessionFinished') and
            pd.notna(session_data['selected_id'].iloc[-1])
        )
        
        if is_successful:
            success_n += 1
           
            # Number of lookups before success
            querys_before_success = len(session_data)
            querys_before_success_list.append(querys_before_success)
            
            # Elapsed time before success
            elapsed_time_before_success = session_data['timestamp'].iloc[-1] - session_data['timestamp'].iloc[0]
            elapsed_time_before_success_list.append(elapsed_time_before_success)
            
            print("_____________________________________")
            # Query length difference
            query_length_diff = (session_data['query_length'].iloc[0] / session_data['query_length'].iloc[-1]) * 100 if session_data['query_length'].iloc[-1]>0 else 0
            query_length_diff_list.append(query_length_diff)
            
            choice_rank = session_data['selected_id'].iloc[-1]
            choice_rank_list.append(choice_rank)
 
    # Calculate percentage of successful sessions
    success_percentage = (success_n / total_n) * 100 if total_n > 0 else 0
    
    # Calculate metrics across sessions
    avg_querys_before_success = sum(querys_before_success_list) / success_n if querys_before_success_list else 0
    avg_elapsed_time_before_success = sum(elapsed_time_before_success_list) / success_n if elapsed_time_before_success_list else 0
    avg_query_length_diff = sum(query_length_diff_list) / success_n if query_length_diff_list else 0
    avg_choice_rank = sum(choice_rank_list) / success_n if choice_rank_list else 0
    
    # Results
    return {
        "id" : [0],
        "success_percentage": success_percentage,
        "avg_querys_before_success": avg_querys_before_success,
        "avg_elapsed_time_before_success": avg_elapsed_time_before_success,
        "avg_query_length_diff": avg_query_length_diff,
        "avg_choice_rank": avg_choice_rank
    }
               
if __name__ == "__main__":
    data = create_dataframe()
    group_0 = data[data['experiment_group'] == 0]
    group_1 = data[data['experiment_group'] == 1]
    
    group_0_results = analyze_group(group_0)
    group_1_results = analyze_group(group_1)
    
    with open('results.txt', 'w') as file:
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
    