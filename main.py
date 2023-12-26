import praw
import csv
from datetime import datetime
import pandas as pd 
import os
import sys

def url_scraper(subreddit_name):
    # Reddit API credentials
    client_id = 'jh9iRoDr15Ce22oM4rNT2Q'
    client_secret = 'nftbO-r1ReVlv4QDH3tD7raEGMu2Gg'
    user_agent = 'Riwaz'

    # Authenticate with Reddit
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    # Access the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Search for posts with the keyword
    keyword_posts = subreddit.search(keyword, limit=None)

    # Create the "UrlData" directory if it doesn't exist
    directory_path = "UrlData"
    os.makedirs(directory_path, exist_ok=True)

    # Create a CSV file with the subreddit name
    csv_file_path = os.path.join(directory_path, f"{subreddit_name}.csv")
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'URL', 'Author', 'Upvotes', 'Comments', 'Created UTC']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        csv_writer.writeheader()

        # Iterate through the posts
        for submission in keyword_posts:
            # Convert UTC timestamp to MM/DD/YYYY format
            created_utc_formatted = datetime.utcfromtimestamp(submission.created_utc).strftime('%m/%d/%Y')

            # Write data to CSV file
            csv_writer.writerow({
                'Title': submission.title,
                'URL': submission.shortlink,  # Use shortlink as the URL
                'Author': submission.author,
                'Upvotes': submission.score,
                'Comments': submission.num_comments,
                'Created UTC': created_utc_formatted
            })

    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, parse_dates=['Created UTC'])

    # Sort DataFrame by 'Created UTC' in ascending order
    df = df.sort_values(by='Created UTC')

    # Write the sorted DataFrame back to the CSV file
    df.to_csv(csv_file_path, index=False)

    # Print a confirmation message
    print(f'Data exported and sorted by Created UTC to {csv_file_path}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <subreddit_name>")
        sys.exit(1)

    subreddit_name = sys.argv[1]
    keyword = 'police'

    # Call the url_scraper function with the specified subreddit
    url_scraper(subreddit_name)

