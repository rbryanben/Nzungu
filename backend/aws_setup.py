from dotenv import load_dotenv
load_dotenv()

import boto3
import os

# Reagion 
reagion = os.getenv('AWS_REAGION')
