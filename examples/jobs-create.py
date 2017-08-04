import neverbounce_sdk

# Load api key from .env in project root
with open (".env", "r") as dotenv:
    token=dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(auth=token)

# Create array of data
inputData = [
    {
        'id': '12345',
        'email': 'support@neverbounce.com',
        'name': 'Fred McValid'
    },
    {
        'id': '12346',
        'email': 'invalid@neverbounce.com',
        'name': 'Bob McInvalid'
    }
]

# Create Job
resp = client.jobs_create(input=inputData, filename="Created from Python Wrapper.csv");
print(resp['job_id'])
