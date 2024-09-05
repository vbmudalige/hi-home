import boto3
from botocore.exceptions import ClientError
import base64

client = boto3.client("bedrock-runtime", region_name="ap-southeast-2")
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

location = input("Enter the location: ")
item = input("Enter the item name: ")
image_name = input("Enter the image name: ")

with open(f"images/{image_name}", "rb") as f:
    image = f.read()

conversation = [
    {
        "role": "user",
        "content": [
            {
                "text": f"This is a {item} in a {location} home. We need to know what kind of maintenance is required for this {item}? What kind of tradies are required and how frequently should this maintenance be done? Need some cost estimation as well. Give me all kinds of possible jobs. Organize each job in this format \n Job Category:....\n Description:..... \nFrequency:..... \n Cost Estimation:...... \n"
            },
            {"image": {"format": "jpeg", "source": {"bytes": image}}},
        ],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=conversation,
        inferenceConfig={"maxTokens": 4096, "temperature": 1},
        additionalModelRequestFields={"top_k": 250},
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
