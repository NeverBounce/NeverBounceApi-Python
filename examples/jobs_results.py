import neverbounce_sdk

# Load api key from .env in project root
with open(".env", "r") as dotenv:
    api_key = dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(api_key=api_key)

# Get job's results
jobs = client.jobs_results(
    job_id=289022
    # page=1,  # Page to start from
    # items_per_page=10,  # Number of items per page
)
for job in jobs:
    print(job)
