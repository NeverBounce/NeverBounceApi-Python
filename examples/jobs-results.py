import neverbounce_sdk

# Load api key from .env in project root
with open (".env", "r") as dotenv:
    token=dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(auth=token)

# Get job's results
jobs = client.jobs_results(job_id=289022);
for job in jobs:
    print(job)
