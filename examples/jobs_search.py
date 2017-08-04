import neverbounce_sdk

# Load api key from .env in project root
with open (".env", "r") as dotenv:
    token=dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(auth=token)

# Get jobs
jobs = client.jobs_search();
for job in jobs:
    print(job)
