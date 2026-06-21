import os
import random
from datetime import datetime, timedelta
import subprocess

start_date = datetime(2026, 6, 13, 10, 0, 0)
messages = [
    "Refactoring components", "Updating styles", "Fixing minor bugs",
    "Adding test cases", "Optimizing performance", "Cleaning up imports",
    "Writing docs", "Updating dependencies", "Fixing typings"
]

for day_offset in range(9): # June 13 to June 21
    current_date = start_date + timedelta(days=day_offset)
    num_commits = random.randint(5, 7)
    
    for i in range(num_commits):
        commit_time = current_date + timedelta(hours=i)
        time_str = commit_time.isoformat()
        
        msg = random.choice(messages)
        
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = time_str
        env["GIT_COMMITTER_DATE"] = time_str
        
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", msg],
            env=env,
            check=True
        )
        print(f"Committed on {time_str}")

