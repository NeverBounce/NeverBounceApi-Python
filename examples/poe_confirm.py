import neverbounce_sdk

# Load api key from .env in project root
with open(".env", "r") as dotenv:
    api_key = dotenv.read().replace('\n', '')

# Create sdk client
client = neverbounce_sdk.client(api_key=api_key)

# Confirm frontend widget
resp = client.poe_confirm(
    email='support@neverbounce.com',
    transaction_id='NBPOE-TXN-5942940c09669',
    confirmation_token='e3173fdbbdce6bad26522dae792911f2',
    result='valid'
)
print(resp['token_confirmed'])
