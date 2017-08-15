import neverbounce_sdk

# Load api key from .env in project root
with open(".env", "r") as dotenv:
    api_key = dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(api_key=api_key)

# Verify email
verification = client.single_check(email='support@neverbounce.com')
print("Result: " + verification['result'])
