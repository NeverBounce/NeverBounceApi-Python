import neverbounce_sdk

# Load api key from .env in project root
with open (".env", "r") as dotenv:
    token=dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(auth=token)

f = open('results.csv', mode='wb')

# Jobs download
resp = client.jobs_download(job_id=289022, fd=f);
f.close()
