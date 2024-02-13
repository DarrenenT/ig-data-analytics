import sys
import os
from datetime import datetime, timedelta
import time
import csv
import pandas as pd
import instaloader

#for recording time
total_time = 0
successful_accounts = 0
error_accounts = 0

# Get the current day of the week
current_day = datetime.now().strftime('%a')

# Use the current day to set the target list
# To divide script workload, preventing from getting banned by IG
if current_day == 'Mon':
    target_list = 'target_accounts_0.csv'
elif current_day == 'Wed':
    target_list = 'target_accounts_1.csv'
elif current_day == 'Fri':
    target_list = 'target_accounts_2.csv'
elif current_day == 'Sat':
    target_list = 'target_accounts_3.csv'
else:
    target_list = None

if target_list is not None:
    print(f"Today is {current_day}, using target list: {target_list}")
else:
    print(f"Today is {current_day}, no target list for today")
    sys.exit()

L = instaloader.Instaloader() # Get instance
df = pd.read_csv(target_list)
ig_accounts = df['Shop'].tolist()

for i, account in enumerate(ig_accounts, start=1):
    try:
        start_time = time.time()
        profile = instaloader.Profile.from_username(L.context, account)
        current_date = datetime.now()

        # Extract the required informations
        ig_acc_name = profile.username
        bio = profile.biography
        no_of_posts = profile.mediacount
        no_of_followers = profile.followers
        one_week_ago = current_date - timedelta(weeks=1)
        posts_in_last_week = 0
        likes_in_last_week = 0
        average_likes_per_post = 0
        skip_pinpost = 3
        for post in profile.get_posts():
            if post.date_utc > one_week_ago:
                posts_in_last_week += 1
                likes_in_last_week += post.likes
                time.sleep(2)  # sleep for 2 second
            else :
                skip_pinpost -= 1
                if skip_pinpost == 0:
                    break

        if posts_in_last_week != 0:
            average_likes_per_post = likes_in_last_week / posts_in_last_week

        # Open the CSV file in write mode
        with open('instagram_data_all.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the headers only if the file is empty
            if os.stat('instagram_data_all.csv').st_size == 0:
                writer.writerow(
                    ["ig acc name",
                    "date of scraping", 
                    "bio", 
                    "no. of post", 
                    "no. of follower", 
                    "posts in last week", 
                    "average likes per posts"])

            # Write the data
            writer.writerow([ig_acc_name, 
                            current_date.strftime('%Y-%m-%d'), 
                            bio, 
                            no_of_posts, 
                            no_of_followers, 
                            posts_in_last_week, 
                            average_likes_per_post])
            
        time.sleep(2)  # sleep for 2 second
        
        time_taken = time.time() - start_time
        total_time += time_taken
        successful_accounts += 1
        print(f"Processed {account},{i} out of {len(ig_accounts)}, took {time_taken} seconds.")

    except instaloader.exceptions.InstaloaderException:
        error_accounts += 1
        print(f"Error processing account: {account}")
        continue

average_time_taken = total_time / successful_accounts if successful_accounts != 0 else 0
print(f"Processed {successful_accounts + error_accounts} accounts in {total_time} seconds, average time taken per account: {average_time_taken} seconds.")
print("Successful: ", successful_accounts, "Error: ", error_accounts)
