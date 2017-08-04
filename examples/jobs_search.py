import neverbounce_sdk

# Load api key from .env in project root
with open(".env", "r") as dotenv:
    api_key = dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(api_key=api_key)

# Get jobs
jobs = client.jobs_search(
    # job_id=10000,  # Filter jobs based on id
    # filename='Book1.csv',  # Filter jobs based on filename
    # job_status='complete',  # Show completed jobs only
    # page=1,  # Page to start from
    # items_per_page=10,  # Number of items per page
)
for job in jobs:
    print(job)
