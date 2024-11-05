from utils import *
from eval import *

if __name__ == "__main__":
    # Create dataframes extracting data from the .csv file
    
    data = create_dataframe()    
    group_0 = data[data['experiment_group'] == 0]
    group_1 = data[data['experiment_group'] == 1]
    
    # Analyze the data
    group_0_results = analyze_group(group_0)
    group_1_results = analyze_group(group_1)
    
    # Plot
    plot_data(group_0_results, group_1_results)
    
    # Write report
    write_report(group_0_results, group_1_results)