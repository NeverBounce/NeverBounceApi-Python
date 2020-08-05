import neverbounce_sdk

# Load api key from .env in project root
with open(".env", "r") as dotenv:
    api_key = dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(api_key=api_key, api_version='v4.2')

# Verify email
verification = client.single_check(
    email='support@neverbounce.com',
    address_info=True,
    credits_info=True,
    historical_data=False,
    timeout=10  # Timeout in seconds
)
print(verification)
