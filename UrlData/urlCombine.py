import os
import pandas as pd

def combine_csv_files_with_subreddit(directory_path, output_file_name='mainURL.csv'):
    """
    Combine multiple CSV files in a directory into a single CSV file.
    Add a 'subreddit' row with the filename and sort by 'Created UTC'.

    Parameters:
        directory_path (str): The path to the directory containing CSV files.
        output_file_name (str): The name of the output combined CSV file.

    Returns:
        None
    """
    # Get a list of all CSV files in the specified directory
    csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

    # Initialize an empty DataFrame to store the combined data
    combined_data = pd.DataFrame()

    # Iterate through each CSV file and append its data to the combined DataFrame
    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_path)

        # Add a new 'subreddit' row with the filename
        df['subreddit'] = os.path.splitext(file)[0]

        combined_data = combined_data.append(df, ignore_index=True)

    # Sort DataFrame by 'Created UTC' in ascending order
    combined_data['Created UTC'] = pd.to_datetime(combined_data['Created UTC'])
    combined_data = combined_data.sort_values(by='Created UTC')

    # Specify the path for the output combined CSV file
    output_file_path = os.path.join(directory_path, output_file_name)

    # Write the combined data to a new CSV file
    combined_data.to_csv(output_file_path, index=False)

    print(f'Data from {len(csv_files)} CSV files combined and saved to {output_file_path}')

# Example usage:
directory_path = '/Users/riwazp/Desktop/PolicingSentiments/UrlData'
combine_csv_files_with_subreddit(directory_path)

