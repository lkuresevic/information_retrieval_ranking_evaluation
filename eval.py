from utils import *

from scipy.special import binom
from scipy.stats import chi2_contingency, mannwhitneyu, norm, t, ttest_ind

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
        "success_percentage": success_percentage,
        "avg_querys_before_success": avg_querys_before_success,
        "avg_elapsed_time_before_success": avg_elapsed_time_before_success/1000,
        "avg_query_length_diff": avg_query_length_diff,
        "avg_choice_rank": avg_choice_rank
    }