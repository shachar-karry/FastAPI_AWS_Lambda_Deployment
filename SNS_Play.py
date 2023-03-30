from dotenv import load_dotenv, find_dotenv
import os
import boto3

load_dotenv(find_dotenv())

sns_client = boto3.client("sns")

for i in range(3):
    sns_client.publish(PhoneNumber="+972523370403", Message=f"Hello SNS ({i})")

