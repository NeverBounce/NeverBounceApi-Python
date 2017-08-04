import neverbounce_sdk

# Load api key from .env in project root
with open (".env", "r") as dotenv:
    token=dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(auth=token)

# Verify email
verification = client.single_verify(email='support@neverbounce.com');
print("Result: " + verification['result'])
